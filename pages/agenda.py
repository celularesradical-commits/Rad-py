import streamlit as st
from datetime import date
from database import supabase

st.set_page_config(
    page_title="Agenda",
    page_icon="📅",
    layout="centered"
)

st.title("📅 Agenda")

hoje = str(date.today())

resposta = (
    supabase.table("ordens_servico")
    .select("*")
    .eq("status", "Em andamento")
    .order("data_retirada")
    .execute()
)

lista = resposta.data

hoje_lista = []
amanha_lista = []
futuras_lista = []
atrasadas_lista = []

for os in lista:

    data = str(os["data_retirada"])

    if data < hoje:
        atrasadas_lista.append(os)

    elif data == hoje:
        hoje_lista.append(os)

    else:
        futuras_lista.append(os)

# ===========================
# ATRASADAS
# ===========================

if atrasadas_lista:

    st.subheader("🔴 Atrasadas")

    for os in atrasadas_lista:

        with st.container(border=True):

            st.write(f"**OS:** {os['numero_os']}")
            st.write(f"**Cliente:** {os['cliente']}")
            st.write(f"**Modelo:** {os['modelo']}")
            st.write(f"**Retirada:** {os['data_retirada']}")

# ===========================
# HOJE
# ===========================

if hoje_lista:

    st.subheader("🟢 Hoje")

    for os in hoje_lista:

        with st.container(border=True):

            st.write(f"**OS:** {os['numero_os']}")
            st.write(f"**Cliente:** {os['cliente']}")
            st.write(f"**Modelo:** {os['modelo']}")
            st.write(f"**Retirada:** {os['data_retirada']}")

# ===========================
# FUTURAS
# ===========================

if futuras_lista:

    st.subheader("⚪ Próximas")

    for os in futuras_lista:

        with st.container(border=True):

            st.write(f"**OS:** {os['numero_os']}")
            st.write(f"**Cliente:** {os['cliente']}")
            st.write(f"**Modelo:** {os['modelo']}")
            st.write(f"**Retirada:** {os['data_retirada']}")

if (
    not atrasadas_lista
    and not hoje_lista
    and not futuras_lista
):
    st.success("Nenhuma retirada agendada.")

st.divider()

if st.button(
    "⬅️ Voltar",
    use_container_width=True
):
    st.switch_page("app.py")