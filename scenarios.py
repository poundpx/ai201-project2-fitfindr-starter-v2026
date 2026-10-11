"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # Criterion 1: a query the data can match
        "name": "matching query completes",
        "query": "adidas track jacket under $90",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # Criterion 2: a query nothing can match. The branch
        "name": "impossible query stops early",
        "query": "miku helmet size xxxl under $100",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Diagnostic: a user with nothing saved. Not one of the five criteria.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Criterion 3: same item id in session, suggest_outfit and create_fit_card
        "name": "state: same item id throughout",
        "query": "h&m comfy pant under $40",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: fit card is 2-4 sentences and contains the item price
        "name": "fit card has price and 2-4 sentences",
        "query": "corduroy bucket hat under $20",
        "wardrobe": "example",
        "criterion": 4,
    },
    # Criterion 5: five different queries with a max price, three also with a size.
    {"name": "price filter: dragonball sweat pant", "query": "dragonball sweat pant under $30",
     "wardrobe": "example", "criterion": 5},
    {"name": "price+size filter: graphic tee", "query": "graphic tee size L under $30",
     "wardrobe": "example", "criterion": 5},
    {"name": "price+size filter: crewneck", "query": "crewneck sweatshirt size XL under $25",
     "wardrobe": "example", "criterion": 5},
    {"name": "price filter: slip dress", "query": "silk slip dress under $40",
     "wardrobe": "example", "criterion": 5},
    {"name": "price+size filter: platform sneakers", "query": "platform sneakers size 8 under $50",
     "wardrobe": "example", "criterion": 5},
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
