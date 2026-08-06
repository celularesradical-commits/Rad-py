import streamlit as st
from datetime import date
from database import supabase

st.set_page_config(
    page_title="Agenda",
    page_icon="📅",
    layout="centered"
)

st.title("📅 Agenda")

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

    data = str(os["data_retirada"])

    if data < hoje:
        atrasadas.append(os)

    elif data == hoje:
        hoje_lista.append(os)

    else:
        proximas.append(os)

# ===========================
# ATRASADAS
# ===========================

if atrasadas:

    st.subheader("🔴 Atrasadas")

    for os in atrasadas:

        with st.container(border=True):

            st.write(f"**🆔 OS:** {os['numero_os']}")
            st.write(f"**👤 Cliente:** {os['cliente']}")
            st.write(f"**📱 Modelo:** {os['modelo']}")
            st.write(f"**📅 Retirada:** {os['data_retirada']}")

            if st.button(
                "📄 Abrir Ordem de Serviço",
                key=f"atrasada_{os['numero_os']}",
                use_container_width=True
            ):

                st.session_state["os_editar"] = os["numero_os"]

                st.switch_page("pages/editar_reparo.py")

# ===========================
# HOJE
# ===========================

if hoje_lista:

    st.subheader("🟢 Hoje")

    for os in hoje_lista:

        with st.container(border=True):

            st.write(f"**🆔 OS:** {os['numero_os']}")
            st.write(f"**👤 Cliente:** {os['cliente']}")
            st.write(f"**📱 Modelo:** {os['modelo']}")
            st.write(f"**📅 Retirada:** {os['data_retirada']}")

            if st.button(
                "📄 Abrir Ordem de Serviço",
                key=f"hoje_{os['numero_os']}",
                use_container_width=True
            ):

                st.session_state["os_editar"] = os["numero_os"]

                st.switch_page("pages/editar_reparo.py")

# ===========================
# PRÓXIMAS
# ===========================

if proximas:

    st.subheader("⚪ Próximas")

    for os in proximas:

        with st.container(border=True):

            st.write(f"**🆔 OS:** {os['numero_os']}")
            st.write(f"**👤 Cliente:** {os['cliente']}")
            st.write(f"**📱 Modelo:** {os['modelo']}")
            st.write(f"**📅 Retirada:** {os['data_retirada']}")

            if st.button(
                "📄 Abrir Ordem de Serviço",
                key=f"proxima_{os['numero_os']}",
                use_container_width=True
            ):

                st.session_state["os_editar"] = os["numero_os"]

                st.switch_page("pages/editar_reparo.py")

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