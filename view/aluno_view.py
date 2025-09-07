import re
import flet as ft
from services.aluno_service import get_all, create, update, delete, assign_turma, get
from services.turma_service import list_turmas
from services.permission_service import has_permission

# validações
NAME_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-]+$")
def _valid_name(s: str) -> bool:
    return bool(s and NAME_RE.match(s.strip()))

def _valid_digits(s: str) -> bool:
    return bool(s and s.isdigit())

def _valid_bi(s: str) -> bool:
    return bool(s and re.fullmatch(r"[A-Za-z0-9]{14}", s.strip()))

def _valid_phone(s: str) -> bool:
    return bool(s and re.fullmatch(r"\d{9}", s.strip()))

def _sanitize_name_input(s: str) -> str:
    # remove dígitos e caracteres proibidos
    return re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ\s'\-]", "", s or "")

def _sanitize_digits_input(s: str) -> str:
    return re.sub(r"[^\d]", "", s or "")

def AlunoView(page: ft.Page, role="aluno", current_user_id=None, go=None):
    page.auto_scroll = True

    # Função para detectar tamanho da tela
    def get_screen_width():
        try:
            return getattr(page, "window_width", 1200)
        except:
            return 1200
    
    screen_width = get_screen_width()
    is_mobile = screen_width < 768
    is_tablet = 768 <= screen_width < 1024
    
    # Campos responsivos
    field_width = 280 if is_mobile else (320 if is_tablet else 360)
    small_field_width = 120 if is_mobile else (140 if is_tablet else 160)
    medium_field_width = 200 if is_mobile else (220 if is_tablet else 240)
    
    nome = ft.TextField(label="Nome", width=field_width)
    bi_field = ft.TextField(label="Nº BI", width=medium_field_width, max_length=14, tooltip="14 caracteres alfanuméricos")
    matricula = ft.TextField(label="Matrícula", width=medium_field_width)
    nome_pai = ft.TextField(label="Nome do Pai", width=field_width)
    nome_mae = ft.TextField(label="Nome da Mãe", width=field_width)
    idade = ft.TextField(label="Idade", width=small_field_width, keyboard_type=ft.KeyboardType.NUMBER)
    localidade = ft.TextField(label="Localidade", width=medium_field_width)
    numero_casa = ft.TextField(label="Número da Casa", width=small_field_width, keyboard_type=ft.KeyboardType.NUMBER)
    periodo = ft.Dropdown(label="Período", width=medium_field_width, options=[ft.dropdown.Option("Manhã", text="Manhã"), ft.dropdown.Option("Tarde", text="Tarde"), ft.dropdown.Option("Noite", text="Noite")], value="Manhã")
    ano_letivo = ft.TextField(label="Ano Letivo", width=small_field_width)
    telefone = ft.TextField(label="Telefone", width=small_field_width, max_length=9, keyboard_type=ft.KeyboardType.NUMBER, tooltip="9 dígitos")

    turma_options = [ft.dropdown.Option("", text="-- sem turma --")]
    turma_options += [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()]
    turma_dropdown = ft.Dropdown(label="Turma (nova matrícula)", width=medium_field_width, options=turma_options, value="")

    # Usar layout manual simples para evitar problemas de texto vertical
    table_header = ft.Container(
        content=ft.Row([
            ft.Container(ft.Text("#", size=14, weight="bold", color="#6B7280"), width=60, alignment=ft.alignment.center),
            ft.Container(ft.Text("Nome", size=14, weight="bold", color="#6B7280"), width=200, alignment=ft.alignment.center),
            ft.Container(ft.Text("Nº BI", size=14, weight="bold", color="#6B7280"), width=150, alignment=ft.alignment.center),
            ft.Container(ft.Text("Matrícula", size=14, weight="bold", color="#6B7280"), width=120, alignment=ft.alignment.center),
            ft.Container(ft.Text("Telefone", size=14, weight="bold", color="#6B7280"), width=120, alignment=ft.alignment.center),
            ft.Container(ft.Text("Turma Atual", size=14, weight="bold", color="#6B7280"), width=140, alignment=ft.alignment.center),
            ft.Container(ft.Text("Nova Turma", size=14, weight="bold", color="#6B7280"), width=160, alignment=ft.alignment.center),
            ft.Container(ft.Text("Ações", size=14, weight="bold", color="#6B7280"), width=200, alignment=ft.alignment.center),
        ], spacing=0),
        bgcolor="#F9FAFB",
        padding=ft.padding.symmetric(vertical=16, horizontal=8),
        border=ft.border.only(bottom=ft.BorderSide(2, "#E5E7EB")),
    )
    
    data_table = ft.Column([], spacing=0)
    
    list_view = ft.ListView(expand=True, spacing=6, padding=6)

    def can_manage_students():
        if role == "admin":
            return True
        if role == "secretaria":
            return has_permission(current_user_id, "matricular")
        return False

    def _show_error(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg)); page.snack_bar.open = True; page.update()

    # mascaramento simples: on_change handlers
    def on_name_change(e):
        v = _sanitize_name_input(nome.value)
        if v != nome.value:
            nome.value = v
            page.update()

    def on_nome_pai_change(e):
        v = _sanitize_name_input(nome_pai.value)
        if v != nome_pai.value:
            nome_pai.value = v; page.update()

    def on_nome_mae_change(e):
        v = _sanitize_name_input(nome_mae.value)
        if v != nome_mae.value:
            nome_mae.value = v; page.update()

    def on_idade_change(e):
        v = _sanitize_digits_input(idade.value)
        if v != idade.value:
            idade.value = v; page.update()

    def on_numero_casa_change(e):
        v = _sanitize_digits_input(numero_casa.value)
        if v != numero_casa.value:
            numero_casa.value = v; page.update()

    def on_telefone_change(e):
        v = _sanitize_digits_input(telefone.value)[:9]
        if v != telefone.value:
            telefone.value = v; page.update()

    def on_bi_change(e):
        # BI permite alfanum, limita a 14
        v = re.sub(r"[^A-Za-z0-9]", "", bi_field.value or "")[:14]
        if v != bi_field.value:
            bi_field.value = v; page.update()

    nome.on_change = on_name_change
    nome_pai.on_change = on_nome_pai_change
    nome_mae.on_change = on_nome_mae_change
    idade.on_change = on_idade_change
    numero_casa.on_change = on_numero_casa_change
    telefone.on_change = on_telefone_change
    bi_field.on_change = on_bi_change

    def load_list():
        # Limpar e recriar as linhas da tabela
        data_table.controls.clear()
        list_view.controls.clear()
        turmas = {str(t["id"]): t["nome"] for t in list_turmas()}
        
        for a in get_all():
            current_turma = str(a.get("turma_id")) if a.get("turma_id") else ""
            aid = a["id"]
            
            # Dropdown para nova turma
            row_turma_dd = ft.Dropdown(
                options=[ft.dropdown.Option("", text="-- sem turma --")] + 
                        [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()],
                value=current_turma, 
                width=160
            )
            
            # Botão Matricular
            def make_matricular_cb(aid_local, dd_local):
                return lambda e: on_matricular(aid_local, dd_local)
            row_mat_btn = ft.ElevatedButton(
                "Matricular", 
                on_click=make_matricular_cb(aid, row_turma_dd), 
                width=100,
                height=36,
                style=ft.ButtonStyle(
                    bgcolor="#3B82F6", 
                    color=ft.Colors.WHITE, 
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8)
                )
            )
            row_mat_btn.disabled = not can_manage_students()
            
            # Layout responsivo da linha
            if is_mobile:
                # Para mobile, usar cards no ListView
                student_card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"#{a['id']}", weight="bold", size=14),
                            ft.Text(a.get("nome") or "", weight="bold", size=14, expand=True),
                        ], alignment="spaceBetween"),
                        ft.Row([
                            ft.Text(f"BI: {a.get('bi') or '--'}", size=12, color="#6B7280"),
                            ft.Text(f"Matrícula: {a.get('matricula') or '--'}", size=12, color="#6B7280"),
                        ], alignment="spaceBetween"),
                        ft.Row([
                            ft.Text(f"Telefone: {a.get('telefone') or '--'}", size=12, color="#6B7280"),
                            ft.Text(f"Turma: {turmas.get(current_turma, '--')}", size=12, color="#6B7280"),
                        ], alignment="spaceBetween"),
                        ft.Divider(height=1, color="#E5E7EB"),
                        ft.Row([
                            row_turma_dd,
                            row_mat_btn,
                            ft.IconButton(ft.Icons.EDIT, on_click=lambda e, aid_local=aid: on_edit(aid_local), icon_size=20),
                            ft.IconButton(ft.Icons.DELETE, on_click=lambda e, aid_local=aid: on_delete(aid_local), icon_size=20),
                        ], alignment="spaceBetween"),
                    ], spacing=8),
                    padding=16,
                    bgcolor="#F9FAFB",
                    border_radius=12,
                    border=ft.border.all(1, "#E5E7EB"),
                )
                list_view.controls.append(student_card)
            else:
                # Para desktop, usar layout manual
                row = ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text(str(a["id"]), size=12), width=60, alignment=ft.alignment.center),
                        ft.Container(ft.Text(a.get("nome") or "", size=12, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS), width=200, alignment=ft.alignment.center),
                        ft.Container(ft.Text(a.get("bi") or "", size=12), width=150, alignment=ft.alignment.center),
                        ft.Container(ft.Text(a.get("matricula") or "", size=12), width=120, alignment=ft.alignment.center),
                        ft.Container(ft.Text(a.get("telefone") or "", size=12), width=120, alignment=ft.alignment.center),
                        ft.Container(ft.Text(turmas.get(current_turma, "--"), size=12), width=140, alignment=ft.alignment.center),
                        ft.Container(row_turma_dd, width=160, alignment=ft.alignment.center),
                        ft.Container(
                            ft.Row([
                                row_mat_btn,
                                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, aid_local=aid: on_edit(aid_local), icon_size=18, tooltip="Editar"),
                                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, aid_local=aid: on_delete(aid_local), icon_size=18, tooltip="Excluir"),
                            ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                            width=200, alignment=ft.alignment.center
                        ),
                    ], spacing=0),
                    bgcolor="#FFFFFF",
                    padding=ft.padding.symmetric(vertical=12, horizontal=8),
                    border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")),
                )
                data_table.controls.append(row)
        page.update()

    def _validate_all_fields():
        if not _valid_name(nome.value):
            return False, "Nome inválido (apenas letras, espaços, - e ')."
        if nome_pai.value and not _valid_name(nome_pai.value):
            return False, "Nome do pai inválido."
        if nome_mae.value and not _valid_name(nome_mae.value):
            return False, "Nome da mãe inválido."
        if idade.value and not _valid_digits(idade.value):
            return False, "Idade deve conter apenas números."
        if idade.value:
            iv = int(idade.value)
            if iv < 0 or iv > 120:
                return False, "Idade fora do intervalo válido."
        if numero_casa.value and not _valid_digits(numero_casa.value):
            return False, "Número da casa deve conter apenas dígitos."
        if bi_field.value and not _valid_bi(bi_field.value):
            return False, "BI inválido: deve ter exatamente 14 caracteres alfanuméricos."
        if telefone.value and not _valid_phone(telefone.value):
            return False, "Telefone inválido: deve ter exatamente 9 dígitos."
        return True, None

    def on_add(e):
        if not can_manage_students():
            _show_error("Sem permissão para cadastrar alunos"); return
        ok, msg = _validate_all_fields()
        if not ok:
            _show_error(msg); return

        tval = turma_dropdown.value
        turma_id = int(tval) if tval and str(tval).isdigit() else None
        idade_val = int(idade.value) if idade.value and idade.value.isdigit() else None

        try:
            create(
                nome=nome.value.strip(),
                matricula=matricula.value.strip() if matricula.value else None,
                turma_id=turma_id,
                bi=bi_field.value.strip() if bi_field.value else None,
                nome_pai=nome_pai.value.strip() if nome_pai.value else None,
                nome_mae=nome_mae.value.strip() if nome_mae.value else None,
                idade=idade_val,
                localidade=localidade.value.strip() if localidade.value else None,
                numero_casa=numero_casa.value.strip() if numero_casa.value else None,
                periodo=periodo.value if periodo.value else None,
                ano_letivo=ano_letivo.value.strip() if ano_letivo.value else None,
                telefone=telefone.value.strip() if telefone.value else None,
            )
        except Exception as ex:
            _show_error(f"Erro ao salvar no banco: {ex}"); return

        # limpa campos
        nome.value = bi_field.value = matricula.value = nome_pai.value = nome_mae.value = idade.value = localidade.value = numero_casa.value = ano_letivo.value = telefone.value = ""
        periodo.value = "Manhã"
        turma_dropdown.value = ""
        page.update()
        load_list()

    def on_edit(aid):
        a = get(aid)
        if not a: return
        nome.value = a.get("nome") or ""
        matricula.value = a.get("matricula") or ""
        turma_dropdown.value = str(a.get("turma_id")) if a.get("turma_id") else ""
        bi_field.value = a.get("bi") or ""
        nome_pai.value = a.get("nome_pai") or ""
        nome_mae.value = a.get("nome_mae") or ""
        idade.value = str(a.get("idade")) if a.get("idade") is not None else ""
        localidade.value = a.get("localidade") or ""
        numero_casa.value = a.get("numero_casa") or ""
        periodo.value = a.get("periodo") or "Manhã"
        ano_letivo.value = a.get("ano_letivo") or ""
        telefone.value = a.get("telefone") or ""
        page.update()
        save_btn.visible = True
        add_btn.visible = False
        save_btn.data = aid
        page.update()

    def on_save(e):
        aid = save_btn.data
        ok, msg = _validate_all_fields()
        if not ok:
            _show_error(msg); return

        tval = turma_dropdown.value
        turma_id = int(tval) if tval and str(tval).isdigit() else None
        idade_val = int(idade.value) if idade.value and idade.value.isdigit() else None

        try:
            update(
                aid,
                nome.value.strip(),
                matricula.value.strip() if matricula.value else None,
                turma_id,
                bi_field.value.strip() if bi_field.value else None,
                nome_pai.value.strip() if nome_pai.value else None,
                nome_mae.value.strip() if nome_mae.value else None,
                idade_val,
                localidade.value.strip() if localidade.value else None,
                numero_casa.value.strip() if numero_casa.value else None,
                periodo.value if periodo.value else None,
                ano_letivo.value.strip() if ano_letivo.value else None,
                telefone.value.strip() if telefone.value else None,
            )
        except Exception as ex:
            _show_error(f"Erro ao atualizar no banco: {ex}"); return

        nome.value = bi_field.value = matricula.value = nome_pai.value = nome_mae.value = idade.value = localidade.value = numero_casa.value = ano_letivo.value = telefone.value = ""
        periodo.value = "Manhã"
        turma_dropdown.value = ""
        save_btn.visible = False
        add_btn.visible = True
        page.update()
        load_list()

    def on_delete(aid):
        delete(aid); load_list()

    def on_matricular(aid, dd):
        if not can_manage_students():
            _show_error("Sem permissão para matricular alunos")
            return
        
        val = dd.value
        if not val or val == "":
            _show_error("Selecione uma turma para matricular o aluno")
            return
            
        try:
            turma_id = int(val) if val and str(val).isdigit() else None
            if turma_id is None:
                _show_error("Turma inválida selecionada")
                return
                
            # Atualizar matrícula do aluno
            assign_turma(aid, turma_id)
            
            # Buscar nome da turma para feedback
            turmas = {str(t["id"]): t["nome"] for t in list_turmas()}
            turma_nome = turmas.get(str(turma_id), "Turma desconhecida")
            
            # Mostrar sucesso
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Aluno matriculado na turma {turma_nome} com sucesso!"),
                bgcolor="#10B981"
            )
            page.snack_bar.open = True
            page.update()
            
            # Recarregar lista para mostrar mudanças
            load_list()
            
        except Exception as e:
            _show_error(f"Erro ao matricular aluno: {str(e)}")
            return

    add_btn = ft.ElevatedButton("Adicionar", on_click=on_add, disabled=not can_manage_students(),
                               style=ft.ButtonStyle(bgcolor="#3B82F6", color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12)))
    save_btn = ft.ElevatedButton("Salvar", on_click=on_save, visible=False,
                                style=ft.ButtonStyle(bgcolor="#10B981", color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12)))

    # Card do formulário responsivo
    if is_mobile:
        form_fields = [
            ft.Column([nome], spacing=12),
            ft.Column([bi_field], spacing=12),
            ft.Column([matricula], spacing=12),
            ft.Column([turma_dropdown], spacing=12),
            ft.Column([nome_pai], spacing=12),
            ft.Column([nome_mae], spacing=12),
            ft.Column([idade, localidade, numero_casa], spacing=12),
            ft.Column([periodo, ano_letivo, telefone], spacing=12),
            ft.Column([add_btn, save_btn], spacing=12)
        ]
    else:
        form_fields = [
            ft.Row([nome, bi_field], spacing=16),
            ft.Row([matricula, turma_dropdown], spacing=16),
            ft.Row([nome_pai, nome_mae], spacing=16),
            ft.Row([idade, localidade, numero_casa], spacing=16),
            ft.Row([periodo, ano_letivo, telefone], spacing=16),
            ft.Row([add_btn, save_btn], spacing=16)
        ]
    
    form_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PERSON_ADD, size=20 if is_mobile else 24, color="#3B82F6"),
                ft.Text("Dados do Aluno", 
                       size=16 if is_mobile else 20, 
                       weight="bold", color="#1F2937"),
            ], spacing=12),
            ft.Divider(height=1, color="#E5E7EB"),
            ft.Column(form_fields, spacing=16),
        ], spacing=16),
        padding=16 if is_mobile else 24,
        bgcolor="#FFFFFF",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=8, color="#00000010", offset=ft.Offset(0, 4)),
        border=ft.border.all(1, "#E5E7EB"),
    )

    # Card da lista de alunos responsivo
    if is_mobile:
        # Header simples para mobile
        list_header = ft.Row([
            ft.Icon(ft.Icons.SCHOOL, size=20, color="#10B981"),
            ft.Text("Lista de Alunos", size=16, weight="bold", color="#1F2937"),
        ], spacing=12)
    else:
        # Header com colunas para desktop/tablet - corrigindo texto vertical
        list_header = ft.Row([
            ft.Container(ft.Text("#", size=12, weight="bold", color="#6B7280"), width=60, alignment=ft.alignment.center),
            ft.Container(ft.Text("Nome", size=12, weight="bold", color="#6B7280"), expand=True, alignment=ft.alignment.center),
            ft.Container(ft.Text("Nº BI", size=12, weight="bold", color="#6B7280"), width=180, alignment=ft.alignment.center),
            ft.Container(ft.Text("Matrícula", size=12, weight="bold", color="#6B7280"), width=140, alignment=ft.alignment.center),
            ft.Container(ft.Text("Telefone", size=12, weight="bold", color="#6B7280"), width=140, alignment=ft.alignment.center),
            ft.Container(ft.Text("Turma Atual", size=12, weight="bold", color="#6B7280"), width=160, alignment=ft.alignment.center),
            ft.Container(ft.Text("Nova Turma", size=12, weight="bold", color="#6B7280"), width=180, alignment=ft.alignment.center),
            ft.Container(ft.Text("Ações", size=12, weight="bold", color="#6B7280"), width=300, alignment=ft.alignment.center),
        ], alignment="spaceBetween", spacing=4)
    
    # Container da lista com scroll horizontal
    if is_mobile:
        list_content = ft.Column([
            list_header,
            ft.Divider(height=1, color="#E5E7EB"),
            list_view,
        ], spacing=16)
    else:
        # Para desktop/tablet, usar layout manual
        list_content = ft.Column([
            table_header,
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=data_table,
                        expand=True,
                        width=1400,  # Largura fixa para forçar scroll horizontal
                    )
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
            ),
        ], spacing=0)
    
    list_card = ft.Container(
        content=list_content,
        padding=16 if is_mobile else 24,
        bgcolor="#FFFFFF",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=8, color="#00000010", offset=ft.Offset(0, 4)),
        border=ft.border.all(1, "#E5E7EB"),
        expand=True,
    )

    # Header responsivo da página
    header = ft.Container(
        content=ft.Column([
            ft.Text("Gestão de Alunos", 
                   size=20 if is_mobile else 28, 
                   weight="bold", color="#1F2937"),
            ft.Text("Cadastre e gerencie os alunos do sistema", 
                   size=14 if is_mobile else 16, 
                   color="#6B7280"),
        ], spacing=4),
        padding=ft.padding.only(bottom=16 if is_mobile else 24),
    )

    container = ft.Container(
        content=ft.Column([
            header,
            form_card,
            ft.Container(height=16 if is_mobile else 24),
            list_card,
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO),
        expand=True,
        padding=16 if is_mobile else 20,
    )

    load_list()
    return container

def build_students_table(students: list[dict]) -> ft.Control:
    """
    Retorna um ft.DataTable responsivo para exibir a lista de alunos.
    Cada item em 'students' deve ser um dict com chaves como:
      'nome', 'bi', 'matricula', 'turma', 'telefone'
    Garante que o nome NÃO seja renderizado letra-a-letra.
    """
    columns = [
        ft.DataColumn(ft.Text("#", weight="bold")),
        ft.DataColumn(ft.Text("Nome", weight="bold")),
        ft.DataColumn(ft.Text("Nº BI", weight="bold")),
        ft.DataColumn(ft.Text("Matrícula", weight="bold")),
        ft.DataColumn(ft.Text("Turma", weight="bold")),
        ft.DataColumn(ft.Text("Telefone", weight="bold")),
        ft.DataColumn(ft.Text("Ações", weight="bold")),
    ]

    rows = []
    for idx, s in enumerate(students, start=1):
        nome = s.get("nome", "")
        # garantir que 'nome' é uma string inteira (não uma lista)
        if isinstance(nome, (list, tuple)):
            nome = "".join(nome)

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(idx))),
                    # texto simples (não empacotar por caractere). Se ficar muito longo, o DataTable trata o overflow.
                    ft.DataCell(ft.Text(nome, selectable=True)),
                    ft.DataCell(ft.Text(s.get("bi", "--"))),
                    ft.DataCell(ft.Text(s.get("matricula", "--"))),
                    ft.DataCell(ft.Text(s.get("turma", "--"))),
                    ft.DataCell(ft.Text(s.get("telefone", "--"))),
                    # exemplo de ações (editar / apagar) — adapte handlers conforme seu código
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.EDIT, tooltip="Editar"),
                                ft.IconButton(ft.icons.DELETE, tooltip="Remover"),
                            ],
                            spacing=8,
                        )
                    ),
                ]
            )
        )

    table = ft.DataTable(
        columns=columns,
        rows=rows,
        column_spacing=20,
        heading_row_height=40,
        data_row_height=48,
    )

    # container responsivo que expande horizontalmente
    return ft.Container(content=table, expand=True, padding=8)
