import sqlite3
from pathlib import Path

# Caminho do banco de dados
DB_PATH = Path("radicalsystem.db")


def conectar():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_PATH)


def criar_banco():
    """Cria o banco de dados e as tabelas, caso não existam."""
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de Ordens de Serviço
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            defeito TEXT,
            valor REAL,
            data_retirada TEXT,
            cliente TEXT,
            contato TEXT,
            observacoes TEXT,
            status TEXT DEFAULT 'Recebido',
            data_entrada TEXT,
            data_entrega TEXT
        )
    """)

    conn.commit()
    conn.close()


# Cria o banco automaticamente ao importar este arquivo
criar_banco()