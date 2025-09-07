import sqlite3, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB = os.path.join(BASE_DIR, "sistema_escolar.db")

conn = sqlite3.connect(DB)
cur = conn.cursor()

users = [
    ("prof1", "profpass", "professor", None),
    ("aluno1", "alunopass", "aluno", None),
    ("resp1", "respass", "responsavel", None),
]

cur.executemany(
    "INSERT OR IGNORE INTO users (username, password, role, person_id) VALUES (?, ?, ?, ?)",
    users
)

conn.commit()
conn.close()
print("users added")