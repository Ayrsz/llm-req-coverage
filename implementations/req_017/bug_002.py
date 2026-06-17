def filter_by_tag(bookmarks: list, tag: str) -> list:
    # bug_002 (operador errado): membership invertida (not in), retorna os que
    # NÃO têm a tag.
    if not tag:
        return []
    target = tag.lower()
    result = []
    for bm in bookmarks:
        tags = [t.lower() for t in bm.get("tags", [])]
        if target not in tags:
            result.append(bm["title"])
    return result
