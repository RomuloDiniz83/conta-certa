import sqlite3
import hashlib
import streamlit as st

DB_NAME = "users.db"

# Criar a tabela de usuários se não existir
def init_auth_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            data_nascimento TEXT NOT NULL,
            nome_mae TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para cadastrar um usuário
def registrar_usuario(nome, email, data_nascimento, nome_mae, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()  # Hash da senha
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (nome, email, data_nascimento, nome_mae, senha) VALUES (?, ?, ?, ?, ?)", 
                       (nome, email, data_nascimento, nome_mae.lower(), senha_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email já cadastrado
    finally:
        conn.close()

# Função para verificar login
def verificar_login(email, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND senha = ?", (email, senha_hash))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def usuario_existe(email):
    """Verifica se um usuário já está cadastrado pelo email."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe


# Função para recuperar senha
def recuperar_senha(email, nome_mae):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND nome_mae = ?", (email, nome_mae.lower()))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None  # Retorna True se os dados estiverem corretos

