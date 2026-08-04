import streamlit as st
# ==========================
# Configuração da página
# ==========================
st.set_page_config(
    page_title="RadicalSystem",
    page_icon="📱",
    layout="centered"
)
# ==========================
# Título
# ==========================
st.title("📱 RadicalSystem")
st.subheader("Sistema de Gestão para Assistência Técnica")
st.markdown("---")
st.write(
    "Bem-vindo ao RadicalSystem.\n\n"
    "Selecione uma opção abaixo para iniciar."
)
st.markdown("")
# ==========================
# Menu Principal
# ==========================
if st.button("📋 Nova Ordem de Serviço", use_container_width=True):
    st.info("🚧 Em desenvolvimento.")
if st.button("🔎 Pesquisar Ordem de Serviço", use_container_width=True):
    st.info("🚧 Em desenvolvimento.")
if st.button("🔍 Pesquisar Películas", use_container_width=True):
    st.info("🚧 Em desenvolvimento.")
if st.button("👥 Clientes", use_container_width=True):
    st.info("🚧 Em desenvolvimento.")
if st.button("📅 Agenda", use_container_width=True):
    st.info("🚧 Em desenvolvimento.")
if st.button("⚙️ Configurações", use_container_width=True):
    st.info("🚧 Em desenvolvimento.")
st.markdown("---")
st.caption("Radical Celulares • RadicalSystem • Versão 1.0")