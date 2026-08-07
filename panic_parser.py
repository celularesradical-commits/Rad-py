import json
import re


def extrair_resumo(conteudo: str) -> str:

    campos = {
        "product": "",
        "model": "",
        "os_version": "",
        "bug_type": "",
        "panicString": "",
        "Debugger message": "",
    }

    termos_tecnicos = [
        "Missing Sensor",
        "Missing Sensors",
        "userspace watchdog",
        "watchdog timeout",
        "AOP PANIC",
        "RTKit",
        "SMC",
        "ANS",
        "I2C",
        "PCIe",
        "Baseband",
        "Thermal",
        "SEP",
        "Pearl",
        "!pulse",
    ]

    linhas_tecnicas = []
    encontrados = set()

    # ===========================
    # TENTAR LER O CABEÇALHO JSON
    # ===========================

    linhas = conteudo.splitlines()

    if linhas:

        primeira_linha = linhas[0].strip()

        try:
            cabecalho = json.loads(primeira_linha)

            campos["product"] = str(
                cabecalho.get("product", "")
            ).strip()

            campos["model"] = str(
                cabecalho.get("model", "")
            ).strip()

            campos["os_version"] = str(
                cabecalho.get("os_version", "")
            ).strip()

            campos["bug_type"] = str(
                cabecalho.get("bug_type", "")
            ).strip()

        except (json.JSONDecodeError, TypeError):
            pass

    # ===========================
    # EXTRAÇÃO DOS CAMPOS
    # ===========================

        padroes = {
        "product": [
            r'"product"\s*:\s*"([^"]+)"',
            r"\bproduct\s*[:=]\s*([^\n,}]+)",
        ],
        "model": [
            r'"model"\s*:\s*"([^"]+)"',
            r"\bmodel\s*[:=]\s*([^\n,}]+)",
        ],
        "os_version": [
            r'"os_version"\s*:\s*"([^"]+)"',
            r"\bos_version\s*[:=]\s*([^\n,}]+)",
        ],
        "bug_type": [
            r'"bug_type"\s*:\s*"?([^",}\n]+)"?',
            r"\bbug_type\s*[:=]\s*([^\n,}]+)",
        ],
        "panicString": [
            r'"panicString"\s*:\s*"((?:\\.|[^"\\])*)"',
            r"\bpanicString\s*[:=]\s*(.+)",
        ],
        "Debugger message": [
            r"Debugger message\s*[:=]\s*(.+)",
        ],
    }

    for campo, lista_padroes in padroes.items():

        if campos.get(campo):
            continue

        for padrao in lista_padroes:

            resultado = re.search(
                padrao,
                conteudo,
                re.IGNORECASE
            )

            if resultado:

                valor = resultado.group(1).strip()

                valor = (
                    valor
                    .replace("\\n", " ")
                    .replace("\\r", " ")
                    .replace("\\t", " ")
                    .replace('\\"', '"')
                )

                valor = re.sub(
                    r"\s+",
                    " ",
                    valor
                ).strip()

                campos[campo] = valor
                break

    # ===========================
    # LINHAS TÉCNICAS IMPORTANTES
    # ===========================

    for linha in linhas:

        texto = linha.strip()

        if not texto:
            continue

        texto_normalizado = re.sub(
            r"\s+",
            " ",
            texto
        ).strip()

        for termo in termos_tecnicos:

            if termo.lower() in texto_normalizado.lower():

                chave = texto_normalizado.lower()

                if chave not in encontrados:

                    encontrados.add(chave)

                    # Evita adicionar o arquivo inteiro
                    if len(texto_normalizado) > 500:
                        texto_normalizado = texto_normalizado[:500]

                    linhas_tecnicas.append(
                        texto_normalizado
                    )

                break

    # ===========================
    # MONTAR RESUMO FINAL
    # ===========================

    resumo = []

    resumo.append("===== RESUMO TÉCNICO =====")

    if campos["product"]:
        resumo.append(
            f"product: {campos['product']}"
        )

    if campos["model"]:
        resumo.append(
            f"model: {campos['model']}"
        )

    if campos["os_version"]:
        resumo.append(
            f"os_version: {campos['os_version']}"
        )

    if campos["bug_type"]:
        resumo.append(
            f"bug_type: {campos['bug_type']}"
        )

    if campos["Debugger message"]:
        resumo.append(
            f"Debugger message: "
            f"{campos['Debugger message']}"
        )

    if campos["panicString"]:
        resumo.append(
            f"panicString: "
            f"{campos['panicString']}"
        )

    if linhas_tecnicas:

        resumo.append("")
        resumo.append(
            "Informações técnicas encontradas:"
        )

        for linha in linhas_tecnicas[:20]:

            # Não repetir linhas já exibidas
            if (
                campos["panicString"]
                and linha.lower()
                in campos["panicString"].lower()
            ):
                continue

            resumo.append(
                f"- {linha}"
            )

    if len(resumo) == 1:

        resumo.append(
            "Nenhuma informação técnica "
            "relevante foi encontrada."
        )

    resumo.append(
        "===== FIM DO RESUMO ====="
    )

    return "\n".join(resumo)