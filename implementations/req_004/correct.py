def bmi_category(weight: float, height: float) -> str:
    # Guarda de entrada: altura não positiva ou peso negativo são inválidos.
    if height <= 0 or weight < 0:
        return "invalido"
    bmi = weight / (height * height)
    # Faixas da OMS, fronteiras fechadas à esquerda.
    if bmi < 18.5:
        return "abaixo"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "sobrepeso"
    return "obesidade"
