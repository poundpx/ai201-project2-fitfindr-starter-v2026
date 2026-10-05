"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re
from utils.data_loader import load_listings  # check the real name in the stub
import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
   # --- search_listings body ---
    stop = {"a", "an", "the", "under", "size", "in", "for", "and", "with", "i", "want"}
    keywords = [w for w in re.findall(r"[a-z0-9']+", description.lower()) if w not in stop]

    scored = []
    for item in load_listings():
        if max_price is not None and item["price"] > max_price:
            continue
        if size is not None:
            tokens = re.findall(r"[a-z0-9]+", item["size"].lower())
            if size.lower() not in tokens:
                continue
        text = " ".join([item["title"], item["description"], item["category"],
                         " ".join(item["style_tags"])]).lower()
        score = sum(1 for k in keywords if k in text)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda p: -p[0])  # stable sort, so ties keep file order
    return [item for _, item in scored][:config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    # --- suggest_outfit body ---
    items = wardrobe.get("items", [])
    base = f"Item: {new_item['title']} (${new_item['price']}, size {new_item['size']}, colors {', '.join(new_item['colors'])})."
    if not items:
        prompt = (base + " The user has no wardrobe on file. Give one or two general outfit "
                  "ideas for this item, naming typical pieces that would go with it. Keep it short.")
    else:
        owned = "\n".join(f"- {i}" for i in items)
        prompt = (base + f"\nThe user already owns:\n{owned}\n"
                  "Suggest one or two outfits that combine this item with specific pieces "
                  "from that list. Name the pieces. Keep it short.")
    return generate(prompt)

# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
   # --- create_fit_card body ---
    if not outfit or not outfit.strip():
        return "No outfit ideas were available, so a fit card could not be written."
    prompt = (f"Write a 2 to 4 sentence social media caption about a thrift find: "
              f"{new_item['title']}, ${new_item['price']} on {new_item['platform']}. "
              f"Outfit ideas: {outfit}\n"
              "Sound like a real person posting, not a product description. "
              "Mention the item, price and platform once each, and be specific about the vibe.")
    return generate(prompt)
