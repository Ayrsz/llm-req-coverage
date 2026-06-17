# Fault: fronteira/off-by-one (exige margem de +1 na comparacao de frequencia).
# Um vencedor com frequencia maior por exatamente 1 nao e selecionado.
def most_frequent(items: list) -> str:
    if not items:
        return ""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    best = items[0]
    best_count = counts[best]
    for item, count in counts.items():
        # Off-by-one: deveria ser 'count > best_count'.
        if count > best_count + 1:
            best = item
            best_count = count
    return best
