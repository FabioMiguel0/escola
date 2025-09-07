from services.db import get_conn

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        permission TEXT NOT NULL,
        UNIQUE(user_id, permission)
    )
    """)
    conn.commit()
    conn.close()

def grant_permission(user_id: int, permission: str):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO user_permissions (user_id, permission) VALUES (?, ?)", (user_id, permission))
    conn.commit()
    conn.close()

def revoke_permission(user_id: int, permission: str):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_permissions WHERE user_id = ? AND permission = ?", (user_id, permission))
    conn.commit()
    conn.close()

def has_permission(user_id: int, permission: str) -> bool:
    ensure_table()
    if user_id is None:
        return False
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM user_permissions WHERE user_id = ? AND permission = ? LIMIT 1", (user_id, permission))
    row = cur.fetchone()
    conn.close()
    return bool(row)

def list_permissions(user_id: int):
    ensure_table()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT permission FROM user_permissions WHERE user_id = ?", (user_id,))
    rows = [r["permission"] for r in cur.fetchall()]
    conn.close()
    return rows