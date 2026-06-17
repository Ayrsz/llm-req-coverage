# Fault: guarda ausente — não apara os hifens das pontas (strip removido).
# "-already-slug-" permanece com hifens nas bordas.
import unicodedata


def slugify(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    no_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = no_accents.lower()
    result = []
    for ch in lowered:
        if ch in (" ", "_"):
            result.append("-")
        elif ("a" <= ch <= "z") or ("0" <= ch <= "9") or ch == "-":
            result.append(ch)
    slug = "".join(result)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug
