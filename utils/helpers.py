from datetime import datetime


def data_hora_atual():
    """Retorna a data e hora atual no formato dd/mm/aaaa HH:MM"""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def data_atual():
    """Retorna apenas a data atual no formato dd/mm/aaaa"""
    return datetime.now().strftime("%d/%m/%Y")


def moeda(valor):
    """Formata um número como moeda brasileira"""
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"