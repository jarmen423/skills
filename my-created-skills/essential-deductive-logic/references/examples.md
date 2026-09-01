# Essential deductive logic — examples

Target shape only. Copy the structure, not the domain.

Each example is a re-phrase of a complex plan. The source review (file:line findings, test lists, production incidents, tool traces) is not the output.

## Shape

- Numbered causal chain. Each step is a premise or a deduction from earlier steps.
- Keep the domain nouns that carry the argument (`9155`, `Sold`, Redis, snapshot).
- Distinguish states that look alike (`Sold` vs `Ended` vs `Owned`).
- End with one sentence that is the whole argument.
- Do not include file:line, test lists, incident reports, “I did X”, or implementation recipes unless the recipe **is** the deduction.

## Short form (default)

User: *tell me the essential deductive logic your plan uses*

### Essential logic

1. **9155 is the right evidence.**
   It tells us that an exact `auctionId` moved into recent sales. No guessing from a missing search result and no extra EA calls.

2. **A Sold event alone is insufficient.**
   Events can be dropped, missed while disconnected, or forgotten after the row fades. A reconnect would then reload the old listing from `stream:auctions` and make Buy active again.

3. **Therefore Sold must become durable state, not merely an animation.**
   Redis should remember: “auction X is terminal” and “card Y now has these Q3/profit values.” Every new snapshot must check that state before showing a listing.

4. **Clients must remember terminal status separately from displayed rows.**
   Removing a Sold row must not erase the knowledge that it sold. Later deal updates cannot resurrect it.

5. **“Someone bought it,” “it expired,” and “I bought it” are different states.**
   - **Sold:** confirmed by 9155.
   - **Ended:** local timer reached zero; sale is unproven.
   - **Owned:** this user bought it; preserve the Sell flow.

   A later confirmed sale may upgrade Ended → Sold, but nothing should overwrite Owned.

6. **One card update should carry card data once.**
   Send one card-level message containing the latest Q3, profits, and sales history, plus the affected sold auction IDs. Do not repeat the same large tooltip data for every auction.

7. **Keep the existing architecture where it is already correct.**
   Use the existing 9155 polling and `/ws/deals/v2`. No second WebSocket, endpoint, service, public `/players` work, or extra EA traffic.

So the core deduction is:

> **The existing data source and WebSocket are correct; the missing piece is durable server and client state that prevents a transient event, reconnect, or late update from making a dead listing buyable again.**

## Long form (whole plan, start from a named path)

User: *tell me the essential deductive logic the whole plan is using. Start with how we accomplish acquiring and broadcasting known state changes for rows in the live deals table*

### 1. First acquire the identity of every row we actually show

When 9153 finds a profitable listing and publishes it to `stream:auctions`, we know:

- its exact `auctionId`;
- its `cardId` and market;
- when we observed it;
- approximately when it expires;
- that it was eligible to appear in the Live Deals table.

In the same atomic Redis operation as publishing the deal, we register that exact auction in a compact **surfaced-auction registry**.

That registry answers:

> “Which specific auctions have we put in front of customers?”

This is better than comparing two 9155 snapshots because it targets only rows we may need to update. It avoids broadcasting hundreds of thousands of irrelevant market sales and eliminates the first-snapshot flood problem.

### 2. Use 9155 to acquire confirmed state changes

Sales workers already poll 9155. Its recent-sales rows carry the same exact `auctionId`.

For each successful 9155 response:

1. Extract the recent auction IDs.
2. Look those IDs up in the surfaced-auction registry.
3. Any exact intersection means:

> “We showed this exact listing, and 9155 now identifies that exact listing as sold.”

No player-name matching, price matching, or inference from a listing disappearing from search.

The Sold transition does **not** depend on having a price. Price is optional metadata; exact auction identity is the evidence that retires Buy.

### 3. Acquire card-level changes at the same time

The same 9155 response contains the current sales history used to calculate:

- Q3 for each window;
- profit for each window;
- the sales-history tooltip.

We calculate one valuation fingerprint. If that fingerprint changed, the card has new market state—even if none of that client’s particular auctions sold.

So a single 9155 result may produce:

- one or more exact Sold auction IDs;
- a card valuation update;
- or both.

### 4. Persist the state transition atomically

One Redis Lua operation:

1. rechecks that the auction is still surfaced;
2. removes it from surfaced state;
3. writes a terminal Sold record;
4. updates the latest card valuation;
5. appends one card-market event to the lifecycle stream.

This prevents partial outcomes such as:

- remembering Sold but failing to broadcast;
- broadcasting Sold but leaving the auction live;
- two workers closing the same auction twice;
- a late 9153 result republishing an already-sold listing.

Repeated 9155 responses become harmless because an auction that has already moved to terminal state is no longer surfaced.

### 5. Broadcast through the existing v2 WebSocket

The realtime API reads the new central lifecycle stream and sends a new protobuf tag-6 payload through `/ws/deals/v2`.

One card-level message contains:

- card ID and market;
- Q3 and profit for all windows;
- sales-history data;
- repeated compact Sold auction IDs.

The card data appears once rather than being duplicated for every sold auction.

There is:

- no second WebSocket;
- no new endpoint for normal live delivery;
- no new EA traffic;
- no deal-capture/Postgres dependency.

### 6. Treat Redis state as truth and the stream as notification

A WebSocket event can be missed. Therefore the event itself cannot be the only record that an auction sold.

On every initial or replacement snapshot, the server:

1. reads candidate deals from `stream:auctions`;
2. removes locally expired rows;
3. checks their IDs against terminal Redis state;
4. excludes sold IDs;
5. then applies the customer’s normal filters.

Therefore, even if a browser missed the animation, reconnecting cannot make the dead listing buyable again.

Persisted Watchlist IDs can be reconciled over a bounded control message on the same socket—still no EA request and no permanent server-side tracking of what the customer has open.

### 7. Prioritize state corrections over new deals

Ordinary deal updates may be coalesced or dropped under pressure. A Sold transition cannot be silently discarded.

The revised transport rules are:

- coalesce ordinary updates by auction ID;
- coalesce card valuation updates by card/fingerprint;
- preserve every distinct Sold ID;
- process lifecycle updates first;
- if lifecycle delivery saturates, disconnect the slow client so it reconnects to a corrected snapshot.

A clean reconnect is safer than leaving a ghost Buy button.

### 8. Store lifecycle independently from rendered rows

Each client maintains:

- auction status keyed by `(market, auctionId)`;
- card valuation keyed by `(market, cardId)`.

The status is not stored only on the row component. Therefore fading and deleting the row does not delete the tombstone, and a later BatchUpdate cannot resurrect it.

### 9. Keep Sold, Ended, and Owned distinct

The state machine is:

- **Live:** currently buyable.
- **Ended:** local clock reached zero; a sale is not proven.
- **Sold:** 9155 confirmed the exact auction.
- **Owned:** this user successfully bought it.

Precedence:

> **Owned > Sold > Ended > Live**

Consequences:

- a later exact sale can upgrade Ended → Sold;
- a generic Sold broadcast cannot overwrite Owned;
- Owned preserves the existing Sell flow and `itemInstanceId`;
- Sold/Ended rows cannot be revived by stale deal updates.

### The central conclusion

> We learn which rows matter when we surface them, learn exact closures from 9155, atomically preserve those state changes in Redis, use the existing WebSocket for fast notification, and make both server snapshots and client reducers reconcile against durable state.

That gives us real-time animation when everything is healthy **and** correct behavior after dropped messages, reconnects, app restarts, races, or delayed 9155 polling.
