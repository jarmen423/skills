# eBay Sold Listings Checker

Fulfills skill #2 in Joshua's deal-finder-agent spec (jarmen423/deal-finder-agent,
skills/index.md): before recommending any used purchase or flip, check recent
eBay SOLD listings to establish real market value. Built 2026-10-20 after the
spec was found unbuilt on every machine and repo.

## The one rule

Value from SOLD prices, never asking prices. An item is worth what the last
~15 buyers actually paid for it, in matching condition.

## Workflow

1. **Sharpen the query before searching.** Sellers mistitle constantly.
   - Use the exact make + model + variant identifiers (e.g. "Elgato 4K60 Pro
     MK.2 10GAS9901", not "elgato capture card").
   - Split variants into SEPARATE checks whenever they carry different money
     (original 4K60 Pro vs MK.2: ~$110 vs ~$135 used median, Oct 2026). A
     blended median is a wrong answer.
   - Note look-alike different products to exclude on sight (Elgato "4K Pro"
     10GBK9901 is a newer, different card).

2. **Pull the sold rows.** eBay gates sold prices behind sign-in, and the
   public trackers are unreliable from here (130point returns 403 bot-wall;
   WatchCount is a JS app behind reCAPTCHA). The working route is a live
   browser task on the default profile, which holds Joshua's eBay session:
   - `browser.browse` task_id "new": search eBay with Sold items + Completed
     listings filters, sort "Ended Recently", collect the most recent ~15
     sold results per variant: price, shipping charged, condition, title,
     sale date.
   - If eBay asks for sign-in or a captcha, the browser handles the captcha;
     sign-in is Joshua's step (he signs in, hands control back). Never ask
     for his password.
   - Sold rows come back one per line: `$PRICE +$SHIPPING shipping CONDITION TITLE`.

3. **Run the numbers, don't eyeball them.**
   `bin/sold_stats.py rows.txt [--buy PRICE]`
   - Reports row count, ALL-sold median/mean/range, and the USED/unspecified
     median — the market-value basis (new/open-box rows inflate the ALL line;
     for-parts rows are excluded when their condition is stated).
   - `--buy PRICE` adds flip math: eBay final-value fee 13.25% on
     price+shipping, minus shipping-out at the median shipping charged.
     Profit is net of both. A flip that clears less than ~$25 rarely survives
     the trip + listing + shipping time — say so.
   - Row hygiene decides the median: drop mislabeled rows (wrong model in
     title), accessories, and geographic outliers before running. When a
     hand-check and the script disagree, the rows differ — find which.

4. **Report verdict-first.** Lead with the used median and, when a target buy
   price exists, the flip verdict (profitable / break-even / dead) with the
   net number. Condition caveats (no box, untested) change value ~10-20% —
   name them when the target listing has them.

## Known limits

- eBay sold history reaches back ~90 days in the web UI; thin markets may
  return fewer than 10 usable rows — report the count with the median.
- "Best offer accepted" rows show the asking price struck through, not the
  accepted price, on some result cards; drop rows whose price the pull could
  not see rather than guessing.
- The browser session can expire; if sold filters bounce to a login wall and
  Joshua is unavailable, report the check as blocked instead of substituting
  asking prices.

## Verified

2026-10-20, Elgato 4K60 Pro: browser pull (~30 sold rows) + this analyzer
reproduced the hand-checked medians — original used $110.00 (flip at $100 =
-$5.47, dead), MK.2 used $133.75 (flip at $100 = +$15.18, thin). Test rows:
the two listing sets in that night's session.
