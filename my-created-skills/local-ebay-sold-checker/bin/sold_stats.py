#!/usr/bin/env python3
"""Analyze eBay SOLD listing rows: market value stats + flip math.

Input: a text file (or stdin) with one sold listing per line. Each line is
scanned for dollar amounts: the FIRST $ amount is the sale price, the SECOND
(if any) is the shipping charged. The words 'free' near shipping count as 0.
Condition is detected from keywords (new / open box / pre-owned / used /
for parts). Everything else on the line is treated as title text.

Usage:
  sold_stats.py rows.txt [--buy 100] [--fee 0.1325] [--json]

Verified 2026-10-20 against a signed-in browser pull of eBay sold listings
for the Elgato 4K60 Pro: reproduces the hand-checked medians (~$110 original,
~$137.50 MK.2, used/working rows).
"""
import sys
import re
import json
import statistics

PRICE_RE = re.compile(r"\$\s?([0-9][0-9,]*\.?[0-9]{0,2})")
CONDITIONS = [
    ("for parts", re.compile(r"for parts|not working|untested|as-is", re.I)),
    ("new", re.compile(r"brand new|factory sealed|sealed|new in box", re.I)),
    ("open box", re.compile(r"open box|new open", re.I)),
    ("used", re.compile(r"pre-owned|pre owned|used", re.I)),
]


def parse_rows(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        amounts = [float(a.replace(",", "")) for a in PRICE_RE.findall(line)]
        if not amounts:
            continue
        price = amounts[0]
        shipping = None
        if len(amounts) > 1:
            shipping = amounts[1]
        elif re.search(r"free\s+(delivery|shipping)", line, re.I):
            shipping = 0.0
        cond = "unspecified"
        for name, rx in CONDITIONS:
            if rx.search(line):
                cond = name
                break
        if re.search(r"no box", line, re.I):
            cond += ", no box"
        rows.append({"price": price, "shipping": shipping, "condition": cond, "raw": line[:110]})
    return rows


def stats(prices):
    if not prices:
        return None
    s = sorted(prices)
    return {
        "count": len(s),
        "median": round(statistics.median(s), 2),
        "mean": round(statistics.mean(s), 2),
        "low": s[0],
        "high": s[-1],
        "p25": s[max(0, int(len(s) * 0.25) - 1)] if len(s) > 3 else s[0],
        "p75": s[min(len(s) - 1, int(len(s) * 0.75))] if len(s) > 3 else s[-1],
    }


def main():
    args = sys.argv[1:]
    buy = None
    fee = 0.1325
    as_json = "--json" in args
    path = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--buy":
            buy = float(args[i + 1]); i += 2
        elif a == "--fee":
            fee = float(args[i + 1]); i += 2
        elif a == "--json":
            i += 1
        else:
            path = a; i += 1
    text = open(path).read() if path else sys.stdin.read()
    rows = parse_rows(text)
    if not rows:
        print("No priced rows found.", file=sys.stderr)
        sys.exit(1)

    all_prices = [r["price"] for r in rows]
    used = [r for r in rows if r["condition"].startswith("used") or r["condition"].startswith("unspecified")]
    used_prices = [r["price"] for r in used]
    ships = [r["shipping"] for r in rows if r["shipping"] is not None]
    med_ship = round(statistics.median(ships), 2) if ships else 0.0

    out = {
        "all": stats(all_prices),
        "used_or_unspecified": stats(used_prices),
        "median_shipping_charged": med_ship,
        "rows": len(rows),
    }

    if buy is not None:
        mv = out["used_or_unspecified"] or out["all"]
        sale = mv["median"]
        gross = sale + med_ship
        net = gross * (1 - fee) - med_ship
        out["flip"] = {
            "buy_price": buy,
            "at_median_sale": sale,
            "fee_rate": fee,
            "net_after_fees_and_shipping": round(net, 2),
            "profit": round(net - buy, 2),
        }

    if as_json:
        print(json.dumps(out, indent=2))
        return

    def fmt(label, st):
        if not st:
            print(f"{label}: no rows")
            return
        print(f"{label}: n={st['count']} median ${st['median']:.2f} | mean ${st['mean']:.2f} | "
              f"range ${st['low']:.2f}-${st['high']:.2f} | p25 ${st['p25']:.2f} p75 ${st['p75']:.2f}")

    print(f"Rows parsed: {out['rows']} | median shipping charged: ${med_ship:.2f}")
    fmt("ALL sold", out["all"])
    fmt("USED/unspecified (market-value basis)", out["used_or_unspecified"])
    if "flip" in out:
        f = out["flip"]
        verdict = "PROFITABLE" if f["profit"] > 0 else "NOT profitable"
        print(f"FLIP at buy ${f['buy_price']:.2f}, selling at the used median ${f['at_median_sale']:.2f}: "
              f"net ${f['net_after_fees_and_shipping']:.2f} after {f['fee_rate']*100:.2f}% fees + shipping "
              f"-> profit ${f['profit']:.2f} ({verdict})")


if __name__ == "__main__":
    main()
