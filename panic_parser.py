import re


def extrair_resumo(conteudo: str) -> str:

    campos = import re


def extrair_resumo(conteudo: str) -> str:

    palavras_chave = [
        "bug_type",
        "product",
        "model",
        "os_version",
        "panicString",
        "panic(cpu",
        "Missing Sensor",
        "Missing sensor",
        "watchdog",
        "AOP",
        "RTKit",
        "SMC",
        "ANS",
        "I2C",
        "PCIe",
        "Baseband",
        "Thermal",
        "SEP",
        "Pearl",
        "paniclog",
        "userspace watchdog",
        "Debugger message",
        "Exception",
        "Faulting task"
    ]

    linhas = conteudo.splitlines()

    resumo = []

    encontrados = set()

    for linha in linhas:

        texto = linha.strip()

        if not texto:
            continue

        for palavra in palavras_chave:

            if palavra.lower() in texto.lower():

                if texto not in encontrados:
                    resumo.append(texto)
                    encontrados.add(texto)

                break

    # Mantém apenas o começo do log
    resumo.append("\n===== INÍCIO DO LOG =====\n")
    resumo.extend(linhas[:30])

    # Mantém apenas o final do log
    resumo.append("\n===== FINAL DO LOG =====\n")
    resumo.extend(linhas[-30:])

    return "\n".join(resumo)
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