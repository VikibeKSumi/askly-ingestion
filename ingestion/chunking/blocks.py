
import re
from ingestion.chunking.code_blocks import restore_code
from ingestion.chunking.splitters import ITEM_START, recursive_split, split_items, group_items, parse_md_table, row_to_text

PLACEHOLDER = re.compile(r"^<<CODE_\d+>>$")

def line_kind(line, prev):
    """what type of block does this line belong to?"""
    s = line.strip()
    if not s:
        return prev                                  # blank line: stays with current block
    if PLACEHOLDER.match(s):
        return "code"
    if s.startswith("|"):
        return "table"
    if ITEM_START.match(line):
        return "list"
    if prev == "list" and line[:1].isspace():
        return "list"                                # indented line continues the list
    return "text"


def split_blocks(text):
    """section body -> [("text"|"list"|"table"|"code", str), ...] in order"""
    blocks, buf, kind = [], [], None
    for line in text.split("\n"):
        k = line_kind(line, kind)                   
        if k != kind and buf:
            blocks.append((kind, "\n".join(buf).strip()))
            buf = []
        kind = k
        buf.append(line)
    if buf:
        blocks.append((kind, "\n".join(buf).strip()))
    return [(k, b) for k, b in blocks if b]


def block_to_pieces(kind, block, code_blocks, prefix):
    if kind == "code":
        return [restore_code(block, code_blocks)]
    if kind == "table":
        return [row_to_text(row, prefix) for row in parse_md_table(block)]
    if kind == "list":
        return ["\n".join(g) for g in group_items(split_items(block))]
    return [p.strip() for p in recursive_split(block, size=500) if p.strip()]

