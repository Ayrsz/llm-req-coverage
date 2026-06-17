def filter_by_tag(bookmarks: list, tag: str) -> list:
    """Títulos dos bookmarks que possuem ``tag`` (exata, case-insensitive).

    Preserva a ordem; ``tag`` vazia → ``[]``.
    """
    if not tag:
        return []
    target = tag.lower()
    result = []
    for bm in bookmarks:
        tags = [t.lower() for t in bm.get("tags", [])]
        if target in tags:
            result.append(bm["title"])
    return result
