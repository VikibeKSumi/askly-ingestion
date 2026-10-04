import re


def split_by_headers(text, max_level=3):
    """Split on markdown headers, keeping the heading path for each section."""
    pattern = re.compile(rf"^(#{{1,{max_level}}})\s+(.*)$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    sections, path = [], {}
    for i, m in enumerate(matches):
        level, heading = len(m.group(1)), m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        path = {k: v for k, v in path.items() if k < level}
        path[level] = heading

        if body:
            sections.append({
                "section": " > ".join(path[k] for k in sorted(path)),
                "text": body,
                "char_start": start,
            })
    return sections