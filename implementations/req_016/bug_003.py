def most_visited_urls(visits: list, n: int) -> list:
    # bug_003 (ramo/retorno trocado): desempate pela ÚLTIMA aparição (-first_seen)
    # em vez da primeira.
    if n <= 0:
        return []
    counts = {}
    first_seen = {}
    for i, url in enumerate(visits):
        if url not in counts:
            counts[url] = 0
            first_seen[url] = i
        counts[url] += 1
    ranked = sorted(counts, key=lambda u: (-counts[u], -first_seen[u]))
    return ranked[:n]
