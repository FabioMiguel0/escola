import sqlite3
import os

# Caminho do DB ao lado da pasta do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "sistema_escolar.db")

def get_conn():
    """Retorna uma conexão sqlite3 (compatível com código que importa get_conn)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# manter alias para compatibilidade com código que usa get_connection
def get_connection():
    return get_conn()

def _ensure_table_exists_minimal(cur):
    # garante existência da tabela users com pelo menos id e username
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )
    """)

def _existing_columns(cur, table):
    cur.execute(f"PRAGMA table_info('{table}')")
    return [r["name"] for r in cur.fetchall()]

def _add_column_if_missing(cur, table, column_sql):
    # column_sql ex: "password TEXT"
    col_name = column_sql.split()[0]
    cols = _existing_columns(cur, table)
    if col_name not in cols:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_sql}")

def create_tables_and_seed():
    """Cria tabelas mínimas e insere seed (não sobrescreve se já existirem)."""
    conn = get_conn()
    cur = conn.cursor()

    # USERS: cria tabela mínima se não existir, depois adiciona colunas faltantes
    _ensure_table_exists_minimal(cur)
    # adicionar colunas que podem estar faltando
    _add_column_if_missing(cur, "users", "password TEXT")
    _add_column_if_missing(cur, "users", "role TEXT DEFAULT 'aluno'")
    _add_column_if_missing(cur, "users", "person_id INTEGER")

    # outras tabelas mínimas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    # cria tabelas usadas por serviços (disciplinas, alunos, notas, frequencias, comunicados, documentos)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        matricula TEXT,
        turma_id INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        disciplina TEXT,
        valor REAL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS frequencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        data TEXT,
        presente INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comunicados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        texto TEXT,
        data TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT
    )
    """)

    # insere admin se não existir, usando apenas colunas disponíveis
    cols = _existing_columns(cur, "users")
    cur.execute("SELECT COUNT(1) as c FROM users WHERE username = ?", ("admin",))
    row = cur.fetchone()
    if not row or row["c"] == 0:
        insert_cols = []
        placeholders = []
        values = []
        # sempre temos username
        insert_cols.append("username"); placeholders.append("?"); values.append("admin")
        if "password" in cols:
            insert_cols.append("password"); placeholders.append("?"); values.append("admin")
        if "role" in cols:
            insert_cols.append("role"); placeholders.append("?"); values.append("admin")
        sql = f"INSERT INTO users ({', '.join(insert_cols)}) VALUES ({', '.join(placeholders)})"
        cur.execute(sql, values)

    conn.commit()
    conn.close()
