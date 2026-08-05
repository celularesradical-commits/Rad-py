import streamlit as st
from datetime import datetime

from database import salvar_os
from utils.impressao import imprimir_os

st.set_page_config(
    page_title="Nova Ordem de Serviço",
    page_icon="🔧",
    layout="centered"
)

st.title("🔧 Nova Ordem de Serviço")

with st.form("nova_os"):

    modelo = st.text_input(
        "📱 Modelo do Celular"
    )

    defeito = st.text_area(
        "🔧 Defeito Identificado"
    )

    valor = st.number_input(
        "💰 Valor do Reparo",
        min_value=0.0,
        step=1.0,
        format="%.2f"
    )

    cliente = st.text_input(
        "👤 Nome do Cliente"
    )

    contato = st.text_input(
        "📞 Contato"
    )

    data_retirada = st.date_input(
        "📅 Data Prevista de Retirada"
    )

    observacoes = st.text_area(
        "📝 Observações"
    )

    salvar = st.form_submit_button(
        "💾 Salvar Ordem de Serviço",
        use_container_width=True
    )

if salvar:

    if cliente == "" or modelo == "":

        st.error(
            "Cliente e Modelo são obrigatórios."
        )

    else:

        numero_os = salvar_os(

            cliente=cliente,

            contato=contato,

            modelo=modelo,

            defeito=defeito,

            valor=valor,

            data_retirada=data_retirada.strftime(
                "%d/%m/%Y"
            ),

            observacoes=observacoes

        )        imprimir_os(numero_os)

        st.success(
            f"✅ Ordem de Serviço {numero_os} cadastrada com sucesso!"
        )

        st.info(
            f"📅 Data de entrada: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        st.balloons()

        st.rerun()# FIM DO ARQUIVO pages/novo_reparo.py