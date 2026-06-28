---
name: x-algorithm
description: >
  Write high-engagement X posts and grow on X, grounded in the actual source code of
  xAI's open-source recommendation algorithm (github.com/xai-org/x-algorithm). Covers
  the Phoenix ranking model, weighted scoring signals, the banger/safety/spam content
  classifiers, retrieval mechanics, and the home-mixer pipeline. Use when the user asks
  to write, optimize, or strategize X/Twitter posts, grow an account, or understand how
  the X feed ranks content. ALWAYS cite specific code evidence when giving advice.
---

# X Algorithm Skill

Based on a line-by-line reading of **github.com/xai-org/x-algorithm** (the complete open-source release of X's recommendation system). Every claim below is grounded in specific source files from that repo.

---

## THE PIPELINE (How a Post Reaches the For You Feed)

The pipeline has **4 stages**, each with hard gates. A post must survive all four:

```
POST PUBLISHED
     │
     ▼
① CONTENT CLASSIFICATION (grox/)
   ├── Banger Initial Screen → quality_score ≥ 0.4? NO = dead on arrival
   ├── Safety/PTOS classifiers → policy violation? NO = suppressed
   ├── Spam detection → flagged? NO = buried
   └── Multimodal embedding generated (v5, 1024-dim)
     │
     ▼
② RETRIEVAL (Phoenix Two-Tower)
   ├── User history encoded → user embedding [128-dim, L2-normalized]
   ├── All eligible posts encoded → candidate embeddings
   └── Dot-product similarity → top ~200 candidates from millions
     │
     ▼
③ RANKING (Phoenix Transformer)
   ├── Transformer scores each candidate for 19 action types
   ├── Weighted sum of action probabilities = final score
   ├── Author diversity multiplier applied
   └── Out-of-network penalty applied
     │
     ▼
④ BLENDING & SELECTION (Home Mixer)
   ├── Ads blended in
   ├── "Who to Follow" module inserted
   ├── Dedup, age filter, seen-post filter
   └── Final feed served
```

**Source:** `home-mixer/candidate_pipeline/for_you_candidate_pipeline.rs`, `phoenix/README.md`, `grox/plans/plan_master.py`

---

## ① CONTENT CLASSIFICATION — THE GATEKEEPERS

Before a post can be ranked, it passes through multiple LLM classifiers. These are **hard gates** — fail one and your post is suppressed or buried.

### The Banger Initial Screen (`grox/classifiers/content/banger_initial_screen.py`)

This is the single most important classifier. A VLM (vision-language model) scores every non-reply post on:

- **`quality_score`** (0.0–1.0): The overall quality assessment
- **Threshold: `quality_score >= 0.4`** to pass (line 129: `banger_initial_positive = score >= 0.4`)
- Also produces: `slop_score`, `has_minor_score`, `is_image_editable_by_grok`, taxonomy categories, tags, description

**Only non-reply posts are screened** (`task_filters.py`, `TaskInitialBangerFilter`):
- Replies are SKIPPED for banger screening (line 344-349: `if post.ancestors: ... return False`)
- Private accounts are SKIPPED (line 368: `if post.user.is_protected: return "private_account"`)

**ACTIONABLE:** Original posts (not replies) are the only ones that get the full banger pipeline. If you want to be discovered by new audiences, post original content, not just replies.

### Safety/PTOS Classifiers (`grox/classifiers/content/safety_ptos.py`)

Seven policy categories are checked:
- ViolentMedia, AdultContent, Spam, IllegalAndRegulatedBehaviors, HateOrAbuse, ViolentSpeech, SuicideOrSelfHarm

Uses a two-tier system: standard VLM classifier → deluxe reasoning model for borderline cases. Policy violations = suppression.

### Spam Detection (`grox/classifiers/content/spam.py`, `grox/tasks/task_spam_detection.py`)

- **Only applies to replies** where the **parent/root post author has < 1000 followers** (`task_filters.py` lines 118-133)
- If either the reply target or root thread author has > `FOLLOWER_COUNT_THRESHOLD`, spam detection is **skipped** (the conversation is considered "high blast radius")
- Follower buckets tracked: ≤100, ≤500, ≤1000, >1000

**ACTIONABLE:** Reply spam detection only targets you when replying to smaller accounts. When you reply to large accounts (>1000 followers), your reply goes through reply ranking instead.

### Reply Ranking (`grox/classifiers/content/reply_ranking.py`)

- Uses a VLM to score replies 0-3
- **Only activates when parent or root author has followers ABOVE threshold** (`task_filters.py` lines 169-178)
- Below threshold = "low_blast_radius" → reply ranking is SKIPPED entirely
- Same-user replies (replying to your own thread) are excluded

**ACTIONABLE:** Replying to large accounts gets your reply ranked by an LLM. Make replies genuinely valuable — the LLM scores them.

### Post Embedding Generation (`grox/embedder/multimodal_post_embedder_v5.py`)

- Uses a 1024-dimensional embedding model
- **Multimodal**: processes text AND images together
- Video transcripts are appended to text before embedding
- Truncated to 1024 dims, L2-normalized
- Images extracted and embedded alongside text

**ACTIONABLE:** Your post's embedding determines whether it gets retrieved. The embedding captures text + images + video transcripts. Rich, descriptive posts with relevant images will match more user histories.

---

## ② RETRIEVAL — How Posts Are Found (Phoenix Two-Tower)

**Source:** `phoenix/recsys_retrieval_model.py`, `phoenix/run_pipeline.py`

### Architecture
- **User Tower**: Encodes user ID + last 127 actions (posts interacted with + actions taken + product surface) through a 4-layer, 128-dim transformer → L2-normalized user embedding
- **Candidate Tower**: Projects post embedding + author embedding through a 2-layer MLP (SiLU activation) → L2-normalized candidate embedding
- **Similarity**: Pure dot product (`user_repr · candidate_repr`). Top-K retrieved via approximate nearest neighbor search.

### What This Means for Creators
1. **Your post's embedding must be close to target users' history embeddings**. The model learns from what users have liked, replied to, reposted, dwelled on, and clicked.
2. **Author identity matters**: Author embeddings are concatenated with post embeddings in the candidate tower. Consistent author identity = more predictable embedding matching.
3. **Post age is a feature**: `POST_AGE_MAX_MINUTES = 4800` (~3.3 days). Post age is bucketed at 60-minute granularity and embedded as a feature. Older posts get different (likely lower) retrieval priority.
4. **Product surface is tracked**: Where the post appears (For You, Following, Topics) is embedded and used.

### The Action Types the Model Learns From (19 total)
From `phoenix/runners.py` lines 233-253 and `run_pipeline.py` lines 68-73:

| Index | Action | What It Means |
|-------|--------|---------------|
| 0 | favorite_score | Like |
| 1 | reply_score | Reply |
| 2 | repost_score | Repost |
| 3 | photo_expand_score | Expanding a photo |
| 4 | click_score | Clicking into the post |
| 5 | profile_click_score | **Clicking the author's profile** |
| 6 | vqv_score | **Video Quality View** |
| 7 | share_score | Share |
| 8 | share_via_dm_score | Share via DM |
| 9 | share_via_copy_link_score | Copy link |
| 10 | dwell_score | **Dwelling on the post** |
| 11 | quote_score | Quote post |
| 12 | quoted_click_score | Clicking a quoted post |
| 13 | follow_author_score | **Following the author from the post** |
| 14 | not_interested_score | ❌ Not interested |
| 15 | block_author_score | ❌ Block author |
| 16 | mute_author_score | ❌ Mute author |
| 17 | report_score | ❌ Report |
| 18 | dwell_time | Continuous dwell time |

### Continuous Actions (from `runners.py` lines 255-264)
| Index | Action |
|-------|--------|
| 0 | reserved |
| 1 | dwell_time |
| 2 | video_watch_time |
| 3 | scroll_depth |

---

## ③ RANKING — The Weighted Scoring Formula

**This is the heart of the algorithm.** Source: `home-mixer/scorers/ranking_scorer.rs` and `home-mixer/scorers/weighted_scorer.rs`

### The Scoring Formula

The Phoenix model outputs probability predictions for all 19 actions. The final score is a **weighted linear combination**:

```
score = Σ (probability_of_action × weight_for_action)
```

From `ranking_scorer.rs` lines 146-170, the positive signals are:
```
favorite × FavoriteWeight
+ reply × ReplyWeight
+ retweet × RetweetWeight
+ photo_expand × PhotoExpandWeight
+ click × ClickWeight
+ profile_click × ProfileClickWeight
+ vqv × VqvWeight  (only if video > MIN_VIDEO_DURATION_MS)
+ share × ShareWeight
+ share_via_dm × ShareViaDmWeight
+ share_via_copy_link × ShareViaCopyLinkWeight
+ dwell × DwellWeight
+ quote × QuoteWeight
+ quoted_click × QuotedClickWeight
+ quoted_vqv × QuotedVqvWeight
+ dwell_time × ContDwellTimeWeight
+ click_dwell_time × ContClickDwellTimeWeight
+ follow_author × FollowAuthorWeight
```

Negative signals (subtracted):
```
- not_interested × NotInterestedWeight
- block_author × BlockAuthorWeight
- mute_author × MuteAuthorWeight
- report × ReportWeight
- not_dwelled × NotDwelledWeight
```

### The Demo Weights (from `run_pipeline.py` lines 355-360)

The pipeline demo uses these concrete weights to compute the final ranking score:

```python
weighted = (
    p_favorite × 1.0      # LIKES are the #1 signal
    + p_reply × 0.5       # Replies matter significantly
    + p_repost × 0.3      # Reposts are valuable but weighted less than likes
    + p_dwell × 0.2       # Dwell time is a meaningful signal
)
```

**Note:** These are the *demo* weights in the open-source pipeline. Production weights are configurable via feature switches (`ScoringWeights::from_params`) and are not published. However, the **relative ordering** in the demo is instructive:
- **Likes are worth 2× replies, 3.3× reposts, 5× dwell**
- All signals are positive and additive — more engagement of ANY type helps

### The Negative Score Offset (`ranking_scorer.rs` lines 175-183)

If the combined score goes negative (negative signals outweigh positive), it's mapped to a small negative range:
```rust
if combined_score < 0.0 {
    (combined_score + negative_sum) / total_sum × NEGATIVE_SCORES_OFFSET
} else {
    combined_score + NEGATIVE_SCORES_OFFSET
}
```
This means negative feedback (blocks, mutes, reports, "not interested") can push a post's score below zero, but the penalty is bounded.

### Author Diversity Multiplier (`ranking_scorer.rs` lines 186-217)

The algorithm actively prevents any single author from dominating a feed:

```rust
fn diversity_multiplier(decay_factor, floor, position) -> f64 {
    (1.0 - floor) × decay_factor^position + floor
}
```

- Sort candidates by score
- For each author, their **Nth post** in the feed gets multiplied by `diversity_multiplier(decay, floor, N)`
- The first post from an author gets full score. The second gets `decay × score + floor × score`. Third gets `decay² × score + floor × score`. And so on.
- The `floor` parameter ensures the multiplier never reaches zero (it asymptotes to `floor`)

**ACTIONABLE:** Posting 5 times in rapid succession doesn't give you 5× the feed presence. The 2nd through 5th posts are heavily discounted in any single feed load. **Spread posts across time** so each gets its own feed request with full multiplier.

### Out-of-Network (OON) Penalty (`ranking_scorer.rs` lines 220-238, `oon_scorer.rs`)

Posts from accounts the user doesn't follow get their score **multiplied by `OON_WEIGHT_FACTOR`** (a value < 1.0):

```rust
let final_score = match c.in_network {
    Some(false) => after_diversity × effective_oon,
    _ => after_diversity,
};
```

**Special cases:**
- If the user has **topic_ids** (browsing a topic), the `TopicOonWeightFactor` is used instead
- **New users** get a special `NEW_USER_OON_WEIGHT_FACTOR` (likely higher, to help them discover content)
- New user eligibility: account age < `NewUserAgeThresholdSecs` AND following ≥ `NEW_USER_MIN_FOLLOWING`

**ACTIONABLE:** Your content faces a penalty when shown to non-followers. This penalty is offset by having a high engagement score. You need disproportionately strong engagement signals to break through to non-followers.

### The VM Ranker — DPP for Diversity (`vm_ranker.rs`)

An alternative ranker that supports **Determinantal Point Processes (DPP)**:
- `dpp_theta` and `dpp_max_selected_rank` parameters
- DPP is a mathematical method for selecting diverse subsets — it actively penalizes redundant/similar content
- Also receives `is_retweet` and `is_reply` flags, plus `author_followers_count`
- **Viewer's following count** is sent to the ranker (`viewer_following_count`)

**ACTIONABLE:** The ranker explicitly knows how many followers you have, whether the post is a reply or retweet, and applies diversity-aware re-ranking. Original posts from your account are treated differently than retweets.

---

## ④ FILTERS & PIPELINE GATES

### Age Filter (`age_filter.rs`)
Posts older than `max_age` duration are removed. X is a recency-heavy platform.

### Previously Seen Posts Filter (`previously_seen_posts_filter.rs`)
Uses **Bloom filters** + client-sent `seen_ids` to prevent showing the same post twice. Related post IDs (quotes, ancestors) are also checked.

**ACTIONABLE:** Once a user has seen your post, they won't see it again. Each impression is precious.

### Dedup Filters
- `dedup_conversation_filter.rs` — prevents multiple posts from the same conversation
- `retweet_deduplication_filter.rs` — dedupes retweets of the same original post
- `drop_duplicates_filter.rs` — general dedup

### Video Filter (`video_filter.rs`)
Only active when `exclude_videos` is set (user preference/device constraint). Videos with `min_video_duration_ms` set are filtered out.

### Tweet Type Metrics Hydrator (`tweet_type_metrics_hydrator.rs`)

The system tags every candidate with a **bitset** of type flags that influence scoring:
- RETWEET, REPLY, SUBSCRIPTION_POST, HAS_ANCESTORS, IN_NETWORK
- VIDEO, VIDEO_LTE_10_SEC, VIDEO_BT_10_60_SEC, VIDEO_GT_60_SEC
- TWEET_AGE_LTE_30_MINUTES, TWEET_AGE_LTE_1_HOUR, TWEET_AGE_LTE_6_HOURS, TWEET_AGE_LTE_12_HOURS, TWEET_AGE_GTE_24_HOURS
- AUTHOR_FOLLOWERS_0_100, 100_1K, 1K_10K, 10K_100K, 100K_1M, 1M_PLUS
- EMPTY_REQUEST, NEAR_EMPTY, SERVED_SIZE_LESS_THAN_20/10/5

**ACTIONABLE:** Your follower count bucket is explicitly tracked and used as a feature. The algorithm treats posts from 1M+ follower accounts differently than 100-follower accounts. Video duration buckets (≤10s, 10-60s, >60s) are explicitly tracked — mid-length videos (10-60s) are a distinct category.

---

## THE PHOENIX MODEL ARCHITECTURE (Deep Technical Details)

**Source:** `phoenix/recsys_model.py`, `phoenix/grok.py`, `phoenix/README.md`

### Ranking Model
- **Architecture**: Transformer (ported from Grok-1), adapted for recommendations
- **Mini config**: 128-dim embeddings, 4 layers, 4 attention heads, key_size=32
- **Production**: Larger model with more layers and wider embeddings (not released)
- **History**: 127 most recent actions
- **Candidates**: Up to 64 scored simultaneously per batch

### Candidate Isolation Masking
A critical design choice: **candidates cannot attend to each other**. Each candidate is scored independently based on the user + history context. This means:
- Your post's score depends ONLY on: the viewer's identity, their history, and your post's features
- It does NOT depend on what other posts are in the same batch

### Right-Anchored RoPE Positions
The model uses Rotary Position Embeddings where the newest history token always gets a fixed position. This means **recent interactions are weighted more heavily** in the attention mechanism.

### Multi-Action Output
The model outputs `[batch, num_candidates, 19]` — probabilities for all 19 action types simultaneously, plus `[batch, num_candidates, 8]` continuous predictions (dwell time, video watch time, scroll depth, etc.).

### Training
- **Continuously trained** on real-time engagement data
- The released checkpoint is a **frozen snapshot** from that continuous training
- Trained on actual X engagement signals

---

## ACTIONABLE PLAYBOOK: Optimizing for the X Algorithm

### 1. ENGAGEMENT HIERARCHY (what to optimize for, in priority order)

Based on the demo weights and scoring structure:

| Priority | Signal | Weight (demo) | How to get it |
|----------|--------|---------------|---------------|
| 1 | **Likes** | 1.0 | Make posts that trigger immediate positive emotion |
| 2 | **Replies** | 0.5 | Ask questions, share controversial-but-safe takes |
| 3 | **Reposts** | 0.3 | Make posts people want to associate with their identity |
| 4 | **Dwell time** | 0.2 | Long-form text, threads, compelling images that make people stop |
| 5 | **Profile clicks** | — | Create curiosity about who you are |
| 6 | **Follow from post** | — | Deliver value that makes people want more |
| 7 | **Shares (DM/copy link)** | — | Make content worth sending to specific people |
| 8 | **Video quality views** | — | Post engaging video content (VQV requires minimum duration) |
| 9 | **Quote posts** | — | Create content that sparks commentary |

**Negative signals to AVOID at all costs:**
- "Not Interested" clicks (weight: heavy negative)
- Block author (weight: heavy negative)
- Mute author (weight: heavy negative)
- Report (weight: heavy negative)
- Not dwelling (implied negative)

### 2. CONTENT STRATEGY RULES

**A. Post original content, not just replies.**
The banger initial screen only runs on non-reply posts. Original posts get quality scored, safety checked, embedded, and entered into the retrieval corpus. Replies only go through reply ranking (which requires the parent author to be large enough).

**B. The first 30 minutes are critical.**
The age filter and age buckets show the system explicitly tracks: ≤30min, ≤1hr, ≤6hr, ≤12hr, ≥24hr. Posts get their strongest retrieval in the first 30 minutes. If they don't get engagement in that window, they decay.

**C. Video length matters in specific buckets.**
The system categorizes videos as ≤10s, 10-60s, or >60s. VQV (Video Quality View) only counts if video duration > `MIN_VIDEO_DURATION_MS`. Short, punchy videos that hold attention for their full duration maximize VQV probability.

**D. Dwell time is tracked as both binary AND continuous.**
The model predicts both `dwell_score` (did they dwell?) and `dwell_time` (how long?). Content that makes people stop scrolling and actually read/watch is scored positively. Long threads, compelling images, and video transcripts all increase dwell.

**E. Images are embedded multimodally.**
The v5 embedder processes text AND images together. Posts with relevant, high-quality images get richer embeddings that match more user histories in retrieval.

**F. Your author identity is part of the embedding.**
Author embeddings are concatenated with post embeddings in both the candidate tower (retrieval) and the ranking model. Consistent posting in your niche builds a stronger, more recognizable author embedding.

### 3. TIMING & FREQUENCY

**A. Don't rapid-fire posts.**
The author diversity multiplier decays your 2nd, 3rd, 4th post in a single feed load. Post across different feed refresh cycles.

**B. Post when your audience is active.**
The user action sequence hydrator (`user_action_seq_query_hydrator.rs`) captures each user's recent actions. If your followers are active, their recent history will include content similar to yours, boosting your retrieval score.

**C. New users get a different algorithm config.**
New accounts (age < threshold, following ≥ min) get a different OON weight factor and potentially different retrieval/ranking clusters. The algorithm actively tries to help new users discover content.

### 4. WHAT GETS YOU SUPPRESSED

**A. Low banger quality score (< 0.4).**
The VLM judges your post quality. Low quality = not entered into recommendation pipeline.

**B. Safety/PTOS violations.**
Any of the 7 policy categories = suppression. The system uses both standard and "deluxe" reasoning models for enforcement.

**C. Spam classification on replies.**
If you reply to smaller accounts (< 1000 followers) with spammy content, the spam classifier flags you.

**D. Negative feedback signals.**
Users clicking "Not Interested", blocking, muting, or reporting your posts directly reduce your score through the negative weight terms.

**E. Being too similar to yourself.**
The DPP ranker and author diversity scorer both penalize redundant content. Don't post the same thing rephrased.

### 5. THE RETRIEVAL ADVANTAGE

Retrieval is where discovery happens for non-followers. Your post embedding is compared against every user's history embedding via dot product. To maximize retrieval:

**A. Post in a consistent niche.**
Users who have engaged with similar content will have history embeddings close to yours. Consistency = stronger embedding signal.

**B. Use relevant imagery.**
Multimodal embeddings capture image content. Relevant images expand your embedding's match surface.

**C. Write descriptively.**
The embedding model processes your full post text (up to 4096 chars). Rich, descriptive posts create more nuanced embeddings.

**D. Post fresh.**
Post age is a feature in the embedding. The retrieval corpus is time-windowed. Fresh posts get priority in the retrieval corpus.

---

## THE GROX CONTENT PIPELINE (Processing Flow)

**Source:** `grox/plans/plan_master.py`, `grox/engine.py`

Every post goes through these parallel plans:

1. **PlanInitialBanger** — Quality screening + content understanding
2. **PlanPostSafety** — Safety policy checks
3. **PlanSpamComment** — Spam detection (replies to small accounts only)
4. **PlanPostEmbeddingWithSummary** — Generate post summary + embedding (original posts only)
5. **PlanPostEmbeddingWithSummaryForReply** — Embedding for replies
6. **PlanPostEmbeddingV5** — Multimodal v5 embedding (original posts)
7. **PlanPostEmbeddingV5ForReply** — Multimodal v5 embedding (replies)
8. **PlanReplyRanking** — LLM-based reply quality scoring (replies to large accounts)
9. **PlanSafetyPtos** — Detailed safety policy enforcement

All plans run **in parallel** (`asyncio.gather`) and results are merged. This means all classifiers see your post simultaneously.

---

## KEY FILE REFERENCE

| File | What It Reveals |
|------|----------------|
| `phoenix/recsys_model.py` | Ranking transformer, action types, post age bucketing, scoring head |
| `phoenix/recsys_retrieval_model.py` | Two-tower retrieval, candidate tower, ANN search |
| `phoenix/run_pipeline.py` | **Demo scoring weights** (like=1.0, reply=0.5, repost=0.3, dwell=0.2) |
| `phoenix/grok.py` | Transformer architecture, attention masking, RoPE positions |
| `phoenix/runners.py` | All 19 action types listed, ranking output structure |
| `home-mixer/scorers/ranking_scorer.rs` | **Full weighted scoring formula**, diversity, OON penalty |
| `home-mixer/scorers/weighted_scorer.rs` | Alternative scorer with same signal weights |
| `home-mixer/scorers/oon_scorer.rs` | Out-of-network penalty |
| `home-mixer/scorers/vm_ranker.rs` | VM ranker with DPP diversity, follower count feature |
| `home-mixer/scorers/author_diversity_scorer.rs` | Author diversity multiplier math |
| `grox/classifiers/content/banger_initial_screen.py` | **Quality score threshold = 0.4** |
| `grox/tasks/task_filters.py` | **Eligibility gates** for every classifier |
| `grox/classifiers/content/spam.py` | Spam detection for low-follower replies |
| `grox/classifiers/content/reply_ranking.py` | Reply scoring by VLM |
| `grox/embedder/multimodal_post_embedder_v5.py` | 1024-dim multimodal embedding |
| `home-mixer/filters/age_filter.rs` | Age-based removal |
| `home-mixer/candidate_hydrators/tweet_type_metrics_hydrator.rs` | Follower buckets, video duration buckets, age buckets |
| `home-mixer/candidate_pipeline/for_you_candidate_pipeline.rs` | Full pipeline assembly |

---

## CITATION FORMAT

When advising on X strategy, always cite the source:
- "The banger quality threshold is 0.4 (`banger_initial_screen.py` line 129)"
- "Demo weights: likes=1.0, replies=0.5, reposts=0.3, dwell=0.2 (`run_pipeline.py` lines 355-360)"
- "Author diversity decays your Nth post in a feed (`ranking_scorer.rs` lines 186-217)"
- "Out-of-network posts are penalized by a multiplicative factor (`ranking_scorer.rs` lines 272-275)"
