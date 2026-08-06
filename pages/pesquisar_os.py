def pesquisar_os(texto):

    consulta = supabase.table("ordens_servico").select("*")

    if texto.isdigit():
        resposta = consulta.eq("numero_os", int(texto)).execute()
        print("Pesquisa por número:", resposta.data)
        return resposta.data

    resposta = consulta.or_(
        f"cliente.ilike.%{texto}%,modelo.ilike.%{texto}%,contato.ilike.%{texto}%"
    ).execute()

    print("Pesquisa por texto:", resposta.data)
    return resposta.data