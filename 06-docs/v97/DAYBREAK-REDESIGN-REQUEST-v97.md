# v97 — DAYBREAK, REDESIGNED BY RICK: A CIRCLE OF SUNLIGHT FROM THE POINT OF CONTACT. FOR COWORK TO PRICE — Code does not design (rule 0).

**Rick, 2026-09-27, after watching the built clip (`07-shorts/v97/daybreak-window.mp4`):**

> *"how about daybreak begins at a point of contact after a hit and grows in a circle from that
> point. lets also make the animation look more like sunlight glowing rather than the dul white.
> its also hard to tell what exactly it does by watching it"*

Asked who sets the new mechanic's numbers, **Rick chose: "Send it to Cowork."** This file carries
the request, what Code measured on the version he watched, and what Code needs back. It proposes
no numbers. Those are Cowork's to price and Rick's to rule on, and Code builds from the brief.

## 1. What Rick is asking for, in his words, and what stays his

- **The mechanic changes.** The dawn no longer rises as a horizontal line from the floor. It
  **begins at a point of contact after a hit and grows in a circle from that point.**
- **The picture:** "more like **sunlight glowing** rather than the dull white".
- **Legibility:** "it's also **hard to tell what exactly it does** by watching it".

## 2. What Code needs in the brief (the questions Rick's sentence leaves open)

Code will not answer these (rule 0), so the brief should settle each:
1. **Which contact.** The first blow Dawnbringer lands after the cast, any blow, or something
   else. What happens if no blow lands.
2. **The circle.** How fast it grows, how large it gets, and whether it stays where it began or
   moves (with the foe, with Dawnbringer).
3. **What it does.** To a foe inside it (the line's was smite +1 and 2 damage every 0.5s) and to
   Dawnbringer inside it (the line gave the caster nothing; the heal was Rick's flag, v86 §6).
4. **The window.** Still 8s, and how it ends (the line's reached the ceiling).
5. **The charge**, stated on the lab's clock. It is converted to the engine's at build time (the
   batch ruling below).
6. **The card** (72 characters) and anything about the picture the brief wants to fix. Rick's
   "sunlight glowing" is an art note, and Code picks the look on measurements under "you pick i
   overrule" unless the brief says otherwise.
7. **The blade**, if it moves off 10.4.

## 3. What Code measured on the version Rick watched (the line), for the pricing to start from

All on Chromium 151, DESKTOP-DERRAFT, the chain tip. Full record in
`dawnbringer-daybreak-build-v97.md`.
- **Built as v86 wrote it, at charge 14, the line version read 52.2%** at blade 10.4 (1320
  fights, two blocks) against the lab's arm B at 53.5%. The shipped sparks read 58.0%.
  Dawnbringer was 53.8% in verify.
- Per cast: 9.9 ticks, 19.8 damage; the foe was lit 59% of the window; 3.3 casts a fight.

## 4. Constraints the pricing will meet (all measured, all in the repo)

- **THE CHARGE IS THE GAME'S EQUIVALENT (Rick, 2026-09-27, the whole batch).** The lab's
  `ult_overlay.py` schedules casts on its own step clock, which counts hit-stop freezes. The
  engine charges only in unfrozen time, so the lab's 16 is the engine's ~14 (measured per
  fighter). Price on the lab as before and state the lab's number; Code converts. The same clock
  point applies to the WINDOW: the engine's window clock stops through a hit stop. A
  window-second runs a median 1.16s and p99 1.62s of match time.
- **THE PICTURE HAS A HISTORY HERE.** CLAUDE.md §4.1b is this relic's own: the old Daybreak
  corona ERASED the ball. §4.1c: "alpha is invisible to the bloom, reach is not". The v86 line
  was drawn as a world-pass WASH for exactly that reason, and measured with a bloom share of ~0
  and the balls' discs unchanged. The same wash in the emissive pass lifted +0.071, over the
  Harrowing's +0.0628. **"Sunlight glowing" is buildable, but the glow must be measured against
  the ball discs** (the v86 gate: arena-mean lift ≤ +0.02; Morningstar's: the disc ≤ 0.90).
  Code will measure it; the brief may set the bar.
- **ONE ultFx SLOT** (open item 25): window art must hang off the fighter or the match, and a
  circle that persists for seconds is drawn, not a SPECS field. The v86 cast burst was removed
  because it whitened the foe's disc to 0.87-0.91.
- **The engine rules the build will follow:** `apply`'s source is a side letter; a tick that
  KILLS files its own fatal beat; others file none unless the brief says so.

## 5. State while this is priced

- The line version is built and gated (`sc-daybreak-fx`, v97 §4) and **does not ship**. The app
  stays on `sc-leaf`. The link stays in the chain, and the circle is built as new stages on top
  of the chain tip, the way Corollary's later stages were.
- Code carries on with the batch's next builds (Morningstar, Ironwood, Portcullis) meanwhile.
