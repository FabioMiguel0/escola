def create_tables_and_seed():
    import sqlite3

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sistema_escolar.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        turma_id INTEGER,
        FOREIGN KEY (turma_id) REFERENCES turmas (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        disciplina_id INTEGER,
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        disciplina_id INTEGER,
        nota REAL,
        FOREIGN KEY (aluno_id) REFERENCES alunos (id),
        FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id)
    )
    ''')

    # Seed initial data
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('secretaria', 'secretaria', 'secretaria')")

    conn.commit()
    conn.close()