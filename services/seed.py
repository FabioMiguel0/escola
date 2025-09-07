from services.db import get_conn
from services import nota_service, horario_service, turma_service, disciplina_service
from services import aluno_service

def seed_all():
    conn = get_conn()
    cur = conn.cursor()

    # garante tabelas e seeds mínimos
    turma_service.ensure_table()
    disciplina_service.ensure_table()
    horario_service.ensure_table()
    nota_service.ensure_table()
    aluno_service.ensure_table()

    # seed disciplinas
    cur.execute("SELECT COUNT(1) as c FROM disciplinas")
    if cur.fetchone()["c"] == 0:
        disciplina_service.add_disciplina("Matemática", professor_id=2)
        disciplina_service.add_disciplina("Português", professor_id=3)
        disciplina_service.add_disciplina("Física", professor_id=2)

    # seed turmas
    cur.execute("SELECT COUNT(1) as c FROM turmas")
    if cur.fetchone()["c"] == 0:
        cur.execute("INSERT INTO turmas (nome, professor_id) VALUES (?, ?)", ("10A", 2))
        cur.execute("INSERT INTO turmas (nome, professor_id) VALUES (?, ?)", ("11B", 3))
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

    # seed horário
    cur.execute("SELECT COUNT(1) as c FROM horario")
    if cur.fetchone()["c"] == 0:
        horario_service.add_slot(professor_id=2, turma_id=1, disciplina="Matemática", dia="Segunda", hora="08:00-09:00")
        horario_service.add_slot(professor_id=2, turma_id=1, disciplina="Física", dia="Quarta", hora="10:00-11:00")
        horario_service.add_slot(professor_id=3, turma_id=2, disciplina="Português", dia="Terça", hora="09:00-10:00")

    # seed notas de exemplo
    nota_service.seed_sample()

    conn.close()
    return True