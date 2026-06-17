# Fault: off-by-one na faixa de dígitos ('1' em vez de '0' como limite inferior).
# Descarta o dígito '0' (ex.: "Python 3.10" perde os zeros -> "python-31").
import unicodedata


def slugify(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    no_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = no_accents.lower()
    result = []
    for ch in lowered:
        if ch in (" ", "_"):
            result.append("-")
        elif ("a" <= ch <= "z") or ("1" <= ch <= "9") or ch == "-":
            result.append(ch)
    slug = "".join(result)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")
