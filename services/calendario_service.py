from services.db import get_connection
from models.calendario import Calendario

class CalendarioService:
    @staticmethod
    def adicionar_evento(evento: Calendario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO calendario (evento, data, descricao)
            VALUES (?, ?, ?)
        """, (evento.evento, evento.data, evento.descricao))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_eventos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, evento, data, descricao FROM calendario")
        rows = cursor.fetchall()
        conn.close()
        return [Calendario(id=row[0], evento=row[1], data=row[2], descricao=row[3]) for row in rows]

    @staticmethod
    def atualizar_evento(evento: Calendario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE calendario
            SET evento=?, data=?, descricao=?
            WHERE id=?
        """, (evento.evento, evento.data, evento.descricao, evento.id))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar_evento(evento_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calendario WHERE id=?", (evento_id,))
        conn.commit()
        conn.close()
