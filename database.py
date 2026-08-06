from supabase import create_client
from datetime import datetime

# ===========================
# CONFIGURAÇÃO SUPABASE
# ===========================

SUPABASE_URL = "https://hqbdzacpolmeqicowjws.supabase.co"
SUPABASE_KEY = "sb_publishable_UOEeboBVGq6Ysnn28YbsPg_YgBo5B4p"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ===========================
# GERAR NÚMERO DA OS
# ===========================

def gerar_numero_os():
    resposta = (
        supabase.table("ordens_servico")
        .select("numero_os")
        .order("numero_os", desc=True)
        .limit(1)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]["numero_os"] + 1

    return 5001


# ===========================
# SALVAR ORDEM DE SERVIÇO
# ===========================

def salvar_os(
    modelo,
    defeito,
    valor,
    cliente,
    contato,
    retirada,
    observacoes
):

    numero = gerar_numero_os()

    dados = {
        "numero_os": numero,
        "modelo": modelo,
        "defeito": defeito,
        "valor": float(valor),
        "cliente": cliente,
        "contato": contato,
        "data_entrada": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_retirada": str(retirada),
        "observacoes": observacoes,
        "status": "Em andamento"
    }

    supabase.table("ordens_servico").insert(dados).execute()

    return numero


# ===========================
# PESQUISAR ORDEM
# ===========================

def pesquisar_os(texto):

    resposta = (
        supabase.table("ordens_servico")
        .select("*")
        .execute()
    )

    return resposta.data

# ===========================
# REPAROS EM ANDAMENTO
# ===========================

def reparos_em_andamento():

    resposta = (
        supabase.table("ordens_servico")
        .select("*")
        .eq("status", "Em andamento")
        .order("numero_os")
        .execute()
    )

    return resposta.data


# ===========================
# ENTREGAR APARELHO
# ===========================

def entregar_os(numero):

    supabase.table("ordens_servico").update(
        {"status": "Entregue"}
    ).eq(
        "numero_os", numero
    ).execute()