from services.db import get_conn
from services import nota_service, turma_service, disciplina_service
from services import aluno_service
from services import professor_service
from services import horario_service

def seed_all():
    conn = get_conn()
    cur = conn.cursor()

    # garante tabelas mínimas
    turma_service.ensure_table()
    disciplina_service.ensure_table()
    professor_service.ensure_table()
    nota_service.ensure_table()
    aluno_service.ensure_table()

    # seed professores
    cur.execute("SELECT COUNT(1) as c FROM professores")
    if cur.fetchone()["c"] == 0:
        p1 = professor_service.create(
            nome="João Silva", documento="123456789", area_atuacao="Matemática",
            formacao="Licenciatura em Matemática", disponibilidade="Manhã", contato="joao@email.com"
        )
        p2 = professor_service.create(
            nome="Maria Souza", documento="987654321", area_atuacao="Português",
            formacao="Licenciatura em Letras", disponibilidade="Tarde", contato="maria@email.com"
        )
        p3 = professor_service.create(
            nome="Carlos Lima", documento="555666777", area_atuacao="Física",
            formacao="Licenciatura em Física", disponibilidade="Manhã,Tarde", contato="carlos@email.com"
        )
    else:
        cur.execute("SELECT id FROM professores ORDER BY id")
        rows = cur.fetchall()
        p1 = rows[0]["id"] if rows else None
        p2 = rows[1]["id"] if len(rows) > 1 else None
        p3 = rows[2]["id"] if len(rows) > 2 else None

    # seed disciplinas com carga horária
    cur.execute("SELECT COUNT(1) as c FROM disciplinas")
    if cur.fetchone()["c"] == 0:
        disciplina_service.add_disciplina("Matemática", professor_id=None)
        disciplina_service.add_disciplina("Português", professor_id=None)
        disciplina_service.add_disciplina("Física", professor_id=None)

    # seed turmas
    cur.execute("SELECT COUNT(1) as c FROM turmas")
    if cur.fetchone()["c"] == 0:
        cur.execute("INSERT INTO turmas (nome, ano_letivo, turno) VALUES (?, ?, ?)", ("10ª A", 2025, "Manhã"))
        cur.execute("INSERT INTO turmas (nome, ano_letivo, turno) VALUES (?, ?, ?)", ("9ª B", 2025, "Tarde"))
        conn.commit()

    # seed alunos
    cur.execute("SELECT COUNT(1) as c FROM alunos")
    if cur.fetchone()["c"] == 0:
        a1 = aluno_service.create(nome="João Silva", matricula="2025-001")
        a2 = aluno_service.create(nome="Maria Costa", matricula="2025-002")
        a3 = aluno_service.create(nome="Pedro Gomes", matricula="2025-003")
        alunos = [a1, a2, a3]
    else:
        cur.execute("SELECT id FROM alunos ORDER BY id LIMIT 3")
        alunos = [r["id"] for r in cur.fetchall()]

    # associa alunos a turmas (turma_alunos)
    cur.execute("SELECT COUNT(1) as c FROM turma_alunos")
    if cur.fetchone()["c"] == 0:
        cur.execute("SELECT id FROM turmas ORDER BY id")
        turmas = [r["id"] for r in cur.fetchall()]
        if turmas:
            for i, aid in enumerate(alunos):
                tid = turmas[i % len(turmas)]
                cur.execute("INSERT INTO turma_alunos (turma_id, aluno_id) VALUES (?, ?)", (tid, aid))
        conn.commit()

    # seed horários
    cur.execute("SELECT COUNT(1) as c FROM horarios")
    if cur.fetchone()["c"] == 0:
        # map disciplinas
        cur.execute("SELECT id, nome FROM disciplinas")
        disc_map = {r["nome"]: r["id"] for r in cur.fetchall()}
        cur.execute("SELECT id FROM turmas ORDER BY id")
        turmas = [r["id"] for r in cur.fetchall()]
        if p1 and turmas:
            horario_service.create(professor_id=p1, disciplina_id=disc_map.get("Matemática"), turma_id=turmas[0], dia_semana="Segunda", hora_inicio="08:00", hora_fim="10:00")
        if p3 and turmas:
            horario_service.create(professor_id=p3, disciplina_id=disc_map.get("Física"), turma_id=turmas[0], dia_semana="Quarta", hora_inicio="10:00", hora_fim="12:00")
        if p2 and len(turmas) > 1:
            horario_service.create(professor_id=p2, disciplina_id=disc_map.get("Português"), turma_id=turmas[1], dia_semana="Terça", hora_inicio="14:00", hora_fim="16:00")

    # seed notas de exemplo
    nota_service.seed_sample()

    conn.close()
    return True