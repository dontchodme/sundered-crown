# 08-analytics — the TikTok read, 2026-08-19

Why this folder exists: the cold-open experiment was graded from TikTok's
summary metrics until this session, and the summary metrics were hiding the
thing that mattered. The per-second retention curves are fetchable, and they
are what turned "the card is probably expensive" into a number.

```
cold-open-read-2026-08-19.md        the read from summary metrics (v31)
retention-curves-2026-08-19.md      the per-second curves (v32) -- the one that matters
charts/*.html                       open in a browser; each has a data table toggle
code/*.py                           every number in the two notes, reproducible
```

## The instrument

TikTok Studio shows only "most viewers stopped watching at 0:0X". The curve is
served by the same endpoint the page already calls, from a logged-in session:

```js
const B = "https://www.tiktok.com/aweme/v2/data/insight/?locale=en&aid=1988"
        + "&app_name=tiktok_creator_center&device_platform=web_pc&channel=tiktok_web"
        + "&os=win&tz_name=America%2FLos_Angeles&tz_offset=-25200&type_requests=";
const get = async (id, kind) => fetch(
  B + encodeURIComponent(JSON.stringify([{insigh_type: kind, aweme_id: String(id)}])),
  {credentials: "include"}).then(r => r.json());

await get(AWEME_ID, "video_retention_rate_realtime");  // {timestamp:"3000", value:0.56}
await get(AWEME_ID, "video_info");                     // .statistics
```

`aweme_id`s are in the DOM of `/tiktokstudio/content` (`/7[56]\d{17}/`).

## The three findings, shortest form

1. **The cold open works, and only in second 2** — it cuts that second's
   departure rate from 0.298 to 0.158, and does nothing else. +44% average
   watch time, permutation p=0.008.
2. **The card is the cliff, and it travels with the card.** Card-first videos
   peak at second 2; cold opens, which raise it ~1.9s later, peak at second 4.
   Card-first videos lose 71-75% of the audience present when it appears.
   That is what `sc-scrunch` exists to fix.
3. **Zero shares across 2,563 views**, on all eight videos pulled. Retention is
   up 44% and reach has not moved, and this is the likeliest mechanical reason.

## A note on the code

`analyze.py`, `followup.py`, `curves.py`, `ceilings.py`, `hazard.py` and
`card3.py` are the versions whose numbers are quoted in the notes. Two earlier
cuts are NOT shipped and are named here so the record is complete: `card.py`
priced the card counterfactual against each video's own late-fight hazard,
which was too generous, and `card2.py` modelled "remove the card" as replacing
a zero-length window, so it reproduced the observed curve and reported +0% —
incoherently better than halving it. `card3.py` models removal as EXCISION,
which is what removing four seconds of frozen video actually is.
