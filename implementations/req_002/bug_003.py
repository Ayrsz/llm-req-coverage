# Fault: regra ausente (não exige dígito).
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    return has_upper and has_lower and has_symbol
