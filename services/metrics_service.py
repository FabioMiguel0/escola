from .db import get_connection

class MetricsService:
    def __init__(self):
        pass

    def get_total_alunos(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM alunos")
        count = cur.fetchone()[0]
        conn.close()
        return count

    def get_total_professores(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM professores")
        count = cur.fetchone()[0]
        conn.close()
        return count

    def get_total_turmas(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM turmas")
        count = cur.fetchone()[0]
        conn.close()
        return count

    def get_total_disciplinas(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM disciplinas")
        count = cur.fetchone()[0]
        conn.close()
        return count

    def get_proximos_eventos(self, limit=5):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT data, evento, COALESCE(descricao, '') FROM calendario ORDER BY data ASC LIMIT ?", (limit,))
        data = cur.fetchall()
        conn.close()
        return data

    def get_counts(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM alunos"); alunos = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM professores"); profs = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM turmas"); turmas = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM comunicados"); comunicados = cur.fetchone()[0]
        conn.close()
        return {"alunos": alunos, "professores": profs, "turmas": turmas, "comunicados": comunicados}
