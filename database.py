import sqlite3
from pathlib import Path

# Caminho do banco de dados
DB_PATH = Path("radicalsystem.db")


def conectar():
    """Conecta ao banco de dados."""
    return sqlite3.connect(DB_PATH)


def criar_banco():
    """Cria as tabelas do sistema."""

    conn = conectar()
    cursor = conn.cursor()

    # Ordem de Serviço
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            contato TEXT,
            modelo TEXT NOT NULL,
            defeito TEXT,
            valor REAL DEFAULT 0,
            data_entrada TEXT,
            data_retirada TEXT,
            data_entrega TEXT,
            observacoes TEXT,
            status TEXT DEFAULT 'Recebido'
        )
    """)

    # Agenda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            os_id INTEGER,
            cliente TEXT,
            modelo TEXT,
            data TEXT,
            concluido INTEGER DEFAULT 0
        )
    """)

    # Estoque
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            quantidade INTEGER DEFAULT 0,
            valor REAL DEFAULT 0
        )
    """)

    # Configurações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT,
            telefone TEXT,
            endereco TEXT,
            garantia TEXT
        )
    """)

    conn.commit()
    conn.close()


# Cria o banco automaticamente
criar_banco()


if __name__ == "__main__":
    print("Banco de dados criado com sucesso.")