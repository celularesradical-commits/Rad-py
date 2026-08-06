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

except:

    agenda_hoje = 0

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

if st.button("📋 Ordem de Serviço", use_container_width=True):
    st.switch_page("pages/novo_reparo.py")

if st.button("🔎 Pesquisar Reparo", use_container_width=True):
    st.switch_page("pages/pesquisar_os.py")

if st.button("🛠️ Reparos em Andamento", use_container_width=True):
    st.switch_page("pages/reparos_andamento.py")

if st.button("✅ Entregues", use_container_width=True):
    st.switch_page("pages/entregues.py")

if st.button("🔍 Pesquisar Películas", use_container_width=True):
    st.switch_page("pages/peliculas.py")

if st.button(f"📅 Agenda ({agenda_hoje})", use_container_width=True):
    st.switch_page("pages/agenda.py")

if st.button("📦 Estoque", use_container_width=True):
    st.switch_page("pages/estoque.py")

if st.button("💰 PDV", use_container_width=True):
    st.switch_page("pages/pdv.py")

if st.button("📊 Relatórios", use_container_width=True):
    st.switch_page("pages/relatorios.py")

if st.button("⚙️ Configurações", use_container_width=True):
    st.switch_page("pages/configuracoes.py")

st.markdown("---")

st.caption("Radical Celulares • RadicalSystem")