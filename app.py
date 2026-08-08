import streamlit as st
from datetime import date
from database import supabase

# ============================================
# Configuração da página
# ============================================

st.set_page_config(
    page_title="RadicalSystem",
    page_icon="📱",
    layout="centered"
)

# ============================================
# Verificar Login
# ============================================

if not st.session_state.get("logado", False):
    st.switch_page("pages/login.py")
    st.stop()

# ============================================
# Dados do Perfil
# ============================================

perfil_id = st.session_state.get("perfil_id")

perfil_nome = st.session_state.get(
    "perfil_nome",
    "Usuário"
)

perfil_loja = st.session_state.get(
    "perfil_loja",
    "Loja 1"
)

# ============================================
# Contador da Agenda
# ============================================

hoje = date.today().isoformat()

try:

    resposta = (
        supabase.table("ordens_servico")
        .select("numero_os")
        .eq("status", "Em andamento")
        .eq("data_retirada", hoje)
        .execute()
    )

    agenda_hoje = len(resposta.data)

except Exception:

    agenda_hoje = 0

# ============================================
# Cabeçalho
# ============================================

st.title("📱 RadicalSystem")
st.subheader("Sistema de Gestão para Assistência Técnica")

st.divider()

# ============================================
# Perfil e Loja
# ============================================

col_usuario, col_loja = st.columns([2, 1])

with col_usuario:

    st.caption(
        f"👤 {perfil_nome}"
    )

with col_loja:

    lojas = [
        "Loja 1",
        "Loja 2"
    ]

    if perfil_loja not in lojas:
        perfil_loja = "Loja 1"

    loja_selecionada = st.selectbox(
        "Loja atual",
        lojas,
        index=lojas.index(perfil_loja),
        label_visibility="collapsed",
        key="loja_menu"
    )

# ============================================
# Alterar Loja
# ============================================

if loja_selecionada != perfil_loja:

    try:

        (
            supabase.table("perfis")
            .update(
                {
                    "loja": loja_selecionada
                }
            )
            .eq("id", perfil_id)
            .execute()
        )

        st.session_state["perfil_loja"] = loja_selecionada

        st.rerun()

    except Exception as erro:

        st.error(
            f"Não foi possível alterar a loja:\n\n{erro}"
        )

st.divider()

st.write("Selecione um módulo abaixo:")

# ============================================
# Botões
# ============================================

if st.button(
    "📋 Ordem de Serviço",
    use_container_width=True
):
    st.switch_page("pages/novo_reparo.py")

if st.button(
    "🔎 Pesquisar Reparo",
    use_container_width=True
):
    st.switch_page("pages/pesquisar_os.py")

if st.button(
    "🛠️ Reparos em Andamento",
    use_container_width=True
):
    st.switch_page("pages/reparos_andamento.py")

if st.button(
    "✅ Entregues",
    use_container_width=True
):
    st.switch_page("pages/entregues.py")

if st.button(
    "🔍 Pesquisar Películas",
    use_container_width=True
):
    st.switch_page("pages/peliculas.py")

if st.button(
    f"📅 Agenda ({agenda_hoje})",
    use_container_width=True
):
    st.switch_page("pages/agenda.py")

if st.button(
    "💬 Chat Geral",
    use_container_width=True
):
    st.switch_page("pages/chat.py")

if st.button(
    "📱 Analisar Panic Full",
    use_container_width=True
):
    st.switch_page("pages/panic_full.py")

if st.button(
    "📦 Estoque",
    use_container_width=True
):
    st.switch_page("pages/estoque.py")

if st.button(
    "💰 PDV",
    use_container_width=True
):
    st.switch_page("pages/pdv.py")

if st.button(
    "📊 Relatórios",
    use_container_width=True
):
    st.switch_page("pages/relatorios.py")

if st.button(
    "⚙️ Configurações",
    use_container_width=True
):
    st.switch_page("pages/configuracoes.py")

# ============================================
# Rodapé
# ============================================

st.divider()

st.caption(
    "Radical Celulares • RadicalSystem"
)