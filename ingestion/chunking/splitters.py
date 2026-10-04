import re 

SEPARATORS = ["\n\n", "\n", ". ", " ", ""]
ITEM_START = re.compile(r"^(-|\d+\.)\s")        # top-level "- " or "1. ", widen it for real document
MAX_ITEMS = 5


def recursive_split(text, size=100, separators=SEPARATORS):
    if len(text) <= size:
        return [text]
    sep, *rest = separators
    if sep == "":
        return [text[i:i+size] for i in range(0, len(text), size)]   # hard cut, last resort

    pieces = text.split(sep)
    parts = [p + sep for p in pieces[:-1]] + [pieces[-1]]   

    out, buf = [], ""
    for p in parts:
        candidate = buf + p if buf else p

        if len(candidate) <= size:
            buf = candidate
        else:
            if buf:
                out.append(buf)
            buf = p if len(p) <= size else ""
            if len(p) > size:
                out.extend(recursive_split(p, size, rest))   # still too big → next separator
    if buf:
        out.append(buf)
    return out


def split_items(list_text):
    """list block -> items; indented lines (nested bullets) join the item above"""
    items = []
    for line in list_text.split("\n"):
        if ITEM_START.match(line):
            items.append(line)
        elif line.strip() and items:
            items[-1] += "\n" + line
    return items


def group_items(items, max_items=MAX_ITEMS):
    if len(items) <= max_items + 1:                 # short list -> keep whole
        return [items]
    return [items[i:i + max_items] for i in range(0, len(items), max_items)]


def parse_md_table(text):
    """markdown table -> list of row dicts"""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    split = lambda l: [c.strip() for c in l.strip("|").split("|")]
    header = split(lines[0])
    return [dict(zip(header, split(l))) for l in lines[2:]]      # skip --- line


def row_to_text(row, title):
    first, *rest = row.items()                                   # first column = row label
    pairs = ", ".join(f"{k}: {v}" for k, v in rest)
    return f"{title} — {first[1]}: {pairs}"