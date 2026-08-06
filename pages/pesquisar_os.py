def pesquisar_os(texto):

    resposta = (
        supabase.table("ordens_servico")
        .select("*")
        .execute()
    )

    dados = resposta.data

    texto = str(texto).strip().lower()

    resultados = []

    for os in dados:

        if (
            texto == str(os.get("numero_os", "")).lower()
            or texto in str(os.get("cliente", "")).lower()
            or texto in str(os.get("modelo", "")).lower()
            or texto in str(os.get("contato", "")).lower()
        ):
            resultados.append(os)

    return resultados