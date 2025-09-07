from services.db import get_connection, get_conn
import hashlib

# ========================
# Função utilitária de hash
# ========================
def _hash_pwd(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

# ========================
# Autenticação
# ========================
def authenticate(email: str, password: str):
    """
    Autentica usuário pelo email e senha.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, senha, tipo FROM usuarios WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    if row["senha"] == _hash_pwd(password):
        return {"id": row["id"], "nome": row["nome"], "email": row["email"], "tipo": row["tipo"]}
    return None

# ========================
# Cadastro de usuários
# ========================
def registrar_usuario(nome, email, senha, tipo="aluno"):
    """
    Cadastra um novo usuário com senha hasheada.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, _hash_pwd(senha), tipo)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Erro ao registrar usuário:", e)
        return False
    finally:
        conn.close()

# ========================
# Itens de menu por papel
# ========================
def menu_for_role(role: str):
    """
    Retorna lista de items do menu para o role solicitado.
    Cada item é uma tupla (route, label). A UI/Shell deve adaptar-se a esta estrutura.
    """
    role = (role or "").lower()
    # assegura que professores vejam 'documentos'
    menu_map = {
        "admin": [
            ("dashboard", "Dashboard"),
            ("usuarios", "Usuários"),
            ("professores", "Professores"),
            ("disciplinas", "Disciplinas"),
            ("turmas", "Turmas"),
            ("alunos", "Alunos"),
            ("documentos", "Documentos"),
            ("comunicados", "Comunicados"),
            ("calendario", "Calendário"),
            ("frequencia", "Frequência"),
            ("notas", "Notas"),
        ],
        "professor": [
            ("dashboard", "Dashboard"),
            ("minhas_turmas", "Minhas Turmas"),
            ("horario", "Horário"),
            ("minhas_disciplinas", "Disciplinas"),
            ("frequencia", "Frequência"),
            ("notas", "Notas"),
            ("comunicados", "Comunicados"),
            ("documentos", "Documentos"),  # ADICIONADO
        ],
        "aluno": [
            ("perfil", "Perfil"),
            ("desempenho", "Desempenho"),
            ("boletim", "Boletim"),
            ("horario", "Horário"),
        ],
        # ... outros papéis ...
    }
    return menu_map.get(role, menu_map.get("aluno"))

def authenticate(username: str, password: str, role: str = None):
    # modo dev: aceita qualquer credencial (retorna dict com id/role)
    return {"id": 0, "username": username, "role": role or "aluno"}

# ========================
# Funções extras para alunos
# ========================
def get_aluno_turma(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id, t.nome
        FROM turmas t
        JOIN disciplinas d ON d.turma_id = t.id
        JOIN notas n ON n.disciplina_id = d.id
        WHERE n.aluno_id = ?
        LIMIT 1
    """, (aluno_id,))
    turma = cursor.fetchone()

    conn.close()
    return turma["nome"] if turma else None


def get_aluno_disciplinas(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT d.id, d.nome
        FROM disciplinas d
        JOIN notas n ON n.disciplina_id = d.id
        WHERE n.aluno_id = ?
    """, (aluno_id,))
    disciplinas = cursor.fetchall()

    conn.close()
    return [d["nome"] for d in disciplinas]


def get_aluno_boletim(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT d.nome AS disciplina, n.nota
        FROM notas n
        JOIN disciplinas d ON n.disciplina_id = d.id
        WHERE n.aluno_id = ?
    """, (aluno_id,))
    boletim = cursor.fetchall()

    conn.close()
    return [{"disciplina": row["disciplina"], "nota": row["nota"]} for row in boletim]

def list_users():
    """Retorna lista de usuários (id, username, role)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def change_role(user_id: int, new_role: str, performed_by: str = None):
    """
    Altera o papel (role) de um usuário.
    Regras de proteção:
    - performed_by não pode alterar seu próprio papel.
    - não é permitido remover o último usuário com role='admin'.
    Lança ValueError em caso de violação.
    """
    conn = get_conn()
    cur = conn.cursor()

    # busca usuário alvo
    cur.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    target = cur.fetchone()
    if not target:
        conn.close()
        raise ValueError("Usuário alvo não encontrado.")

    target_username = target["username"]
    target_role = target["role"] or "aluno"

    # proteção: não permitir que o executor altere seu próprio papel
    if performed_by is not None and performed_by == target_username:
        conn.close()
        raise ValueError("Operação proibida: você não pode alterar seu próprio papel.")

    # proteção: não remover o último admin
    if target_role == "admin" and new_role != "admin":
        cur.execute("SELECT COUNT(1) as c FROM users WHERE role = 'admin'")
        row = cur.fetchone()
        admin_count = row["c"] if row else 0
        if admin_count <= 1:
            conn.close()
            raise ValueError("Operação proibida: não é possível remover o último administrador.")

    # realiza alteração
    cur.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()
    return True

def create_user(username: str, password: str = None, role: str = "aluno"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()

