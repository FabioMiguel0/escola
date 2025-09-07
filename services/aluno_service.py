from .db import get_conn

# -------- CRUD Aluno --------
def list_alunos():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT a.id, a.nome, IFNULL(t.nome, 'Sem turma')
        FROM alunos a
        LEFT JOIN turmas t ON t.id = a.turma_id
        ORDER BY a.nome
    """)
    rows = [{"id":i,"nome":n,"turma":t} for i,n,t in cur.fetchall()]
    conn.close()
    return rows

def add_aluno(nome:str, turma_id:int|None):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO alunos (nome, turma_id) VALUES (?, ?)", (nome.strip(), turma_id))
    conn.commit(); conn.close()

def update_aluno(aluno_id:int, nome:str, turma_id:int|None):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE alunos SET nome=?, turma_id=? WHERE id=?", (nome.strip(), turma_id, aluno_id))
    conn.commit(); conn.close()

def delete_aluno(aluno_id:int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM matriculas WHERE aluno_id=?", (aluno_id,))
    cur.execute("DELETE FROM notas WHERE aluno_id=?", (aluno_id,))
    cur.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
    conn.commit(); conn.close()

# -------- Matrículas e Consultas do Aluno --------
def list_disciplinas_matriculadas(aluno_id:int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT d.id, d.nome
        FROM matriculas m
        JOIN disciplinas d ON d.id = m.disciplina_id
        WHERE m.aluno_id = ?
        ORDER BY d.nome
    """, (aluno_id,))
    rows = [{"id":i,"nome":n} for i,n in cur.fetchall()]
    conn.close()
    return rows

def set_matriculas(aluno_id:int, disciplina_ids:list[int]):
    """Substitui as matrículas do aluno pelas fornecidas."""
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM matriculas WHERE aluno_id=?", (aluno_id,))
    cur.executemany("INSERT INTO matriculas (aluno_id, disciplina_id) VALUES (?, ?)",
                    [(aluno_id, d) for d in disciplina_ids])
    conn.commit(); conn.close()

def get_turma_do_aluno(aluno_id:int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT IFNULL(t.nome,'Sem turma')
        FROM alunos a LEFT JOIN turmas t ON t.id=a.turma_id
        WHERE a.id=?
    """,(aluno_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "Não encontrado"

import sqlite3
from services.db import get_conn

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
    # cria tabela base se não existir (esquema mínimo)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        matricula TEXT
    )
    """)
    # migrações: adiciona colunas ausentes
    _add_column_if_missing(cur, "alunos", "turma_id INTEGER")
    _add_column_if_missing(cur, "alunos", "bi TEXT")
    _add_column_if_missing(cur, "alunos", "nome_pai TEXT")
    _add_column_if_missing(cur, "alunos", "nome_mae TEXT")
    _add_column_if_missing(cur, "alunos", "idade INTEGER")
    _add_column_if_missing(cur, "alunos", "localidade TEXT")
    _add_column_if_missing(cur, "alunos", "numero_casa TEXT")
    _add_column_if_missing(cur, "alunos", "periodo TEXT")
    _add_column_if_missing(cur, "alunos", "ano_letivo TEXT")
    _add_column_if_missing(cur, "alunos", "telefone TEXT")
    conn.commit()
    conn.close()

def get_all():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get(id_):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos WHERE id = ?", (id_,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None

def create(nome, matricula=None, turma_id=None, bi=None, nome_pai=None, nome_mae=None, idade=None, localidade=None, numero_casa=None, periodo=None, ano_letivo=None, telefone=None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alunos
        (nome, matricula, turma_id, bi, nome_pai, nome_mae, idade, localidade, numero_casa, periodo, ano_letivo, telefone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, matricula, turma_id, bi, nome_pai, nome_mae, idade, localidade, numero_casa, periodo, ano_letivo, telefone))
    conn.commit()
    id_ = cur.lastrowid
    conn.close()
    return id_

def update(id_, nome, matricula=None, turma_id=None, bi=None, nome_pai=None, nome_mae=None, idade=None, localidade=None, numero_casa=None, periodo=None, ano_letivo=None, telefone=None):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE alunos SET nome=?, matricula=?, turma_id=?, bi=?, nome_pai=?, nome_mae=?, idade=?, localidade=?, numero_casa=?, period o=?, ano_letivo=?, telefone=?
        WHERE id=?
    """.replace("period o","period"), (nome, matricula, turma_id, bi, nome_pai, nome_mae, idade, localidade, numero_casa, periodo, ano_letivo, telefone, id_))
    conn.commit()
    conn.close()

def delete(id_):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM alunos WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def assign_turma(id_, turma_id):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE alunos SET turma_id=? WHERE id=?", (turma_id, id_))
    conn.commit()
    conn.close()

def count_alunos():
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) as c FROM alunos")
    r = cur.fetchone()
    conn.close()
    return r["c"] if r else 0
