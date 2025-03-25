import sqlite3
import json

def init_historico_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            restaurante TEXT,
            data TEXT,
            total REAL,
            itens TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

def salvar_conta(usuario_id, restaurante, data, total, itens):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    itens_json = json.dumps(itens)
    cursor.execute('''
        INSERT INTO historico_contas (usuario_id, restaurante, data, total, itens)
        VALUES (?, ?, ?, ?, ?)
    ''', (usuario_id, restaurante, data, total, itens_json))
    conn.commit()
    conn.close()

def carregar_historico(usuario_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, restaurante, data, total, itens FROM historico_contas WHERE usuario_id = ? ORDER BY data DESC
    ''', (usuario_id,))
    dados = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "restaurante": row[1],
            "data": row[2],
            "total": row[3],
            "itens": json.loads(row[4])
        }
        for row in dados
    ]
