# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.


<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user types what they want in plain language, for example 'vintage graphic tee under $30, size M'. FitFindr pulls out the price limit and the size, searches the listings, and picks the best-scoring match. It then asks the model for outfit ideas that combine that item with pieces from the user's wardrobe, and writes a short social caption for the find. If nothing matches, it stops and tells the user what to change instead of calling the other tools.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings in `data/listings.json` for items that match the user's keywords, keeps only those that fit the size and price limit, and ranks them by how many keywords they match.
- **Inputs:** `description` (str) is the keywords, e.g. "vintage graphic tee". Filler words like "a", "the" and "under" are ignored. `size` (str or None) is a size such as "M"; None means no size filter. `max_price` (float or None) is the price ceiling; None means no price filter.
- **Returns:** A list of listing dicts (id, title, description, category, style_tags, size, condition, price, colors, brand, platform), best match first. Score = number of keywords found in the listing's title, description, category and style_tags; a score of 0 is dropped. Size matches when the user's size equals one whole word of the listing's size ("M" matches "S/M" but not "XL" or "US 9"). Price matches when price <= max_price (inclusive). At most `config.SEARCH_RESULT_LIMIT` results.
- **When it has nothing:** Returns an empty list `[]`, never None and never an exception. The loop branches on this.

### `suggest_outfit`

- **What it does:** Asks the model to mix the newly found item with pieces the user already owns and suggest one or two outfits.
- **Inputs:** `new_item` (dict, one listing from search_listings), `wardrobe` (dict with an `items` list, each item a dict with id, name, category, colors, style_tags, notes).
- **Returns:** A non-empty string of outfit ideas that name specific wardrobe pieces.
- **When it has nothing:** If the wardrobe is empty (`{"items": []}`), it still returns a non-empty string of general styling advice for the item. It never returns `""` or None.

### `create_fit_card`

- **What it does:** Asks the model to write a short caption about the find, the kind of thing someone would post.
- **Inputs:** `outfit` (str, the text from suggest_outfit), `new_item` (dict, one listing).
- **Returns:** A caption string of 2 to 4 sentences that mentions the item (and its price and platform) and the outfit idea.
- **When it has nothing:** If `outfit` is empty or only whitespace, it skips the model and returns a short message string saying no fit card could be written because there were no outfit ideas. It never raises.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that tells the user what to change (remove the size, raise the price, or use fewer or different keywords, with an example), leave `session["fit_card"]` as None, and return without calling `suggest_outfit` or `create_fit_card`. Otherwise take the first result as `session["selected_item"]` and go on to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. The price comes from a `$N` pattern and the size from "size X". Whatever is left of the query becomes the description. If a price or size is missing, that value is None and search_listings skips that filter.

**What moves through the session:** `parsed` (description, size, max_price) → `search_results` → `selected_item` (the first result) → `outfit_suggestion` → `fit_card`. Each tool reads its input back out of the session. On an empty search, `error` is set and `fit_card` stays None.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* i using claude to generalize me the flow of each element to understand code struction
- *What came back:* clear structure and explanation of everything but its usually overload
- *What I changed:* targeting each part and element instead of over load understanding everything at once

**Moment 2**

- *What I asked for:* generate other project to learn applying my skill so i can have better understand of this current project
- *What came back:* clean everything but some part is still hard to understand or hard to apply to real world scenario
- *What I changed:* be more specific with claude before transform project from 1 subject to another with different requirement or better planning

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

Produced by `python run_eval.py --label before` (`results/run_2026-10-10_2140_before.md`),
cache off, 5 tries per scenario, 90 model calls in total. Each try was marked PASS or
FAIL by hand against the rule in `criteria.md`.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools (`adidas track jacket under $90`) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool (`miku helmet size xxxl under $100`) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Same item id in session, `suggest_outfit` and `create_fit_card` (`h&m comfy pant under $40`) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card is 2-4 sentences and has the price (`corduroy bucket hat under $20`) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every result within the price ceiling and size (5 queries) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Note on an earlier run: my first full run (`results/run_2026-10-10_2132.md`, no label) used
`miles morale adidas under $90` for criterion 1. No listing contains those words, so all
5 tries stopped at the empty branch. It had only worked by hand because `90$` was not
parsed as a price, so the stray `90` matched `90s` in a listing title. Two criterion 5
queries in that run also returned `[]`, which passes a price/size check without testing
it. I replaced those three queries with ones that match real listings and re-ran. That is
a fix to the test inputs; the criteria and targets were not changed.

**Real output from one try per criterion**

Criterion 1: `agent.py::run_agent` and `tools.py::create_fit_card`, query `adidas track jacket under $90`, try 1:

```
[1] search_listings (via MCP)
      in:  description='adidas track jacket under', size=None, max_price=90.0
      out: 4 items: 90s Track Jacket - Navy/White Stripe, Denim Jacket - Light Wash, Cropped, 90s Leather Bomber - Black + 1 more
[2] suggest_outfit
      in:  item='90s Track Jacket - Navy/White Stripe', item_id=lst_004, wardrobe_items=10
[3] create_fit_card
      in:  item='90s Track Jacket - Navy/White Stripe', item_id=lst_004, ...

Fit card: Scored this gorgeous navy and white striped 90s track jacket for just $45 on Poshmark and I'm obsessed. I'm planning to wear it two ways: super casual for daytime with baggy dark-wash denim and chunky sneakers, or dressed up a bit with wide-leg khaki trousers and combat boots. It's the ultimate sporty-meets-chic piece for that effortless retro vibe!
```

Criterion 2: `agent.py::run_agent`, the `if not session["search_results"]` branch, query `miku helmet size xxxl under $100`, try 1:

```
[1] search_listings (via MCP)
      in:  description='miku helmet   under', size=xxxl, max_price=100.0
      out: [] (empty)
[2] branch: empty search
      ->   stopping, suggest_outfit not called

No listings matched 'miku helmet   under' in size xxxl under $100. Try removing the size, raising your max price, or using fewer or different keywords (for example 'denim jacket' instead of 'distressed light-wash denim jacket').
```

Criterion 3: `agent.py::run_agent`, query `h&m comfy pant under $40`, try 1. The same `item_id=lst_005` (Corduroy Wide-Leg Pants, the first search result and `session["selected_item"]`) reached both tools:

```
[2] suggest_outfit
      in:  item='Corduroy Wide-Leg Pants - Rust', item_id=lst_005, wardrobe_items=10
[3] create_fit_card
      in:  item='Corduroy Wide-Leg Pants - Rust', item_id=lst_005, outfit='Here is an outfit combining the new rust'
```

Criterion 4: `tools.py::create_fit_card`, query `corduroy bucket hat under $20`, try 1 (3 sentences, contains `$14`):

```
Score this reversible brown plaid bucket hat for just $14 on thredUp and I'm honestly obsessed. It's giving major 90s indie sleaze whether I'm throwing it on with baggy denim for a chill coffee run or styling it over an oversized crewneck with combat boots. Such a good little secondhand win!
```

Criterion 5: `tools.py::search_listings`, checked directly (no model, so all 5 tries are identical). Every returned (price, size) is within the ceiling, and the size is a whole word of the listing size:

```
dragonball sweat pant under $30        -> Low-Rise Cargo Pants (27.0, W29), Oversized Crewneck Sweatshirt (20.0, XL (fits oversized))
graphic tee size L under $30           -> Graphic Tee (24.0, L), Vintage Band Tee (19.0, L), Vintage Graphic Hoodie (26.0, L)
crewneck sweatshirt size XL under $25  -> Oversized Crewneck Sweatshirt (20.0, XL (fits oversized)), Oversized College Crewneck (21.0, XL)
silk slip dress under $40              -> 90s Silk Slip Dress (30.0, M), Leather Belt (12.0, One Size (adjustable)), Vintage Linen Blazer (38.0, M/L), Silk Button-Down (28.0, M)
platform sneakers size 8 under $50     -> Platform Sneakers (48.0, US 8)
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All 5 tries of `adidas track jacket under $90` reached a fit card with no early stop. 5 passes is above the target of 4. |
| 2 | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | All 5 tries of `miku helmet size xxxl under $100` stopped at the empty branch with a message naming what to change. The trace has no suggest_outfit step and there were 0 model calls. |
| 3 | Same item id throughout | 5 of 5 | MET (5/5) | The trace showed `item_id=lst_005` in both suggest_outfit and create_fit_card in all 5 tries of `h&m comfy pant under $40`, and lst_005 is the first search result. |
| 4 | Fit card has 2-4 sentences and the price | 4 of 5 | MET (5/5) | All 5 fit cards for `corduroy bucket hat under $20` had 3 sentences and contained "$14". |
| 5 | Results respect price and size | 5 of 5 | MET (5/5) | All 5 queries returned only listings at or under the price ceiling, with sizes matching as whole words. Search has no randomness, so the 5 tries were identical. |

**Diagnoses**

No criterion was missed, so there is no miss to trace to a tool, branch, session or model. I am not reporting a clean sheet, though. Testing showed two real weaknesses that my criteria did not catch:

1. **The loop's query parsing.** `agent.py::run_agent` only reads a price written as `$30`. When I typed `30$`, `90$` or `100$` in manual runs, the price was ignored, `max_price` stayed `None`, and the stray token stayed in the description. "over $60" is not supported at all, since the tool only has a ceiling.
2. **The tool's keyword matching.** `tools.py::search_listings` counts a keyword as matched if it appears anywhere in the text. `h&m comfy pant` became the keywords `h`, `m`, `comfy`, `pant`, and the letters `h` and `m` match almost every listing, so the search returned 33 matches. The same effect made `miles morale adidas 90$` seem to work in my first run: `90` matched `90s` in a title.

These two are the same kind of problem. Both are in how my agent handles the query text before the model gets involved. The two model-written steps (outfit and fit card) never missed.

My first full run (`results/run_2026-10-10_2132.md`) also showed that a test can pass for the wrong reason: criterion 1 used a query that matched no listing, and two criterion 5 queries returned nothing, which satisfies a price/size check without testing it. I replaced those queries and re-ran. The criteria and targets were not changed.

**Were my targets too easy?** Yes, for most of them. Criteria 2, 3 and 5 test plain code with no randomness, so 5 of 5 was nearly guaranteed. Criterion 1 only asks whether a result exists, not whether it is relevant: the loosely matched track jacket counted as a pass. Only criterion 4 depends on the model, and it passed with sentence counts of 2 to 4, close to the 4-sentence limit on a few tries. If I tighten one target, it is criterion 1: the top result's title or tags should contain at least one keyword from the query.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** one line in `tools.py::search_listings`. Keywords shorter than 3 characters are now ignored when the description is split up: `if w not in skip:` became `if w not in skip and len(w) >= 3:`. Nothing else changed in this step.

**Which failure it was meant to fix:** the tool's loose keyword matching (see Verdicts and Diagnoses). A keyword counts as matched if it appears anywhere in a listing's text, so one- and two-letter tokens such as the `h` and `m` from `h&m`, or a stray `90`, match almost everything. Before the change, `h&m comfy pant under $40` matched 33 listings (the search returned the cap of 10), most of them not pants.

### Run Log: After

Produced by `python run_eval.py --label after` (`results/run_2026-10-10_2155_after.md`), cache off, 5 tries per scenario, same scenarios as the before run.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Same item id in session, suggest_outfit and create_fit_card | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card is 2-4 sentences and has the price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every result within the price ceiling and size | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Real output, criterion 3 scenario (`h&m comfy pant under $40`), `agent.py::run_agent`, after the change. The search now returns 2 items and the same `item_id=lst_005` still reaches both tools:

```
[1] search_listings (via MCP)
      in:  description='h&m comfy pant under', size=None, max_price=40.0
      out: 2 items: Corduroy Wide-Leg Pants - Rust, Low-Rise Cargo Pants - Khaki
[2] suggest_outfit
      in:  item='Corduroy Wide-Leg Pants - Rust', item_id=lst_005, wardrobe_items=10
[3] create_fit_card
      in:  item='Corduroy Wide-Leg Pants - Rust', item_id=lst_005, ...
```

**Did it help, and how do I know:** It helped in the way I aimed at, but my five criteria cannot show it. The pass counts are 5/5 on every row both before and after, so the table is unchanged. The evidence is the search step for `h&m comfy pant under $40`: before, `search_results` was 10 (33 matches, capped); after, it is 2 (Corduroy Wide-Leg Pants and Low-Rise Cargo Pants, the actual pants). The first result, the selected item and every other scenario stayed the same, so nothing got worse. The honest limit is that this changed relevance on one query. It did not touch the larger problem that any single matching keyword counts, so `adidas track jacket` still returns a denim jacket and a bomber alongside the track jacket.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
