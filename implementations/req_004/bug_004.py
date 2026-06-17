# Fault: constante/literal errado (limite 18.5 trocado por 17.5).
# Faixa "abaixo" encolhe; IMC entre 17.5 e 18.5 vira "normal".
def bmi_category(weight: float, height: float) -> str:
    if height <= 0 or weight < 0:
        return "invalido"
    bmi = weight / (height * height)
    if bmi < 17.5:
        return "abaixo"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "sobrepeso"
    return "obesidade"
