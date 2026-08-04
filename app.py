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
# Estado da navegação
# ==========================
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"


def abrir(pagina):
    st.session_state.pagina = pagina


# ==========================
# Página Inicial
# ==========================
if st.session_state.pagina == "inicio":

    st.title("📱 RadicalSystem")
    st.subheader("Sistema de Gestão para Assistência Técnica")

    st.markdown("---")

    st.write("Selecione uma opção:")

    if st.button("📋 Nova Ordem de Serviço", use_container_width=True):
        abrir("ordens")
        st.rerun()

    if st.button("🔎 Pesquisar Ordem de Serviço", use_container_width=True):
        abrir("pesquisar_os")
        st.rerun()

    if st.button("🔍 Pesquisar Películas", use_container_width=True):
        abrir("peliculas")
        st.rerun()

    if st.button("👥 Clientes", use_container_width=True):
        abrir("clientes")
        st.rerun()

    if st.button("📅 Agenda", use_container_width=True):
        abrir("agenda")
        st.rerun()

    if st.button("⚙️ Configurações", use_container_width=True):
        abrir("configuracoes")
        st.rerun()

    st.markdown("---")
    st.caption("Radical Celulares • RadicalSystem")

# ==========================
# Pesquisar Películas
# ==========================
elif st.session_state.pagina == "peliculas":

    if st.button("⬅ Voltar"):
        abrir("inicio")
        st.rerun()

    import pages.peliculas

# ==========================
# Demais módulos
# ==========================
elif st.session_state.pagina == "ordens":

    if st.button("⬅ Voltar"):
        abrir("inicio")
        st.rerun()

    st.title("📋 Nova Ordem de Serviço")
    st.info("Em desenvolvimento.")

elif st.session_state.pagina == "pesquisar_os":

    if st.button("⬅ Voltar"):
        abrir("inicio")
        st.rerun()

    st.title("🔎 Pesquisar Ordem de Serviço")
    st.info("Em desenvolvimento.")

elif st.session_state.pagina == "clientes":

    if st.button("⬅ Voltar"):
        abrir("inicio")
        st.rerun()

    st.title("👥 Clientes")
    st.info("Em desenvolvimento.")

elif st.session_state.pagina == "agenda":

    if st.button("⬅ Voltar"):
        abrir("inicio")
        st.rerun()

    st.title("📅 Agenda")
    st.info("Em desenvolvimento.")

elif st.session_state.pagina == "configuracoes":

    if st.button("⬅ Voltar"):
        abrir("inicio")
        st.rerun()

    st.title("⚙️ Configurações")
    st.info("Em desenvolvimento.")
    