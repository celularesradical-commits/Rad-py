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

st.write("""
Bem-vindo ao **RadicalSystem**.

Este sistema foi desenvolvido para facilitar a gestão da assistência técnica da Radical Celulares.

### Módulos disponíveis

- 📋 Nova Ordem de Serviço
- 🔎 Pesquisar Ordem de Serviço
- 🔍 Pesquisar Películas
- 👥 Clientes
- 📅 Agenda
- ⚙️ Configurações

➡️ Utilize o **menu lateral** para acessar cada módulo.
""")

st.info("👈 Selecione um módulo no menu lateral.")

st.markdown("---")

st.success("Sistema iniciado com sucesso.")

st.caption("© Radical Celulares • RadicalSystem • Versão 1.0")