# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
My search scores by keyword overlap, so a phrasing with no words in common with any listing title, description or tags can return nothing, and the model-written steps after it can occasionally fail or come back unusable. 4 of 5 allows one such miss; 5 of 5 would hide that risk.
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
This path never calls the model. It depends only on the empty-list check in agent.py::run_agent, and an impossible query returns [] every time, so any miss would be a bug in the branch, not randomness. That is why 5 of 5 is fair here when criterion 1 is not.
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

In a run that finds a match, the "id" of session["selected_item"] is the same as the "id" of the item that reached suggest_outfit and the "id" of the item that reached create_fit_card, in 5 of 5 tries.

**Why this target:**
Passing the item is plain dict assignment and reading, with no model and no randomness. If the ids ever differ it is a real bug in the loop, so I expect 5 of 5 and anything less is a failure to diagnose, not variance.

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

In a run that finds a match, the fit card is 2 to 4 sentences long and contains the item price (for example "$18"), in at least 4 of 5 tries.

**Why this target:**
The fit card comes from a model with TEMPERATURE 0.9, so the same input gives different words. My prompt asks for the price, but a model can drop it or write 5 sentences, so I allow one miss in five. 5 of 5 would be unfair to a nondeterministic tool, and 3 of 5 would let a caption that often forgets the price count as working.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

For 5 different queries that include a max price (at least two also include a size), every listing search_listings returns has price <= the max price and a size that contains the requested size as a whole word, in 5 of 5 tries.

**Why this target:**
The price and size filters are plain code in search_listings with no model, so the target is 5 of 5. The real risk is my size rule (the user size must equal a whole word of the listing size) and the inclusive price check; testing several queries is how I would catch an off-by-one or a wrong size match.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
