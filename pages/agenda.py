import streamlit as st
from datetime import date
from database import supabase
from fotos import obter_url_foto

st.set_page_config(
    page_title="Agenda",
    page_icon="📅",
    layout="centered"
)

st.title("📅 Agenda")

# ===========================
# FUNÇÃO PARA EXIBIR A OS
# ===========================

def exibir_os(os, tipo):

    numero_os = os["numero_os"]

    with st.container(border=True):

        st.write(f"**🆔 OS:** {numero_os}")
        st.write(f"**👤 Cliente:** {os['cliente']}")
        st.write(f"**📱 Modelo:** {os['modelo']}")
        st.write(f"**📅 Retirada:** {os['data_retirada']}")

        # ===========================
        # FOTO DA OS
        # ===========================

        url_foto = obter_url_foto(numero_os)

        st.image(
            url_foto,
            caption=f"Foto da OS Nº {numero_os}",
            use_container_width=True
        )

        if st.button(
            "📄 Abrir Ordem de Serviço",
            key=f"{tipo}_{numero_os}",
            use_container_width=True
        ):

            st.session_state["os_editar"] = numero_os

            st.switch_page("pages/editar_reparo.py")


# ===========================
# BUSCAR ORDENS
# ===========================

hoje = date.today().isoformat()

resposta = (
    supabase.table("ordens_servico")
    .select("*")
    .eq("status", "Em andamento")
    .order("data_retirada")
    .execute()
)

lista = resposta.data

atrasadas = []
hoje_lista = []
proximas = []

for os in lista:

    data_retirada = str(os["data_retirada"])

    if data_retirada < hoje:
        atrasadas.append(os)

    elif data_retirada == hoje:
        hoje_lista.append(os)

    else:
        proximas.append(os)

# ===========================
# ATRASADAS
# ===========================

if atrasadas:

    st.subheader("🔴 Atrasadas")

    for os in atrasadas:
        exibir_os(
            os,
            "atrasada"
        )

# ===========================
# HOJE
# ===========================

if hoje_lista:

    st.subheader("🟢 Hoje")

    for os in hoje_lista:
        exibir_os(
            os,
            "hoje"
        )

# ===========================
# PRÓXIMAS
# ===========================

if proximas:

    st.subheader("⚪ Próximas")

    for os in proximas:
        exibir_os(
            os,
            "proxima"
        )

# ===========================
# SEM RETIRADAS
# ===========================

if (
    len(atrasadas) == 0
    and len(hoje_lista) == 0
    and len(proximas) == 0
):

    st.success("Nenhuma retirada agendada.")

# ===========================
# VOLTAR
# ===========================

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):

    st.switch_page("app.py")