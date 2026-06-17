# Aplica uma sequência de comandos a um contador, com piso em 0.
# Comando desconhecido ignorado; contador nunca fica abaixo de 0.


def apply_commands(start: int, commands: list) -> int:
    counter = start
    for command in commands:
        if command == "inc":
            counter += 1
        elif command == "dec":
            # Piso em 0: nunca decrementa abaixo de zero.
            if counter > 0:
                counter -= 1
        elif command == "double":
            counter *= 2
        elif command == "reset":
            counter = 0
        # Comando desconhecido: ignorado.
    return counter
