"""Where each stage-6 event hangs: line numbers of fixed strings on the fx link and on the b12.5."""
import pathlib
L = pathlib.Path(__file__).resolve().parent.parent / "links"
NEED = [
 ("fireUlt", "  fireUlt(f, foe){"),
 ("the cast voice (fireUlt's prologue)", '    SFX.play("ult", { w: f.w.id });\n\n    const dist'),
 ("the life map line", "              censer: 1.6,"),
 ("the life map line (b12.5)", "              aureole: 1.6, censer: 1.6,"),
 ("the halo's cast branch", '    if (u.kind === "halo"){'),
 ("the window opens", "      f.ultHalo = { t: 0, dur: u.dur, cd: 0, bcd: 0 };"),
 ("step: tickHalo", "    this.tickHalo(dt);                  // BENEDICTION (v82)"),
 ("tickHalo(dt){", "  tickHalo(dt){"),
 ("the close voice", '      if (Z.t >= Z.dur && f.alive && foe.alive) SFX.play("ult", { w: "aureole-close" });'),
 ("the close", "      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHalo = null; continue; }"),
 ("the entry's test", "      const voiceIn = Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R;"),
 ("the entry voice", '      if (voiceIn && Z.voiceIn === 0) SFX.play("ult", { w: "aureole-enter" });'),
 ("the inside test", "      if (!(Math.hypot(foe.x - f.x, foe.y - f.y) < u.haloR + R)) continue;"),
 ("T.inFrames++", "      T.inFrames++;"),
 ("the smite", '        foe.apply("smite", u.smite, side);'),
 ("the blessing", '        f.apply("blessing", u.bless, side);'),
 ("T.bless", "        T.bless += u.bless;"),
 ("the heal chime", '        SFX.play("spark", { collect: true, n: f.stacks("blessing") });'),
 ("Sfx: the cast arm", '        } else if (w === "aureole"){'),
 ("Sfx: the entry arm", '        } else if (w === "aureole-enter"){'),
 ("Sfx: the close arm", '        } else if (w === "aureole-close"){'),
 ("Sfx: the shared rune-crack fallback", "        } else {                                        // rune-crack"),
 ("picture fields", "    this.beneFade = 0;"),
 ("tickPresentation", "  tickPresentation(dt){"),
 ("the picture's call", "    this.tickBenediction(dt);"),
 ("tickBenediction(dt){", "  tickBenediction(dt){"),
 ("the world pass call", "    if (__world) this.drawBenediction(m);"),
 ("drawBenediction(m){", "  drawBenediction(m){"),
 ("drawMotes(m){", "  drawMotes(m){"),
 ("ULTSIG aureole", "  aureole(c, t, cf, P){"),
 ("retired: the lit ground (comment)", "    /* ---- Benediction's lit ground was the BEAM's"),
 ("retired: the lance (comment)", "    /* ---- Benediction's lance and its rings were the BEAM's"),
 ("b12.5: drawUltUnder aureole", "    /* ---- Benediction: the lit ground under the blessing"),
 ("b12.5: drawUltOver aureole", "    /* ---- Benediction: sent OUT, not called down"),
 ("fx SPECS.aureole (inline)", "    aureole: { mode: 'beam', n: 1350,"),
]
for name in ("sc-aureole-b12.5-fx.html", "sc-aureole-b12.5.html"):
    s = (L / name).read_text(encoding="utf-8")
    print(f"== {name}")
    for lab, needle in NEED:
        n = s.count(needle)
        if not n:
            print(f"  {lab:38s} -")
            continue
        i = s.find(needle)
        ln = s.count("\n", 0, i) + 1 + (1 if needle.startswith("\n") else 0)
        print(f"  {lab:38s} {ln:6d}" + (f"   ({n}x)" if n > 1 else ""))
