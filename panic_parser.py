def extrair_resumo(conteudo: str) -> str:

    secoes = [
        "product",
        "model",
        "os_version",
        "bug_type",
        "panicString",
        "Debugger message",
        "panic(cpu",
        "userspace watchdog",
        "watchdog",
        "Missing Sensor",
        "Missing sensor",
        "AOP",
        "RTKit",
        "SMC",
        "ANS",
        "I2C",
        "PCIe",
        "Baseband",
        "Thermal",
        "SEP",
        "Pearl"
    ]

    linhas = conteudo.splitlines()

    resumo = []

    resumo.append("===== RESUMO TÉCNICO =====\n")

    encontrados = set()

    for linha in linhas:

        texto = linha.strip()

        if not texto:
            continue

        for secao in secoes:

            if secao.lower() in texto.lower():

                if texto not in encontrados:
                    resumo.append(texto)
                    encontrados.add(texto)

                break

    resumo.append("\n===== FIM DO RESUMO =====")

    return "\n".join(resumo)