"""Scratch: control variants and mutants of an Oracle link (v105 §2-3). Each
variant is a small, exact-once edit of the built link, written to scratch and
never to the chain. CONTROLS move one of the build's readings back to the lab's;
MUTANTS break one sentence of the design (each must fail its own probe check).

  python variants.py --src <link> --v <name> --out <file>
"""
import argparse, hashlib, pathlib, sys

AIM_OLD = '''    else if (f.ultSight){
      if (f.alive && foe.alive){'''

V = {
 # ---- CONTROLS (the lab's constructions, one at a time) -------------------
 # the lab's clock: the window and the aim run through hit stops too
 "ctl-labclock": [
  ('''                                      / HP.massRef, HP.massWeight) * dt;
      }
      return;
    }
''', '''                                      / HP.massRef, HP.massWeight) * dt;
      }
      this.sightFrozen(dt);          // CONTROL: the lab's clock runs through the freeze
      return;
    }
'''),
  ('''  tickSight(dt){
''', '''  /* CONTROL (scratch, v105 §2): the lab's clock. The lab's overlay turned the
     facing and ran the window through every step, frozen or not. */
  sightFrozen(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultSight;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      if (f.alive && foe.alive){
        const S = f.w.shot;
        const tof = Math.hypot(foe.x - f.x, foe.y - f.y) / S.speed;
        const tx = foe.x + foe.vx * tof, ty = foe.y + foe.vy * tof;
        const want = ballisticAngle(tx - f.x, ty - f.y, S.speed, S.grav || 0);
        const dl = Math.atan2(Math.sin(want - f.theta), Math.cos(want - f.theta));
        const k = f.w.ult.turn * dt;
        f.theta += clamp(dl, -k, k);
      }
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive) f.ultSight = null;
    }
  }

  tickSight(dt){
'''),
 ],
 # the lab's spin: the spin keeps advancing theta in the window and the turn rides on it
 "ctl-labspin": [
  (AIM_OLD, '''    else if (f.ultSight){
      if (f.stun <= 0) f.theta += spin * dt * f.spinDir;   // CONTROL: the lab left the spin running
      if (f.alive && foe.alive){'''),
 ],
 # the lab's hex: the second hex on every blow in the window, the blade's too
 "ctl-labhex": [
  ('''    if (mul !== undefined && self.ultSight){''', '''    if (self.ultSight){                    // CONTROL: the lab counted every me.hits'''),
 ],
 # ---- MUTANTS (each breaks one sentence) -----------------------------------
 # [1] the window 1% long on its clock
 "mut-window": [
  ('''      f.ultSight = { t: 0, dur: u.dur };''', '''      f.ultSight = { t: 0, dur: u.dur * 1.01 };'''),
 ],
 # [2] no lead: aim at where the foe IS (the design's untaken 98%)
 "mut-nolead": [
  ('''        const tof = Math.hypot(foe.x - f.x, foe.y - f.y) / S.speed;
        const leadX = foe.x + foe.vx * tof''', '''        const tof = 0 * Math.hypot(foe.x - f.x, foe.y - f.y) / S.speed;
        const leadX = foe.x + foe.vx * tof'''),
 ],
 # [2] a stunned bow does not turn
 "mut-stunlock": [
  (AIM_OLD, '''    else if (f.ultSight){
      if (f.alive && foe.alive && f.stun <= 0){'''),
 ],
 # [3] the stream quickened in the window (tickFire touched)
 "mut-cadence": [
  ('''    f.fireCd += S.cadence * cm;''', '''    f.fireCd += S.cadence * cm * (f.ultSight ? 0.9 : 1);'''),
 ],
 # [5] the second hex on the blade's blows too
 "mut-bladehex": [
  ('''    if (mul !== undefined && self.ultSight){''', '''    if (self.ultSight){'''),
 ],
 # [5] the second hex outside the window too
 "mut-outhex": [
  ('''    if (mul !== undefined && self.ultSight){
      const T = self.sightTally;
      T.arrows++;
      if (self.w.ult.hex > 0 && foe.alive && !foe.shade){''', '''    if (mul !== undefined && (self.ultSight || self.sightTally)){
      const T = self.sightTally;
      if (self.ultSight) T.arrows++;
      if (self.w.ult.hex > 0 && foe.alive && !foe.shade){'''),
 ],
 # [7] a cast waits 0.5s past its charge
 "mut-wait": [
  ('''    if (f.charge >= f.w.ult.charge && !f.ultCorona''', '''    if (f.charge >= f.w.ult.charge + (f.w.ult.kind === "sight" ? 0.5 : 0) && !f.ultCorona'''),
 ],
 # [4] the window's arrows hit 10% harder (the arrow is not "as ever")
 "mut-dmg": [
  ("""            * (mul === undefined ? (forge ? self.w.ult.strikeMul : 1) : mul)""",
   """            * (mul === undefined ? (forge ? self.w.ult.strikeMul : 1) : mul * (self.ultSight ? 1.1 : 1))"""),
 ],
 # [6] the aim nudges the caster's ball
 "mut-nudge": [
  ("""        f.theta += clamp(dl, -k, k);
      }
    }
    else if (f.stun > 0){ /* weapon locked */ }""",
   """        f.theta += clamp(dl, -k, k);
        f.vx += 1e-9;
      }
    }
    else if (f.stun > 0){ /* weapon locked */ }"""),
 ],

 # ---- THE FIX ROUND (v105 review): mutants the first probe could not see ------
 # [7] the reviewer's rv-charge: the window feeds the charge 25% faster
 "rv-charge": [
  ("""        f.theta += clamp(dl, -k, k);
      }
    }
    else if (f.stun > 0){""", """        f.theta += clamp(dl, -k, k);
        f.charge += 0.25 * dt;
      }
    }
    else if (f.stun > 0){"""),
 ],
 # [6] the reviewer's rv-spindir: the bow leaves each window spinning the way it last turned
 "rv-spindir": [
  ("""        f.theta += clamp(dl, -k, k);
      }
    }
    else if (f.stun > 0){""", """        f.theta += clamp(dl, -k, k);
        if (dl) f.spinDir = dl > 0 ? 1 : -1;
      }
    }
    else if (f.stun > 0){"""),
 ],
 # [1] the window stretched 10% by a writer outside tickSight (the aim)
 "mut-winclock": [
  ("""        f.theta += clamp(dl, -k, k);
      }
    }
    else if (f.stun > 0){""", """        f.theta += clamp(dl, -k, k);
      }
      f.ultSight.t -= 0.1 * dt;
    }
    else if (f.stun > 0){"""),
 ],
 # [3] the stream quickened by a writer outside tickFire (each window arrow that lands)
 "mut-cdhit": [
  ("""    if (mul !== undefined && self.ultSight){
      const T = self.sightTally;
      T.arrows++;""", """    if (mul !== undefined && self.ultSight){
      const T = self.sightTally;
      T.arrows++;
      self.fireCd -= 0.05;"""),
 ],
}

ap = argparse.ArgumentParser(); ap.add_argument("--src", required=True); ap.add_argument("--v", required=True)
ap.add_argument("--out", required=True); a = ap.parse_args()
s = pathlib.Path(a.src).read_text(encoding="utf-8")
for old, new in V[a.v]:
    n = s.count(old)
    if n != 1: raise SystemExit(f"{a.v}: anchor found {n}x: {old.splitlines()[0]!r}")
    s = s.replace(old, new, 1)
out = pathlib.Path(a.out)
if out.exists(): raise SystemExit(f"refusing to overwrite {out}")
out.write_text(s, encoding="utf-8", newline="\n")
print(f"{a.v}: {out.name} {hashlib.sha256(s.encode()).hexdigest()[:16]}")
