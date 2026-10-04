import re


CODE = re.compile(r"```.*?```", re.DOTALL)


def protect_code(text):
    """swap code blocks for placeholders so their # lines aren't seen as headings"""
    blocks = CODE.findall(text)
    for i, b in enumerate(blocks):
        text = text.replace(b, f"<<CODE_{i}>>", 1)
    return text, blocks

def restore_code(text, blocks):
    return re.sub(r"<<CODE_(\d+)>>", lambda m: blocks[int(m.group(1))], text)

