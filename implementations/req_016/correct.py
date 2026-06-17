def most_visited_urls(visits: list, n: int) -> list:
    """Retorna as ``n`` URLs mais visitadas, por frequência decrescente.

    Desempate: ordem de primeira aparição em ``visits``. ``n <= 0`` → ``[]``.
    """
    if n <= 0:
        return []
    counts = {}
    first_seen = {}
    for i, url in enumerate(visits):
        if url not in counts:
            counts[url] = 0
            first_seen[url] = i
        counts[url] += 1
    # ordena por (frequência decrescente, primeira aparição crescente)
    ranked = sorted(counts, key=lambda u: (-counts[u], first_seen[u]))
    return ranked[:n]
