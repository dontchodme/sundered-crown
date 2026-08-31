#!/usr/bin/env python3
"""RICK'S §1 FOR NIGHTFELL, PRICED.

    "nightfell crackles with purple electricity. for the duration of the ult
     when it lands a hit the hit leaves behind an echo bomb (thinking a
     pentagram imprinted on the battlefield) the echos slowly begin to crackle
     with the same purple electricity and then explode. dealing damage,
     applying curse and knocking back enemy fighters in its area."

THE QUESTION THAT DECIDES WHETHER THIS IS A DIFFERENT ULTIMATE FROM
GRAVEMOURN'S IS THE CATCH RATE. Both designs are: a window; each blow inside
it spawns a delayed explosive; the explosive deals damage, applies Curse and
knocks back. The ONLY structural difference is that a hand FLIES TO the foe
and a bomb STAYS WHERE THE BLOW LANDED.

So the whole difference is: how often is the foe still there when it goes off?
If the answer is "nearly always", Nightfell has Gravemourn's ultimate with a
different sprite. Arena is 520x800 and ballR is 34; the roster's novas run
240-320 radius, which is most of the floor.

  [1] THE CATCH RATE — fuse x radius, the only table that matters.
  [2] THE POSITION IS THE MECHANIC — the same arm with the bomb HOMING onto
      the foe, which is Gravemourn's design, priced as the control.
  [3] DOES THE BOMB'S CURSE STACK SURVIVE? On the flail it was worth +0.4pp
      because a hand could not out-hit a 65-damage blade. Nightfell's blows
      land at ~26, so a bomb CAN out-hit them and its memory can stick. This
      is the one place the school's two relics genuinely differ.

Base curse: K=3, echo 8%, permanent, displacement kept, priced on the target.
Eclipse's `apply:{curse:3}` is stripped in every arm. Runtime only.
"""
from __future__ import annotations
import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent
DONOR = "nightfell"

JS = r"""([donor, foes, seeds, secs, K, RATE, DUR, FUSE, RAD, DMG, KNOCK, HOME, CURSE, BLADE, MINE, LIFE, BPH, SCAT, SELFTRIG]) => {
  const DT = AC.CONFIG.physics.dt, CU = AC.STATUS.curse;
  const oL = CU.maxHpLoss, oC = CU.maxStacks;
  const origResolve = AC.Match.prototype.resolveHit;
  const origFire = AC.Match.prototype.fireUlt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const bA = w.ult.apply, bD = w.dmg, bUd = w.ult.dmg, bKn = w.ult.knock;
  delete w.ult.apply; w.ult.dmg = 0; w.ult.knock = 0;
  if (BLADE > 0) w.dmg = BLADE;
  CU.maxHpLoss = 0; CU.maxStacks = K;

  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const pool = [], bombs = [];
    let inR = false, src = null, hd0 = 0;
    let echoD = 0, bombD = 0, blows = 0, casts = 0, winUntil = -1;
    let lastBoom = -99, chainHits = 0, run_ = 0, maxRun = 0, liveMax = 0;
    let selfHits = 0, selfDmg = 0;
    let spawned = 0, caught = 0, missed = 0, sepSum = 0;

    const trim = () => { pool.sort((a,b)=>b-a); while (pool.length > K) pool.pop(); };
    const oApply = th.apply.bind(th);
    th.apply = function(k, n){
      if (k === "curse"){ const v = inR ? (src.dealt - hd0) : 0;
        if (v > 0){ for (let i=0;i<n;i++) pool.push(v); trim(); } }
      return oApply(k, n);
    };

    m.resolveHit = function(s2, foe, hx, hy, seg, mul, over){
      if (foe !== th) return origResolve.call(this, s2, foe, hx, hy, seg, mul, over);
      const p0 = s2.dealt, h0 = s2.hits;
      let sum = 0; for (const v of pool) sum += v;
      const e = Math.round(sum * RATE);
      inR = true; src = s2; hd0 = p0;
      origResolve.call(this, s2, foe, hx, hy, seg, mul, over);
      inR = false;
      if (s2.hits === h0) return;
      blows++;
      if (e > 0 && foe.alive){ this.hurt(foe, e, s2); echoD += e; }
      /* THE BOMB IS LEFT WHERE THE BLOW LANDED. It does not follow. */
      if (s2 === me && winUntil > this.t){
        /* THE ECHO BOMB, read literally: the imprint is stamped with what
           Curse remembers at the moment the blow lands. A COPY -- the pool is
           not spent, which is what keeps it off Gravemourn's verb. */
        let stamp = 0; for (const v of pool) stamp += v;
        /* BOMBS PER HIT, scattered deterministically off the contact point --
           a chain needs more than one thing to chain into, and Nightfell only
           lands ~2 blows inside an 8s window. */
        for (let i = 0; i < BPH; i++){
          /* SCAT < 0 == THE FIGURE: charges evenly spaced on a ring of
             |SCAT|, so one blow stamps ONE sigil rather than scattering dots.
             The chain is then a chain WITHIN the figure. */
          const ring = SCAT < 0;
          const a2 = ring ? (i * 6.2831853 / BPH + (spawned * 0.7) % 6.2831853)
                          : (spawned * 2.399963 + i * 1.7) % 6.2831853;
          const rr = ring ? -SCAT
                          : (i === 0 ? 0 : SCAT * (0.55 + 0.45 * ((i * 7 % 5) / 5)));
          spawned++;
          bombs.push({ at: this.t + FUSE, x: hx + Math.cos(a2)*rr,
                       y: hy + Math.sin(a2)*rr, mem: stamp / BPH });
        }
      }
    };

    m.fireUlt = function(fr, foe){
      const r = origFire.call(this, fr, foe);
      if (fr === me && foe === th){ casts++; winUntil = this.t + DUR; }
      return r;
    };

    let step = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++;
      if (winUntil > 0 && m.t > winUntil) winUntil = -1;
      /* MINE: the imprint ARMS after the fuse and then waits. It goes off the
         moment the foe is inside it, or expires unspent after LIFE. His §1
         says "then explode" -- a timer -- so this is a fork, not the design. */
      if (MINE){
        let live = 0;
        for (const b of bombs) if (m.t >= b.at) live++;
        if (live > liveMax) liveMax = live;
        for (let i = bombs.length - 1; i >= 0; i--){
          const b = bombs[i];
          if (m.t < b.at) continue;                       // still crackling
          if (m.t > b.at + LIFE){ bombs.splice(i,1); missed++; continue; }
          /* THE CASTER STANDS ON ITS OWN FLOOR. A landmine does not know who
             put it there. SELFTRIG makes the figures a hazard to both balls. */
          if (SELFTRIG && me.alive){
            const ds = Math.hypot(me.x - b.x, me.y - b.y);
            const df = Math.hypot(th.x - b.x, th.y - b.y);
            if (ds <= RAD && (ds < df || df > RAD)){
              bombs.splice(i,1); selfHits++;
              const sd = Math.round((DMG < 0 ? b.mem * (-DMG) : DMG) * me.dmgTakenMul());
              if (sd > 0){ m.hurt(me, sd, th); selfDmg += sd; }
              const dx2 = me.x - b.x, dy2 = me.y - b.y, dl2 = Math.hypot(dx2,dy2) || 1;
              me.vx += (dx2/dl2) * KNOCK; me.vy += (dy2/dl2) * KNOCK;
              me.flash = 1;
              continue;
            }
          }
          const d = Math.hypot(th.x - b.x, th.y - b.y);
          if (d > RAD || !th.alive) continue;
          bombs.splice(i,1); caught++; sepSum += d;
          if (m.t - lastBoom <= 0.45){ chainHits++; run_++; }
          else run_ = 1;
          if (run_ > maxRun) maxRun = run_;
          lastBoom = m.t;
          const raw = DMG < 0 ? b.mem * (-DMG) : DMG;
          const dmg = Math.round(raw * th.dmgTakenMul());
          if (dmg > 0){ m.hurt(th, dmg, me); me.dealt += dmg; bombD += dmg; }
          if (CURSE && dmg > 0 && th.alive){ pool.push(dmg); trim(); }
          const dx = th.x - b.x, dy = th.y - b.y, dl = Math.hypot(dx,dy) || 1;
          th.vx += (dx/dl) * KNOCK; th.vy += (dy/dl) * KNOCK;
          th.flash = 1;
        }
        continue;
      }
      while (bombs.length && bombs[0].at <= m.t){
        const b = bombs.shift();
        if (!th.alive) continue;
        /* HOME = the control: the blast is centred on the foe instead, which
           is Gravemourn's design and the thing this must not be. */
        const cx = HOME ? th.x : b.x, cy = HOME ? th.y : b.y;
        const d = Math.hypot(th.x - cx, th.y - cy);
        sepSum += d;
        if (d > RAD){ missed++; continue; }
        caught++;
        const raw2 = DMG < 0 ? b.mem * (-DMG) : DMG;
        const dmg = Math.round(raw2 * th.dmgTakenMul());
        if (dmg > 0){ m.hurt(th, dmg, me); me.dealt += dmg; bombD += dmg; }
        if (CURSE && dmg > 0 && th.alive){ pool.push(dmg); trim(); }
        const dx = th.x - cx, dy = th.y - cy, dl = Math.hypot(dx, dy) || 1;
        th.vx += (dx/dl) * KNOCK; th.vy += (dy/dl) * KNOCK;
        th.flash = 1;
      }
    }
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                echoD, bombD, blows, casts, spawned, caught, missed,
                chainHits, maxRun, liveMax, selfHits, selfDmg,
                sep: (caught+missed) ? sepSum/(caught+missed) : 0 });
  }
  CU.maxHpLoss = oL; CU.maxStacks = oC;
  w.dmg = bD; w.ult.dmg = bUd; w.ult.knock = bKn; if (bA) w.ult.apply = bA;
  return rows;
}"""

ap = argparse.ArgumentParser()
ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
ap.add_argument("--seeds", type=int, default=8)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--dur", type=float, default=8.0)
ap.add_argument("--dmg", type=float, default=30.0)
ap.add_argument("--knock", type=float, default=250.0)
ap.add_argument("--stage", default="catch")
a = ap.parse_args()
seeds = [3301 + 19*i for i in range(a.seeds)]

with game(game_path=(HERE / a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != DONOR]
    mm = lambda r,k: statistics.mean([x[k] for x in r])
    wr = lambda r: (lambda f: sum(x["win"] for x in f)/len(f))([x for x in r if x["win"]>=0])
    def run(fuse, rad, home=False, curse=True, dmg=None, blade=0, mine=False, life=6.0, bph=1, scat=70.0, selftrig=False):
        return page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, a.dur, fuse,
                                  rad, a.dmg if dmg is None else dmg, a.knock,
                                  home, curse, blade, mine, life, bph, scat, selftrig])

    if a.stage == "catch":
        print(f"\n  ARENA 520x800, ballR 34. Roster novas run radius 240-320.")
        print(f"  Nightfell, curse K3 echo 8%, {a.dur:.0f}s window, bomb {a.dmg:.0f} dmg, "
              f"knock {a.knock:.0f}. {25*a.seeds} fights an arm.\n")
        print(f"[1] THE CATCH RATE — is the foe still there when it goes off?\n")
        print(f"    {'fuse':>6}" + "".join(f"{('r=%d'%r):>22}" for r in (90,160,240)))
        print(f"    {'':>6}" + "".join(f"{'catch':>10}{'win':>12}" for _ in range(3)))
        for fuse in (0.8, 1.6, 2.6):
            cells = []
            for rad in (90, 160, 240):
                r = run(fuse, rad)
                sp, ca = mm(r,'spawned'), mm(r,'caught')
                cells.append((ca/sp if sp else 0, wr(r)))
            print(f"    {fuse:>5.1f}s" + "".join(f"{c:>9.0%}{w:>12.1%}" for c,w in cells))
        print(f"\n[2] THE CONTROL — the same bomb, HOMING onto the foe "
              f"(= Gravemourn's design)\n")
        print(f"    {'fuse':>6}{'radius':>8}{'stays put':>12}{'homing':>10}{'position costs':>16}")
        for fuse, rad in ((1.6, 90), (1.6, 160), (1.6, 240)):
            s_ = run(fuse, rad); h_ = run(fuse, rad, home=True)
            print(f"    {fuse:>5.1f}s{rad:>8}{wr(s_):>12.1%}{wr(h_):>10.1%}"
                  f"{wr(s_)-wr(h_):>+16.1%}")

    if a.stage == "knobs":
        print(f"\n[11] THE TWO KNOBS THIS DOC HAS BEEN QUOTING WITHOUT MEASURING.")
        print(f"     Settled config: mine, 5 charges on a 60u ring, per-charge r70,")
        print(f"     push 250, stamp pool x0.3, blade 13, foe-only.\n")
        print(f"     HOW LONG A LIVE PENTAGRAM WAITS (window 8s)")
        print(f"      {'life':>7}{'charges':>9}{'caught':>8}{'catch%':>8}{'expired':>9}"
              f"{'chained':>9}{'longest':>9}{'bomb dmg':>10}{'win':>8}")
        for life in (2.0, 4.0, 6.0, 10.0, 99.0):
            r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, 8.0,
                                   1.6, 70, -0.3, 250, False, True, 13,
                                   True, life, 5, -60, False])
            fin=[x for x in r if x["win"]>=0]; w_=sum(x["win"] for x in fin)/len(fin)
            sp=mm(r,'spawned')
            print(f"      {life:>7.0f}{sp:>9.1f}{mm(r,'caught'):>8.1f}"
                  f"{mm(r,'caught')/sp if sp else 0:>8.0%}{mm(r,'missed'):>9.1f}"
                  f"{mm(r,'chainHits'):>9.2f}{mm(r,'maxRun'):>9.2f}"
                  f"{mm(r,'bombD'):>10.0f}{w_:>8.1%}")
        print(f"\n     HOW LONG THE WINDOW STAYS OPEN (life 6s)")
        print(f"      {'window':>7}{'figures':>9}{'charges':>9}{'caught':>8}"
              f"{'chained':>9}{'longest':>9}{'bomb dmg':>10}{'win':>8}")
        for dur in (4.0, 6.0, 8.0, 12.0, 16.0):
            r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, dur,
                                   1.6, 70, -0.3, 250, False, True, 13,
                                   True, 6.0, 5, -60, False])
            fin=[x for x in r if x["win"]>=0]; w_=sum(x["win"] for x in fin)/len(fin)
            print(f"      {dur:>6.0f}s{mm(r,'spawned')/5:>9.2f}{mm(r,'spawned'):>9.1f}"
                  f"{mm(r,'caught'):>8.1f}{mm(r,'chainHits'):>9.2f}"
                  f"{mm(r,'maxRun'):>9.2f}{mm(r,'bombD'):>10.0f}{w_:>8.1%}")

    if a.stage == "self":
        print(f"\n[10] CAN THE CASTER SET ONE OFF? A landmine does not know who put")
        print(f"     it there. 5 points, ring 60, per-charge radius 70, push 250,")
        print(f"     stamp pool x0.3, blade 13, mine.\n")
        print(f"      {'arm':22}{'win':>8}{'charges':>9}{'foe hits':>10}{'SELF hits':>11}"
              f"{'self dmg':>10}{'chained':>9}{'longest':>9}")
        for lab, st, blade in (("foe only", False, 13), ("both balls", True, 13),
                               ("both, blade 15.83", True, 15.83),
                               ("both, blade 18", True, 18)):
            r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, a.dur,
                                   1.6, 70, -0.3, 250, False, True, blade,
                                   True, 6.0, 5, -60, st])
            fin=[x for x in r if x["win"]>=0]
            w_=sum(x["win"] for x in fin)/len(fin)
            print(f"      {lab:22}{w_:>8.1%}{mm(r,'spawned'):>9.1f}{mm(r,'caught'):>10.1f}"
                  f"{mm(r,'selfHits'):>11.2f}{mm(r,'selfDmg'):>10.0f}"
                  f"{mm(r,'chainHits'):>9.2f}{mm(r,'maxRun'):>9.2f}")

    if a.stage == "push":
        print(f"\n[9] PUSH, IN A RING. A shove off one charge throws the ball ACROSS")
        print(f"    the figure rather than out of a scatter. Rick's call is push on")
        print(f"    legibility; this is what it costs, or buys, in the arrangement")
        print(f"    that was chosen with it. 5 points, per-charge radius 70,")
        print(f"    stamp pool x0.3, blade 13, mine.\n")
        print(f"      {'ring r':>8}{'push':>7}{'charges':>9}{'caught':>8}{'catch%':>8}"
              f"{'chained':>9}{'longest':>9}{'bomb dmg':>10}{'win':>8}")
        for ring in (60, 90, 120):
            for kn in (0, 250, 500, 800):
                r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, a.dur,
                                       1.6, 70, -0.3, kn, False, True, 13,
                                       True, 6.0, 5, -ring])
                fin=[x for x in r if x["win"]>=0]
                w_=sum(x["win"] for x in fin)/len(fin)
                sp=mm(r,'spawned')
                print(f"      {ring:>8}{kn:>7}{sp:>9.1f}{mm(r,'caught'):>8.1f}"
                      f"{mm(r,'caught')/sp if sp else 0:>8.0%}{mm(r,'chainHits'):>9.2f}"
                      f"{mm(r,'maxRun'):>9.2f}{mm(r,'bombD'):>10.0f}{w_:>8.1%}")
            print()

    if a.stage == "figure":
        print(f"\n[8] THE PENTAGRAM IS THE CLUSTER. One blow stamps ONE figure --")
        print(f"    charges evenly spaced on a ring -- so the density that makes it")
        print(f"    chain comes from inside the sigil, not from carpeting the hall.")
        print(f"    mine, radius per charge 70, stamp pool x0.3, blade 13.\n")
        print(f"      {'points':>7}{'ring r':>8}{'knock':>8}{'figures':>9}{'charges':>9}"
              f"{'caught':>8}{'chained':>9}{'longest':>9}{'win':>8}")
        for pts, ring in ((5, 60), (5, 85), (5, 110), (3, 70)):
            for kn in (0, -350):
                r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, a.dur,
                                       1.6, 70, -0.3, kn, False, True, 13,
                                       True, 6.0, pts, -ring])
                fin=[x for x in r if x["win"]>=0]
                w_=sum(x["win"] for x in fin)/len(fin)
                lab = "pull %d"%abs(kn) if kn<0 else "none"
                print(f"      {pts:>7}{ring:>8}{lab:>8}{mm(r,'spawned')/pts:>9.2f}"
                      f"{mm(r,'spawned'):>9.2f}{mm(r,'caught'):>8.2f}"
                      f"{mm(r,'chainHits'):>9.2f}{mm(r,'maxRun'):>9.2f}{w_:>8.1%}")

    if a.stage == "implode":
        print(f"\n[7] THE SIGN OF THE SHOVE. Bombs are planted where blows land,")
        print(f"    which is a CLUSTER -- so a push ejects the ball from the field")
        print(f"    it is standing in. A pull holds it there. Negative knock drags")
        print(f"    the foe TOWARD the blast. mine, radius 110, stamp pool x0.3, blade 13.\n")
        for bph in (2, 3):
            print(f"    bombs per blow = {bph}")
            print(f"      {'knock':>8}{'caught':>8}{'chained':>9}{'longest':>9}"
                  f"{'bomb dmg':>10}{'win':>8}")
            for kn in (-700, -400, -200, 0, 250, 500):
                r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, a.dur,
                                       1.6, 110, -0.3, kn, False, True, 13,
                                       True, 6.0, bph, 70.0])
                fin=[x for x in r if x["win"]>=0]
                w_=sum(x["win"] for x in fin)/len(fin)
                lab = ("pull %d"%abs(kn)) if kn < 0 else ("push %d"%kn if kn else "none")
                print(f"      {lab:>8}{mm(r,'caught'):>8.2f}{mm(r,'chainHits'):>9.2f}"
                      f"{mm(r,'maxRun'):>9.2f}{mm(r,'bombD'):>10.0f}{w_:>8.1%}")
            print()

    if a.stage == "chain":
        print(f"\n[6] THE CHAIN — does a knockback fling the ball into the next one?")
        print(f"    mine, fuse 1.6s arm + 6s wait, stamp pool x0.3, blade 13.")
        print(f"    A chain hit is a detonation within 0.45s of the previous one.\n")
        for bph in (1, 2, 3):
            print(f"    bombs per blow = {bph}  (scatter 70u)")
            print(f"      {'radius':>7}{'knock':>7}{'planted':>9}{'caught':>8}"
                  f"{'live at once':>14}{'chained':>9}{'longest':>9}{'win':>8}")
            for rad in (70, 110):
                for kn in (0, 250, 500, 850):
                    global_knock = kn
                    r = page.evaluate(JS, [DONOR, foes, seeds, a.secs, 3, 0.08, a.dur,
                                           1.6, rad, -0.3, kn, False, True, 13,
                                           True, 6.0, bph, 70.0])
                    fin=[x for x in r if x["win"]>=0]
                    w_=sum(x["win"] for x in fin)/len(fin)
                    print(f"      {rad:>7}{kn:>7}{mm(r,'spawned'):>9.2f}{mm(r,'caught'):>8.2f}"
                          f"{mm(r,'liveMax'):>14.2f}{mm(r,'chainHits'):>9.2f}"
                          f"{mm(r,'maxRun'):>9.2f}{w_:>8.1%}")
            print()

    if a.stage == "echo":
        print(f"\n[5] THE ECHO BOMB — the imprint is stamped with what Curse")
        print(f"    remembers when the blow lands. A COPY: the pool is not spent,")
        print(f"    which is what keeps it off Gravemourn's verb.\n")
        print(f"    mine, fuse 1.6s arm + 6s wait, radius 90, knock {a.knock:.0f}, "
              f"blade 15.83\n")
        print(f"    {'stamp':>8}{'no curse':>11}{'+ curse':>10}{'adds':>7}"
              f"{'bombs':>8}{'caught':>8}{'bomb dmg':>10}{'echo dmg':>10}")
        for mult in (0.5, 0.75, 1.0, 1.4):
            n_ = run(1.6, 90, curse=False, dmg=-mult, mine=True)
            c_ = run(1.6, 90, curse=True,  dmg=-mult, mine=True)
            print(f"    {('pool x%.2g'%mult):>8}{wr(n_):>11.1%}{wr(c_):>10.1%}"
                  f"{wr(c_)-wr(n_):>+7.1%}{mm(c_,'spawned'):>8.2f}{mm(c_,'caught'):>8.2f}"
                  f"{mm(c_,'bombD'):>10.0f}{mm(c_,'echoD'):>10.0f}")
        print(f"\n    and with the blade trimmed toward its target of ~13:")
        for blade in (15.83, 14, 13, 12):
            r = run(1.6, 90, curse=True, dmg=-1.0, mine=True, blade=blade)
            print(f"    {('blade %.4g'%blade):>12}{wr(r):>10.1%}"
                  f"{mm(r,'bombD'):>10.0f} bomb dmg{mm(r,'caught'):>8.2f} caught")

    if a.stage == "mine":
        print(f"\n[4] TIMED vs ARMED — his §1 says a timer. A mine is the fork.")
        print(f"    fuse 1.6s to arm, then 6s of waiting. bomb {a.dmg:.0f} dmg.\n")
        print(f"    {'radius':>8}{'timed catch':>13}{'timed win':>11}"
              f"{'mine catch':>12}{'mine win':>10}{'bombs':>8}")
        for rad in (60, 90, 130, 160, 240):
            t_ = run(1.6, rad)
            n_ = run(1.6, rad, mine=True)
            st, sn = mm(t_,'spawned'), mm(n_,'spawned')
            print(f"    {rad:>8}{mm(t_,'caught')/st if st else 0:>12.0%}{wr(t_):>11.1%}"
                  f"{mm(n_,'caught')/sn if sn else 0:>12.0%}{wr(n_):>10.1%}{sn:>8.2f}")

    if a.stage == "curse":
        print(f"\n[3] DOES THE BOMB'S CURSE STACK SURVIVE? fuse 1.6, radius 160")
        print(f"    Nightfell's blows land at ~26. A bomb that out-hits them parks a")
        print(f"    memory the blade cannot displace -- which the flail's hand could not do.\n")
        print(f"    {'bomb dmg':>9}{'no curse':>11}{'+ curse':>10}{'curse adds':>12}"
              f"{'bombs':>8}{'caught':>8}{'echo dmg':>10}")
        for d in (10, 20, 30, 45, 60):
            n_ = run(1.6, 160, curse=False, dmg=d)
            c_ = run(1.6, 160, curse=True,  dmg=d)
            print(f"    {d:>9}{wr(n_):>11.1%}{wr(c_):>10.1%}{wr(c_)-wr(n_):>+12.1%}"
                  f"{mm(c_,'spawned'):>8.2f}{mm(c_,'caught'):>8.2f}{mm(c_,'echoD'):>10.0f}")
    assert not errors, errors[:3]
