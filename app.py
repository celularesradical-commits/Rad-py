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
# Cabeçalho
# ==========================
st.title("📱 RadicalSystem")
st.subheader("Sistema de Gestão para Assistência Técnica")

st.markdown("---")

st.write(
    """
Bem-vindo ao **RadicalSystem**.

Selecione uma opção abaixo:
"""
)

# ==========================
# Menu Principal
# ==========================

st.page_link(
    "pages/ordens.py",
    label="📋 Nova Ordem de Serviço",
    icon="📋"
)

st.page_link(
    "pages/pesquisar_os.py",
    label="🔎 Pesquisar Ordem de Serviço",
    icon="🔎"
)

st.page_link(
    "pages/peliculas.py",
    label="🔍 Pesquisar Películas",
    icon="🔍"
)

st.page_link(
    "pages/clientes.py",
    label="👥 Clientes",
    icon="👥"
)

st.page_link(
    "pages/agenda.py",
    label="📅 Agenda",
    icon="📅"
)

st.page_link(
    "pages/configuracoes.py",
    label="⚙️ Configurações",
    icon="⚙️"
)

st.markdown("---")

st.info(
    "Versão 1.0 - RadicalSystem\n\n"
    "Desenvolvido para gerenciamento de assistência técnica."
)