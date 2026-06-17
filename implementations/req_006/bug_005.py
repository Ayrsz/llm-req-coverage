# Fault: guarda ausente — não verifica zeros à esquerda.
# Aceita octetos como "01" ou "00" (ex.: "01.2.3.4").
def is_valid_ipv4(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for octet in parts:
        if octet == "":
            return False
        if not all("0" <= ch <= "9" for ch in octet):
            return False
        if int(octet) > 255:
            return False
    return True
