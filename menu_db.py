import sqlite3
import json

DB_NAME = "menus.db"

# Inicializa o banco de dados
def init_menu_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cardapios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL UNIQUE,
            itens TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

# Função para salvar um novo cardápio
def salvar_cardapio(usuario_id, nome, itens):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    itens_json = json.dumps(itens)  # Converte os itens para JSON

    try:
        cursor.execute("INSERT INTO cardapios (usuario_id, nome, itens) VALUES (?, ?, ?)", 
                       (usuario_id, nome, itens_json))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Nome de cardápio já existe
    finally:
        conn.close()

# Função para carregar todos os cardápios do usuário
def carregar_cardapios(usuario_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM cardapios WHERE usuario_id = ?", (usuario_id,))
    cardapios = cursor.fetchall()
    conn.close()
    return cardapios  # Retorna lista de (id, nome)

# Função para carregar um cardápio específico
def carregar_cardapio_por_id(cardapio_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT itens FROM cardapios WHERE id = ?", (cardapio_id,))
    cardapio = cursor.fetchone()
    conn.close()
    return json.loads(cardapio[0]) if cardapio else None

# Função para editar um cardápio salvo
def editar_cardapio(cardapio_id, novos_itens):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    itens_json = json.dumps(novos_itens)
    cursor.execute("UPDATE cardapios SET itens = ? WHERE id = ?", (itens_json, cardapio_id))
    conn.commit()
    conn.close()

# Função para excluir um cardápio
def excluir_cardapio(cardapio_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cardapios WHERE id = ?", (cardapio_id,))
    conn.commit()
    conn.close()
