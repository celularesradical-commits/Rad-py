import sqlite3
from pathlib import Path
from datetime import datetime

DB_NAME = Path("radicalsystem.db")


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            numero_os INTEGER UNIQUE,

            cliente TEXT NOT NULL,

            contato TEXT,

            modelo TEXT NOT NULL,

            defeito TEXT,

            valor REAL DEFAULT 0,

            observacoes TEXT,

            data_entrada TEXT,

            data_retirada TEXT,

            data_entrega TEXT,

            status TEXT DEFAULT 'Recebido'

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS agenda(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            numero_os INTEGER,

            cliente TEXT,

            modelo TEXT,

            data_retirada TEXT,

            concluido INTEGER DEFAULT 0

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            produto TEXT,

            quantidade INTEGER DEFAULT 0,

            valor REAL DEFAULT 0

        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            empresa TEXT,

            telefone TEXT,

            endereco TEXT,

            garantia TEXT

        )
        """)

        self.conn.commit()

    def proximo_numero_os(self):

        self.cursor.execute(
            "SELECT MAX(numero_os) FROM ordens_servico"
        )

        numero = self.cursor.fetchone()[0]

        if numero is None:
            return 5001

        return numero + 1

    def salvar_os(
        self,
        cliente,
        contato,
        modelo,
        defeito,
        valor,
        data_retirada,
        observacoes
    ):

        numero = self.proximo_numero_os()

        data_entrada = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )        self.cursor.execute("""

        INSERT INTO ordens_servico(

            numero_os,
            cliente,
            contato,
            modelo,
            defeito,
            valor,
            observacoes,
            data_entrada,
            data_retirada,
            status

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

        """, (

            numero,
            cliente,
            contato,
            modelo,
            defeito,
            valor,
            observacoes,
            data_entrada,
            data_retirada,
            "Recebido"

        ))

        self.cursor.execute("""

        INSERT INTO agenda(

            numero_os,
            cliente,
            modelo,
            data_retirada,
            concluido

        )

        VALUES(?,?,?,?,0)

        """, (

            numero,
            cliente,
            modelo,
            data_retirada

        ))

        self.conn.commit()

        return numero

    def buscar(self, texto):

        self.cursor.execute("""

        SELECT *

        FROM ordens_servico

        WHERE

            CAST(numero_os AS TEXT) LIKE ?

            OR cliente LIKE ?

            OR contato LIKE ?

            OR modelo LIKE ?

        ORDER BY numero_os DESC

        """, (

            f"%{texto}%",
            f"%{texto}%",
            f"%{texto}%",
            f"%{texto}%"

        ))

        return self.cursor.fetchall()

    def listar_andamento(self):

        self.cursor.execute("""

        SELECT *

        FROM ordens_servico

        WHERE status <> 'Entregue'

        ORDER BY numero_os DESC

        """)

        return self.cursor.fetchall()

    def listar_entregues(self):

        self.cursor.execute("""

        SELECT *

        FROM ordens_servico

        WHERE status='Entregue'

        ORDER BY numero_os DESC

        """)

        return self.cursor.fetchall()    def editar_os(
        self,
        numero_os,
        cliente,
        contato,
        modelo,
        defeito,
        valor,
        data_retirada,
        observacoes
    ):

        self.cursor.execute("""

        UPDATE ordens_servico

        SET

            cliente=?,
            contato=?,
            modelo=?,
            defeito=?,
            valor=?,
            observacoes=?,
            data_retirada=?

        WHERE numero_os=?

        """, (

            cliente,
            contato,
            modelo,
            defeito,
            valor,
            observacoes,
            data_retirada,
            numero_os

        ))

        self.cursor.execute("""

        UPDATE agenda

        SET

            cliente=?,
            modelo=?,
            data_retirada=?

        WHERE numero_os=?

        """, (

            cliente,
            modelo,
            data_retirada,
            numero_os

        ))

        self.conn.commit()

    def marcar_entregue(self, numero_os):

        data = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

        self.cursor.execute("""

        UPDATE ordens_servico

        SET

            status='Entregue',
            data_entrega=?

        WHERE numero_os=?

        """, (

            data,
            numero_os

        ))

        self.cursor.execute("""

        UPDATE agenda

        SET concluido=1

        WHERE numero_os=?

        """, (

            numero_os,

        ))

        self.conn.commit()

    def excluir_os(self, numero_os):

        self.cursor.execute(

            "DELETE FROM agenda WHERE numero_os=?",

            (numero_os,)

        )

        self.cursor.execute(

            "DELETE FROM ordens_servico WHERE numero_os=?",

            (numero_os,)

        )

        self.conn.commit()     def obter_os(self, numero_os):

        self.cursor.execute("""

        SELECT *

        FROM ordens_servico

        WHERE numero_os=?

        """, (

            numero_os,

        ))

        return self.cursor.fetchone()

    def fechar(self):

        self.conn.close()


db = Database()


def salvar_os(
    cliente,
    contato,
    modelo,
    defeito,
    valor,
    data_retirada,
    observacoes
):

    return db.salvar_os(
        cliente,
        contato,
        modelo,
        defeito,
        valor,
        data_retirada,
        observacoes
    )


def buscar_os(texto):

    return db.buscar(texto)


def listar_andamento():

    return db.listar_andamento()


def listar_entregues():

    return db.listar_entregues()


def editar_os(
    numero_os,
    cliente,
    contato,
    modelo,
    defeito,
    valor,
    data_retirada,
    observacoes
):

    db.editar_os(
        numero_os,
        cliente,
        contato,
        modelo,
        defeito,
        valor,
        data_retirada,
        observacoes
    )


def marcar_entregue(numero_os):

    db.marcar_entregue(numero_os)


def excluir_os(numero_os):

    db.excluir_os(numero_os)


def obter_os(numero_os):

    return db.obter_os(numero_os)