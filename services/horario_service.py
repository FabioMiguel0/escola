from services.db import get_conn


def ensure_tables():
    conn = get_conn()
    cur = conn.cursor()
    # Dependências
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """
    )
    # Horários
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER NOT NULL,
            disciplina_id INTEGER NOT NULL,
            turma_id INTEGER NOT NULL,
            dia_semana TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fim TEXT NOT NULL,
            FOREIGN KEY (professor_id) REFERENCES professores(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
            FOREIGN KEY (turma_id) REFERENCES turmas(id)
        )
        """
    )
    conn.commit()
    conn.close()


def _has_time_overlap(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    return not (a_end <= b_start or b_end <= a_start)


def has_conflict(professor_id: int, dia_semana: str, hora_inicio: str, hora_fim: str, ignore_id: int = None) -> bool:
    """Verifica conflito de horário para o mesmo professor no mesmo dia.
    Horários são strings HH:MM, comparadas lexicograficamente (válido nesse formato).
    """
    ensure_tables()
    conn = get_conn()
    cur = conn.cursor()
    if ignore_id is None:
        cur.execute(
            "SELECT hora_inicio, hora_fim FROM horarios WHERE professor_id = ? AND dia_semana = ?",
            (professor_id, dia_semana),
        )
    else:
        cur.execute(
            "SELECT hora_inicio, hora_fim FROM horarios WHERE professor_id = ? AND dia_semana = ? AND id <> ?",
            (professor_id, dia_semana, ignore_id),
        )
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        if _has_time_overlap(hora_inicio, hora_fim, r["hora_inicio"], r["hora_fim"]):
            return True
    return False


def create(professor_id: int, disciplina_id: int, turma_id: int, dia_semana: str, hora_inicio: str, hora_fim: str):
    ensure_tables()
    if has_conflict(professor_id, dia_semana, hora_inicio, hora_fim):
        raise ValueError("Conflito de horário para este professor no mesmo dia.")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO horarios (professor_id, disciplina_id, turma_id, dia_semana, hora_inicio, hora_fim)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (professor_id, disciplina_id, turma_id, dia_semana, hora_inicio, hora_fim),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update(id_: int, **kwargs):
    ensure_tables()
    allowed = {"professor_id", "disciplina_id", "turma_id", "dia_semana", "hora_inicio", "hora_fim"}
    fields = []
    values = []
    for k, v in kwargs.items():
        if k in allowed:
            fields.append(f"{k} = ?")
            values.append(v)
    if not fields:
        return

    # Se for alterar professor/dia/horas, validar conflitos
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT professor_id, dia_semana, hora_inicio, hora_fim FROM horarios WHERE id = ?", (id_,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return
    new_prof = kwargs.get("professor_id", row["professor_id"]) 
    new_day = kwargs.get("dia_semana", row["dia_semana"]) 
    new_start = kwargs.get("hora_inicio", row["hora_inicio"]) 
    new_end = kwargs.get("hora_fim", row["hora_fim"]) 
    conn.close()
    if has_conflict(new_prof, new_day, new_start, new_end, ignore_id=id_):
        raise ValueError("Conflito de horário na atualização.")

    conn = get_conn()
    cur = conn.cursor()
    values.append(id_)
    sql = f"UPDATE horarios SET {', '.join(fields)} WHERE id = ?"
    cur.execute(sql, values)
    conn.commit()
    conn.close()


def delete(id_: int):
    ensure_tables()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM horarios WHERE id = ?", (id_,))
    conn.commit()
    conn.close()


def get(id_: int):
    ensure_tables()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM horarios WHERE id = ?", (id_,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None


def list_by_professor(professor_id: int):
    ensure_tables()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM horarios WHERE professor_id = ? ORDER BY dia_semana, hora_inicio",
        (professor_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_by_turma(turma_id: int):
    ensure_tables()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM horarios WHERE turma_id = ? ORDER BY dia_semana, hora_inicio",
        (turma_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_all():
    ensure_tables()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM horarios ORDER BY dia_semana, hora_inicio")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

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