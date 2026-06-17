# Fault: regra ausente (não exige letra maiúscula).
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    return has_lower and has_digit and has_symbol
