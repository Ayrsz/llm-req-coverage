# Fault: off-by-one na fronteira de faixa (> 256 em vez de > 255).
# Aceita o octeto 256 como válido.
def is_valid_ipv4(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for octet in parts:
        if octet == "":
            return False
        if not all("0" <= ch <= "9" for ch in octet):
            return False
        if len(octet) > 1 and octet[0] == "0":
            return False
        if int(octet) > 256:
            return False
    return True
