# Fault: ramo/retorno trocado (retorna o item de MENOR frequencia).
def most_frequent(items: list) -> str:
    if not items:
        return ""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    best = items[0]
    best_count = counts[best]
    for item, count in counts.items():
        if count < best_count:
            best = item
            best_count = count
    return best
