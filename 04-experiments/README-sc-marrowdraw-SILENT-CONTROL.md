# sc-marrowdraw-SILENT-CONTROL.html — a deliberately sabotaged build

Not a candidate. This is the NEGATIVE CONTROL for
`marrowdraw_relic_probe [10]`, kept for the reason 04-experiments exists:
several files in here are the control for a measurement rather than a variant
of the game.

The v42 bug is put back into the ult voice — `this.tone(...)`, a helper that
does not exist — so `SFX.play("ult", {w:"marrowdraw"})` throws inside `play`'s
own try/catch and the cast is silent.

    real build     cast renders audible, and its ring is inharmonic   PASS
    this file      cast renders a peak of exactly 0                   FAIL

That second row is the point: the check fails on a build where the sound is
broken while the Aegis control is untouched in both, so a PASS on the real
build means THIS RELIC'S branch ran — not merely that the audio system exists.

REGENERATE IT FROM THE TIP whenever the ult voice changes, or it stops being a
control for the code that actually ships.
