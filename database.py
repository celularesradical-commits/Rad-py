from supabase import create_client
from datetime import datetime
from zoneinfo import ZoneInfo


# ===========================
# CONFIGURAÇÃO SUPABASE
# ===========================

SUPABASE_URL = "https://hqbdzacpolmeqicowjws.supabase.co"
SUPABASE_KEY = "sb_publishable_UOEeboBVGq6Ysnn28YbsPg_YgBo5B4p"

supabase = 

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


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
        "data_entrada": datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).isoformat(),
        "data_retirada": str(retirada),
        "observacoes": observacoes,
        "status": "Em andamento"
    }

    (
        supabase.table("ordens_servico")
        .insert(dados)
        .execute()
    )

    return numero


# ===========================
# PESQUISAR ORDEM
# ===========================

def pesquisar_os(texto):

    consulta = (
        supabase.table("ordens_servico")
        .select("*")
    )

    if texto.isdigit():

        consulta = consulta.eq(
            "numero_os",
            int(texto)
        )

    else:

        consulta = consulta.or_(
            f"cliente.ilike.%{texto}%,"
            f"modelo.ilike.%{texto}%,"
            f"contato.ilike.%{texto}%"
        )

    resposta = consulta.execute()

    return resposta.data


# ===========================
# BUSCAR UMA OS
# ===========================

def buscar_os(numero):

    resposta = (
        supabase.table("ordens_servico")
        .select("*")
        .eq("numero_os", numero)
        .limit(1)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None


# ===========================
# EDITAR ORDEM
# ===========================

def editar_os(
    numero,
    valor,
    observacoes,
    retirada
):

    (
        supabase.table("ordens_servico")
        .update({
            "valor": float(valor),
            "observacoes": observacoes,
            "data_retirada": str(retirada)
        })
        .eq(
            "numero_os",
            numero
        )
        .execute()
    )


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

    momento_entrega = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).isoformat()

    (
        supabase.table("ordens_servico")
        .update({
            "status": "Entregue",
            "data_entrega": momento_entrega
        })
        .eq(
            "numero_os",
            numero
        )
        .execute()
    )

    return True