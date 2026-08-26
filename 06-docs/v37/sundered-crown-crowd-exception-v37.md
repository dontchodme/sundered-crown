# THE DIRECTOR AND THE CROWD — and the fix was not the one that was obvious

**2026-08-20, v37 round 8. HANDOFF STATE.**

> *"the director currently seems to go off the majority of the time triplicate
> is active... it can still trigger during a big exchange but it needs to know
> to only look for big exchanges compared to the average triplicate."*

# 1. THE COMPLAINT, MEASURED FIRST

50 matches over five foes, `director_diag.py`:

```
  28% of the fight is inside a Triplicate window
  64% of every cut lands there
  4.78 cuts a minute inside against 1.04 outside   ->  4.59x
```

Rate, not count — a raw count would flatter whichever side had more seconds.

# 2. THE OBVIOUS FIX WAS WRONG AND THE MEASUREMENT SAID SO

A SCORE bar: hold crowded beats to a percentile of their own window. Built it.
**It moved the rate by nothing. 4.59x, to the digit.** Twice.

A change that moves *nothing* is louder than one that moves the wrong thing, so
the next step was to ask why rather than reach for a bigger percentile:

```
  crowded   n=673  mean 0.45  med 0.24  p95 1.56  | >= floor  2.2%
  ordinary  n=637  mean 0.48  med 0.31  p95 1.59  | >= floor  2.2%
```

**THE CROWD DOES NOT SCORE HIGHER.** Identical to two decimal places. The
ultimate produces MORE moments, not BIGGER ones — 2.7x the beats per second.
**No level can thin a population that differs only in rate.**

# 3. WHERE THE CUTS ACTUALLY COME FROM

Only **0.3 single hits a fight** clear the bar, yet 47 of 73 cuts land inside a
window. It is `cineVolleys`, which groups consecutive contacts:

```
  cut to        volley [in] 26 · KILL [in] 18 · volley [out] 15 · hit [out] 9
  volleys       inside   91, median 5 blows   sizes 3:22 4:20 5:11 ... 15:2
                outside  37, median 3 blows   sizes 3:21 4:13 5:1 6:2
```

**Outside a summon, an exchange IS three blows** — 34 of 37 are 3 or 4, which is
what `volleyMin: 3` was tuned to mean. Inside a window, three blows is a lull.

So the exception is not a score. It is **the definition of "exchange"**.

# 4. WHAT SHIPPED

```js
  o.crowd = this.shades.length > 0;        // on every beat, in beat()
  crowdVolleyMin: 8,                       // CINE, next to volleyMin: 3
  const need = (crowdMin && run.some(b => b.crowd)) ? crowdMin : min;
```

Judged on the RUN, not the match. Swept on the number the exception can move —
the kill is exempt and 12-18 of the in-window cuts are kills:

```
  crowdVolleyMin    3(off)    6      7      8      9
  preference         3.07x  2.43x  2.01x  1.69x  1.59x
```

**8 taken.** The in-window median run is 5. **1.69x is not 1.00x and should not
be** — the ultimate does put more real spectacle on the floor; it just no longer
out-bids the rest of the fight three to one.

`engine_ab` still 1530/1530: `beats` is presentation data and the sim never
reads it, which is the check that says a director change stayed one.
