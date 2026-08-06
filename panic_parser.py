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
    encontrados = set()

    resumo.append("===== RESUMO TÉCNICO =====\n")

    for linha in linhas:

        texto = linha.strip()

        if not texto:
            continue

        # Ignora linhas enormes
        if len(texto) > 250:
            continue

        for secao in secoes:

            if secao.lower() in texto.lower():

                chave = secao.lower()

                # Apenas uma ocorrência por seção principal
                if chave in [
                    "product",
                    "model",
                    "os_version",
                    "bug_type",
                    "panicstring",
                    "debugger message"
                ]:

                    if chave in encontrados:
                        break

                    encontrados.add(chave)

                resumo.append(texto)
                break

    resumo.append("\n===== FIM DO RESUMO =====")

    return "\n".join(resumo)