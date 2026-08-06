import re


def extrair_resumo(conteudo: str) -> str:

    campos = [
        "product",
        "model",
        "os_version",
        "kernel",
        "bug_type",
        "panicString",
        "panicString :",
        "panic(cpu",
        "Missing sensor",
        "Missing Sensor",
        "watchdog",
        "RTKit",
        "SMC",
        "ANS",
        "I2C",
        "PCIe",
        "Baseband",
        "Thermal",
        "SEP"
    ]

    resultado = []

    linhas = conteudo.splitlines()

    for linha in linhas:

        texto = linha.strip()

        for campo in campos:

            if campo.lower() in texto.lower():

                resultado.append(texto)

                break

    # adiciona as últimas 100 linhas do arquivo
    resultado.append("\n===== FINAL DO LOG =====\n")
    resultado.extend(linhas[-100:])

    return "\n".join(resultado)