import os
import sqlite3
from datetime import datetime
from def_logs import log_error, log_info
from documento import Documento
import hashlib
from usuario import Usuario


class BancoDocumento:
    def __init__(self, nome_banco="banco_documento.sqlite"):
        # Define e cria a pasta 'banco' automaticamente se não existir
        pasta_banco = os.path.join(os.path.dirname(__file__), "banco")
        os.makedirs(pasta_banco, exist_ok=True)
        self.nome_banco = os.path.join(pasta_banco, nome_banco)
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.nome_banco)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela_documento(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Documento (
                        nome_arquivo TEXT PRIMARY KEY,
                        caminho TEXT NOT NULL,
                        tipo_arquivo TEXT NOT NULL,
                        data_criacao TEXT NOT NULL,
                        tamanho_mb REAL
                    )
                    """
                )
                self.conn.commit()
                log_info("Tabela Documento criada com sucesso")
            except sqlite3.Error as e:
                log_error(f"Erro ao criar tabela Documento: {e}")

    def criar_tabela_usuario(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Usuario (
                        cpf TEXT PRIMARY KEY,
                        senha TEXT NOT NULL,
                        nome TEXT,
                        email TEXT
                    )
                    """
                )
                self.conn.commit()
                log_info("Tabela Usuario criada com sucesso")
            except sqlite3.Error as e:
                log_error(f"Erro ao criar tabela Usuario: {e}")

    def inserir_usuario(self, usuario: Usuario):
        if self.conn:
            if not usuario.cpf:
                log_error("CPF é obrigatório para inserir usuário")
                return
            try:
                senha_hash = hashlib.sha256(usuario.senha.encode()).hexdigest()
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Usuario (cpf, senha, nome, email) VALUES (?, ?, ?, ?)",
                    (usuario.cpf, senha_hash, usuario.nome, usuario.email)
                )
                self.conn.commit()
                log_info(f"Novo usuário inserido: {usuario.email}")
            except sqlite3.IntegrityError as e:
                log_error(f"Erro ao inserir usuário - dados duplicados: {e}")
            except sqlite3.Error as e:
                log_error(f"Erro ao inserir usuário: {e}")

    def verificar_login(self, email: str, senha: str):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT nome, senha FROM Usuario WHERE email = ?", (email,))
                return cursor.fetchone()
            except sqlite3.Error as e:
                log_error(f"Erro ao verificar login: {e}")
        return False

    def atualizar_documento(self, documento: Documento):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE Documento SET caminho=?, tipo_arquivo=?, data_criacao=?, tamanho_mb=? WHERE nome_arquivo=?",
                    (
                        documento.caminho,
                        documento.tipo_arquivo,
                        documento.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
                        documento.tamanho_mb,
                        documento.nome_arquivo
                    )
                )
                self.conn.commit()
                log_info(f"Atualização no documento {documento.nome_arquivo}")
            except sqlite3.Error as e:
                print(f"Erro ao atualizar documento: {e}")

    def apagar_documento(self, nome_arquivo: str):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM Documento WHERE nome_arquivo=?", (nome_arquivo,))
                self.conn.commit()
                log_info(f"Documento excluído: {nome_arquivo}")
            except sqlite3.Error as e:
                print(f"Erro ao apagar documento: {e}")

    def buscar_todos_documentos(self):
        documentos = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Documento")
                for row in cursor.fetchall():
                    nome_arquivo, caminho, tipo_arquivo, data_criacao, tamanho_mb = row
                    documentos.append(
                        Documento(
                            nome_arquivo,
                            caminho,
                            tipo_arquivo,
                            datetime.strptime(data_criacao, '%Y-%m-%d %H:%M:%S'),
                            tamanho_mb
                        )
                    )
                log_info("Consulta de todos os documentos")
            except sqlite3.Error as e:
                print(f"Erro ao buscar documentos: {e}")
        return documentos

    def buscar_documento_por_nome(self, nome_arquivo: str):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Documento WHERE nome_arquivo=?", (nome_arquivo,))
                row = cursor.fetchone()
                if row:
                    nome_arquivo, caminho, tipo_arquivo, data_criacao, tamanho_mb = row
                    return Documento(
                        nome_arquivo,
                        caminho,
                        tipo_arquivo,
                        datetime.strptime(data_criacao, '%Y-%m-%d %H:%M:%S'),
                        tamanho_mb
                    )
                log_info(f"Consulta aos dados do documento: {nome_arquivo}")
            except sqlite3.Error as e:
                print(f"Erro ao buscar documento por nome: {e}")
        return None

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def inserir_documento(self, documento: Documento):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO Documento (nome_arquivo, caminho, tipo_arquivo, data_criacao, tamanho_mb) VALUES (?, ?, ?, ?, ?)",
                    (documento.nome_arquivo, documento.caminho, documento.tipo_arquivo, 
                     documento.data_criacao.strftime('%Y-%m-%d %H:%M:%S'), documento.tamanho_mb)
                )
                self.conn.commit()
                log_info(f"Novo documento inserido: {documento.nome_arquivo}")
            except sqlite3.IntegrityError as e:
                log_error(f"Erro ao inserir documento - dados duplicados: {e}")
                raise
            except sqlite3.Error as e:
                log_error(f"Erro ao inserir documento: {e}")

    def atualizar_documento_por_nome(self, nome_antigo: str, novo_documento: Documento):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    """
                    UPDATE Documento 
                    SET nome_arquivo=?, caminho=?, tipo_arquivo=?, data_criacao=?, tamanho_mb=?
                    WHERE nome_arquivo=?
                    """,
                    (novo_documento.nome_arquivo, novo_documento.caminho, novo_documento.tipo_arquivo,
                     novo_documento.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
                     novo_documento.tamanho_mb, nome_antigo)
                )
                self.conn.commit()
                log_info(f"Documento atualizado: {nome_antigo} -> {novo_documento.nome_arquivo}")
            except sqlite3.Error as e:
                log_error(f"Erro ao atualizar documento: {e}")
