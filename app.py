import streamlit as st

# ============================================
# Configuração da página
# ============================================

st.set_page_config(
    page_title="RadicalSystem",
    page_icon="📱",
    layout="centered"
)

# ============================================
# Cabeçalho
# ============================================

st.title("📱 RadicalSystem")
st.subheader("Sistema de Gestão para Assistência Técnica")

st.markdown("---")

st.write("Selecione um módulo abaixo:")

# ============================================
# Botões
# ============================================

if st.button("📋 Nova Ordem de Serviço", use_container_width=True):
    st.switch_page("pages/ordens.py")

if st.button("🔎 Pesquisar Ordem de Serviço", use_container_width=True):
    st.switch_page("pages/pesquisar_os.py")

if st.button("🔍 Pesquisar Películas", use_container_width=True):
    st.switch_page("pages/peliculas.py")

if st.button("👥 Clientes", use_container_width=True):
    st.switch_page("pages/clientes.py")

if st.button("📅 Agenda", use_container_width=True):
    st.switch_page("pages/agenda.py")

if st.button("⚙️ Configurações", use_container_width=True):
    st.switch_page("pages/configuracoes.py")

st.markdown("---")

st.caption("Radical Celulares • RadicalSystem")