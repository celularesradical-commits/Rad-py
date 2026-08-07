import streamlit as st
from datetime import date, datetime
from zoneinfo import ZoneInfo

from database import supabase
from fotos import obter_url_foto


st.set_page_config(
    page_title="Agenda",
    page_icon="📅",
    layout="centered"
)

st.title("📅 Agenda")


# ===========================
# FILTRO
# ===========================

filtro = st.segmented_control(
    "Exibir retiradas",
    options=[
        "Todas",
        "Atrasadas",
        "Hoje",
        "Próximas"
    ],
    default="Todas"
)


# ===========================
# ENTREGAR APARELHO
# ===========================

def entregar_os(numero_os):

    try:

        momento_entrega = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).isoformat()

        (
            supabase.table("ordens_servico")
            .update({
                "status": "Entregue",
                "data_entrega": momento_entrega
            })
            .eq("numero_os", numero_os)
            .execute()
        )

        st.session_state["mensagem_agenda"] = (
            f"OS Nº {numero_os} entregue com sucesso."
        )

        st.rerun()

    except Exception as erro:

        st.error(
            f"Erro ao entregar a OS: {erro}"
        )


# ===========================
# MENSAGEM DE SUCESSO
# ===========================

if "mensagem_agenda" in st.session_state:

    st.success(
        st.session_state.pop("mensagem_agenda")
    )


# ===========================
# EXIBIR ORDEM DE SERVIÇO
# ===========================

def exibir_os(ordem, tipo):

    numero_os = ordem["numero_os"]

    with st.container(border=True):

        st.write(
            f"**🆔 OS:** {numero_os}"
        )

        st.write(
            f"**👤 Cliente:** "
            f"{ordem.get('cliente', '')}"
        )

        st.write(
            f"**📱 Modelo:** "
            f"{ordem.get('modelo', '')}"
        )

        st.write(
            f"**📅 Retirada:** "
            f"{ordem.get('data_retirada', '')}"
        )

        # ===========================
        # FOTO DA OS
        # ===========================

        try:

            url_foto = obter_url_foto(numero_os)

        except Exception:

            url_foto = None

        if url_foto:

            st.image(
                url_foto,
                caption=f"Foto da OS Nº {numero_os}",
                use_container_width=True
            )

        else:

            st.info(
                "📷 Nenhuma foto cadastrada."
            )

        # ===========================
        # BOTÕES
        # ===========================

        coluna_abrir, coluna_entregar = st.columns(2)

        with coluna_abrir:

            if st.button(
                "📄 Abrir OS",
                key=f"abrir_{tipo}_{numero_os}",
                use_container_width=True
            ):

                st.session_state["os_editar"] = numero_os

                st.switch_page(
                    "pages/editar_reparo.py"
                )

        with coluna_entregar:

            if st.button(
                "✅ Entregar",
                key=f"entregar_{tipo}_{numero_os}",
                use_container_width=True
            ):

                entregar_os(numero_os)


# ===========================
# BUSCAR ORDENS
# ===========================

hoje = date.today().isoformat()

try:

    resposta = (
        supabase.table("ordens_servico")
        .select("*")
        .eq("status", "Em andamento")
        .order("data_retirada")
        .execute()
    )

    lista = resposta.data or []

except Exception as erro:

    st.error(
        f"Erro ao carregar a agenda: {erro}"
    )

    lista = []


# ===========================
# SEPARAR ORDENS POR DATA
# ===========================

atrasadas = []
hoje_lista = []
proximas = []

for ordem in lista:

    data_retirada = ordem.get(
        "data_retirada"
    )

    if not data_retirada:
        continue

    data_retirada = str(
        data_retirada
    )[:10]

    if data_retirada < hoje:

        atrasadas.append(ordem)

    elif data_retirada == hoje:

        hoje_lista.append(ordem)

    else:

        proximas.append(ordem)


# ===========================
# QUANTIDADES
# ===========================

coluna_1, coluna_2, coluna_3 = st.columns(3)

with coluna_1:

    st.metric(
        "🔴 Atrasadas",
        len(atrasadas)
    )

with coluna_2:

    st.metric(
        "🟢 Hoje",
        len(hoje_lista)
    )

with coluna_3:

    st.metric(
        "⚪ Próximas",
        len(proximas)
    )


st.divider()


# ===========================
# ATRASADAS
# ===========================

if filtro in ["Todas", "Atrasadas"]:

    if atrasadas:

        st.subheader("🔴 Atrasadas")

        for ordem in atrasadas:

            exibir_os(
                ordem,
                "atrasada"
            )

    elif filtro == "Atrasadas":

        st.success(
            "Nenhuma retirada atrasada."
        )


# ===========================
# HOJE
# ===========================

if filtro in ["Todas", "Hoje"]:

    if hoje_lista:

        st.subheader("🟢 Hoje")

        for ordem in hoje_lista:

            exibir_os(
                ordem,
                "hoje"
            )

    elif filtro == "Hoje":

        st.success(
            "Nenhuma retirada agendada para hoje."
        )


# ===========================
# PRÓXIMAS
# ===========================

if filtro in ["Todas", "Próximas"]:

    if proximas:

        st.subheader("⚪ Próximas")

        for ordem in proximas:

            exibir_os(
                ordem,
                "proxima"
            )

    elif filtro == "Próximas":

        st.success(
            "Nenhuma retirada futura agendada."
        )


# ===========================
# SEM RETIRADAS
# ===========================

if (
    filtro == "Todas"
    and not atrasadas
    and not hoje_lista
    and not proximas
):

    st.success(
        "Nenhuma retirada agendada."
    )


# ===========================
# VOLTAR
# ===========================

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):

    st.switch_page("app.py")