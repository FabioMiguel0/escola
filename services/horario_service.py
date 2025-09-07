from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS horario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_id INTEGER,
        turma_id INTEGER,
        disciplina TEXT,
        dia TEXT, -- e.g. Segunda, Terça
        hora TEXT  -- e.g. 08:00-09:00
    )
    """)
    conn.commit()
    conn.close()

def add_slot(professor_id: int, turma_id: int, disciplina: str, dia: str, hora: str):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO horario (professor_id, turma_id, disciplina, dia, hora) VALUES (?, ?, ?, ?, ?)",
                (professor_id, turma_id, disciplina, dia, hora))
    conn.commit()
    conn.close()

def list_horario_by_professor(professor_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM horario WHERE professor_id=? ORDER BY dia, hora", (professor_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# adiciona consulta por turma
def list_horario_by_turma(turma_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM horario WHERE turma_id=? ORDER BY dia, hora", (turma_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]