import sqlite3
from services.db import get_conn
from services import disciplina_service

def _table_info(conn, table):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info('{table}')")
    return [dict(r) for r in cur.fetchall()]

def _existing_columns(cur, table):
    cur.execute(f"PRAGMA table_info('{table}')")
    return [r["name"] for r in cur.fetchall()]

def _add_column_if_missing(cur, table, column_sql):
    col_name = column_sql.split()[0]
    cols = _existing_columns(cur, table)
    if col_name not in cols:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_sql}")

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    # cria tabela mínima se não existir
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL
    )
    """)
    # garante colunas esperadas (migração segura)
    _add_column_if_missing(cur, "notas", "disciplina TEXT")
    _add_column_if_missing(cur, "notas", "valor REAL")
    _add_column_if_missing(cur, "notas", "periodo TEXT")
    _add_column_if_missing(cur, "notas", "turma_id INTEGER")
    _add_column_if_missing(cur, "notas", "professor_id INTEGER")
    # garante coluna disciplina_id caso versões antigas a usem
    _add_column_if_missing(cur, "notas", "disciplina_id INTEGER")
    conn.commit()
    conn.close()

def _col_notnull(conn, table, col):
    for info in _table_info(conn, table):
        if info["name"] == col:
            return bool(info.get("notnull"))
    return False

def _find_disciplina_id_by_name(name: str):
    if not name:
        return None
    try:
        for d in disciplina_service.list_disciplinas():
            if d.get("nome") and d["nome"].strip().lower() == name.strip().lower():
                return d["id"]
    except Exception:
        pass
    return None

def create_nota(aluno_id: int, disciplina: str, valor: float, periodo: str = None, turma_id: int = None, professor_id: int = None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()

    cols_info = _table_info(conn, "notas")
    cols = [c["name"] for c in cols_info]

    insert_cols = []
    params = []

    # aluno_id sempre
    insert_cols.append("aluno_id"); params.append(aluno_id)

    # disciplina text if available
    if "disciplina" in cols:
        insert_cols.append("disciplina"); params.append(disciplina)

    # disciplina_id if available: try map by name, fallback to 0 if NOT NULL
    if "disciplina_id" in cols:
        did = _find_disciplina_id_by_name(disciplina)
        if did is None and _col_notnull(conn, "notas", "disciplina_id"):
            # fallback para 0 para satisfazer NOT NULL (legacy)
            did = 0
        insert_cols.append("disciplina_id"); params.append(did)

    if "valor" in cols:
        insert_cols.append("valor"); params.append(valor)
    if "periodo" in cols:
        insert_cols.append("periodo"); params.append(periodo)
    if "turma_id" in cols:
        insert_cols.append("turma_id"); params.append(turma_id)
    if "professor_id" in cols:
        insert_cols.append("professor_id"); params.append(professor_id)

    q = f"INSERT INTO notas ({', '.join(insert_cols)}) VALUES ({', '.join(['?']*len(insert_cols))})"
    cur.execute(q, tuple(params))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return nid

# compatibilidade: add_nota (usada por views antigas)
def add_nota(aluno_id: int, disciplina: str, valor: float, periodo: str = None, turma_id: int = None, professor_id: int = None):
    return create_nota(aluno_id, disciplina, valor, periodo, turma_id, professor_id)

def update_nota(nota_id: int, aluno_id: int, disciplina: str, valor: float, periodo: str = None, turma_id: int = None, professor_id: int = None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    # atualiza tanto disciplina (texto) quanto disciplina_id se existirem
    cols = _existing_columns(cur, "notas")
    set_parts = []
    params = []
    set_parts.append("aluno_id=?"); params.append(aluno_id)
    if "disciplina" in cols:
        set_parts.append("disciplina=?"); params.append(disciplina)
    if "disciplina_id" in cols:
        did = _find_disciplina_id_by_name(disciplina)
        if did is None and _col_notnull(conn, "notas", "disciplina_id"):
            did = 0
        set_parts.append("disciplina_id=?"); params.append(did)
    if "valor" in cols:
        set_parts.append("valor=?"); params.append(valor)
    if "periodo" in cols:
        set_parts.append("periodo=?"); params.append(periodo)
    if "turma_id" in cols:
        set_parts.append("turma_id=?"); params.append(turma_id)
    if "professor_id" in cols:
        set_parts.append("professor_id=?"); params.append(professor_id)
    params.append(nota_id)
    q = f"UPDATE notas SET {', '.join(set_parts)} WHERE id=?"
    cur.execute(q, tuple(params))
    conn.commit()
    conn.close()

def delete_nota(nota_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM notas WHERE id=?", (nota_id,))
    conn.commit()
    conn.close()

def get_notas_by_aluno(aluno_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, aluno_id, disciplina, valor, periodo, turma_id, professor_id FROM notas WHERE aluno_id = ? ORDER BY periodo, disciplina", (aluno_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_boletim_summary(aluno_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(periodo, '') as periodo, AVG(valor) as media
        FROM notas
        WHERE aluno_id = ?
        GROUP BY periodo
        ORDER BY periodo
    """, (aluno_id,))
    rows = cur.fetchall()
    conn.close()
    return [ {'periodo': r['periodo'], 'media': r['media']} for r in rows ]

def list_notas(aluno_id: int = None, turma_id: int = None, professor_id: int = None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    q = "SELECT * FROM notas"
    params = []
    where = []
    if aluno_id is not None:
        where.append("aluno_id = ?"); params.append(aluno_id)
    if turma_id is not None:
        where.append("turma_id = ?"); params.append(turma_id)
    if professor_id is not None:
        where.append("professor_id = ?"); params.append(professor_id)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY id DESC"
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def seed_sample():
    ensure_table()
    # inserir exemplos só se tabela vazia
    if not list_notas():
        create_nota(1, "Matemática", 15.0, "2025-1", turma_id=1, professor_id=2)
        create_nota(1, "Português", 12.0, "2025-1", turma_id=1, professor_id=3)
        create_nota(2, "Matemática", 10.0, "2025-1", turma_id=1, professor_id=2)
