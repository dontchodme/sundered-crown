# Next session — v31

**2026-08-19.** The session that made the relics glass vessels and the health a
liquid level. Everything below is on `02-chain/sc-liquid.html`
**`0277dc5fc464f8b0`**.

`01-live/sundered-crown.html` `51c9bf566f9eb679` **untouched.**

---

# 0. The one command

```
cd tools
python3 liquid_build.py --src ../02-chain/sc-health18.html --out ../02-chain/sc-liquid.html
```

One builder, no ordering constraint, because it is the last link. The
shippable JS is `04-experiments/_liquid_core.js`, shared with `liquid_lab.py`
so the standalone lab and the game cannot drift — edit the core, re-run the
builder, re-run `liquid_probe.py`.

# 1. What is in the tip that was not in v30

**THE VESSEL.** Every on-ball health visual is gone — the four-chunk arc gauge,
the ash husk, the ember, the drain tail, the stone fracture, the grain sprite —
replaced by a glass sphere holding a liquid whose level is its life. Per-school
substance driven off the affinity table: sanctified rings like a struck glass,
dwarven amber heaves once and stops. Curse became a frosted dead cap the liquid
can never reach; Sunder became conchoidal spall; death became the vessel
failing and its contents leaving.

Ten numbers of new state per relic, integrated on the simulation tick and read
by nothing in the simulation. `06-docs/LIQUID-NOTES.md` is the full record,
including the three measurements that changed the build and the two derivations
I got wrong before the probe caught them.

# 2. NEXT SESSION'S JOB

1. **Watch it at phone size, with sound.** Rick cut the graduations and then
   the fracture, both on the picture. The consequence is that damage is carried
   by the LEVEL and nothing else on the ball — one strong channel where v5 had
   six weak ones. That trade is defensible and it is not free, and it is now
   PERMANENT: the cracking-and-leaking version was built properly, fixed twice,
   rendered as a frame-for-frame A/B on the same seed, and turned down —
   *"think that settles it. im not interested in the cracking and leaking
   feature."* **Do not rebuild it to find out.** `06-docs/LIQUID-NOTES.md` §4b
   is the whole record, including the two real defects that only surfaced when
   the leak was finally exercised. If the level ever proves insufficient, the
   answer has to be something NEW.
2. **Measure a real handset.** Five sessions of visual work are unmeasured. The
   budget is ~6 ms at 165 Hz. +1.3% median in a GPU-less box is worth what it
   is worth.
3. **Decide the lifeline.** It was deliberately left alone and now speaks a
   different visual language from the balls. Two glass tubes holding the same
   substance at the same level is the obvious move.
4. **Shorts on the new tip — two exist now**, both `--no-intro`, no VO, all
   fight, and both picked so BOTH vessels end near empty (a fight the winner
   finishes at 80% cannot tell you whether a falling level reads):

   ```
   liquid-wm-v-axiom.mp4                 seed 3946016107  47.4s  Axiom ends 2%
   liquid-lastlight-v-grudgebearer.mp4   seed 2976898105  38.5s  thinnest v thickest
   liquid-CRACK-LEAK-wm-v-axiom.mp4      seed 3946016107  47.4s  the same fight with
                                                                 FRACTURE.on -- a true
                                                                 A/B against the first
   ```

   Not in the zip — see `06-docs/07-SHORTS-NOTE.md`. What is still unshot is a
   POSTING short: hook, card, VO, cold open. These two are instruments.

# 3. The pattern worth reusing

Build the look in a STANDALONE LAB against a fake hall before it goes near the
game, and share the actual shipping source between the two so they cannot
drift. Three of the last four visual passes shipped code that was correct and a
picture that was wrong; this one had four wrong pictures and all four were
killed on a contact sheet in the first twenty minutes, before any of it touched
`drawFighter`.

And: a probe whose `--selftest` deliberately breaks the thing it checks. Check
[1] here couples the liquid back into `move()` by 1e-6 and requires the check to
notice. It does — 35 of 36 matches.

# 4. The one piece of debt this session knowingly left

About 500 lines of rejected code still ship in the default build — `glassCracks`,
`drawGlassFracture`, `glassVents`, `tickDrips`, `drawDrips`, and the chip branch
of `glassPath` — all inert behind `FRACTURE.on = false`. This session deleted
`shellCracks` and `corePath` on exactly the argument that retired code is a trap,
so that is an inconsistency and it is a deliberate one.

The resolution is easy and was not done at handoff because it touches a verified
build: **`liquid_build.py --fracture on` can already regenerate every line of it**,
so the shipped HTML does not need to carry it. Teach the builder to omit the
blocks when the flag is off. `liquid_probe` check [12] toggles `FRACTURE.on` and
would need rewriting with it.

# 5. Still open, carried

`06-docs/LIQUID-NOTES.md` §6. sc-scflip decision · 24 free grid cells ·
`o.dark` · Nightfell silhouette · same-type tape ties · render.py wall-time
audio port · cinema director's unretracted 21.85ms phone regression · fireUlt
life-table `grudgebearer: 1.7` shadowed by the forge branch · `cineScore` still
cannot film an ultimate · the HUD spill · **a 2-D fracture has no probe** ·
**nothing spends Smite** · kokoro models are not in this seed.
