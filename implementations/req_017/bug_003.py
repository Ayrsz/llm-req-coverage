def filter_by_tag(bookmarks: list, tag: str) -> list:
    # bug_003 (ramo/retorno trocado): acumula as tags em vez do título.
    if not tag:
        return []
    target = tag.lower()
    result = []
    for bm in bookmarks:
        tags = [t.lower() for t in bm.get("tags", [])]
        if target in tags:
            result.append(bm.get("tags"))
    return result
