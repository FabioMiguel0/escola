import flet as ft
from services.aluno_service import count_alunos
from services.turma_service import count_turmas
from services.professor_service import count_professores


def DashboardView(page: ft.Page, role=None, username=None, go=None):
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
    
    # obtém contagens se as funções existirem
    try:
        alunos_count = str(count_alunos() or 0)
    except Exception:
        alunos_count = "—"
    try:
        turmas_count = str(count_turmas() or 0)
    except Exception:
        turmas_count = "—"
    try:
        prof_count = str(count_professores() or 0)
    except Exception:
        prof_count = "—"

    # Header responsivo
    header = ft.Container(
        content=ft.Column([
            ft.Text(f"Bem-vindo, {username or 'Usuário'}!", 
                   size=20 if is_mobile else 24, 
                   weight="bold", color="#1F2937"),
        ], spacing=4),
        padding=ft.padding.only(bottom=16 if is_mobile else 24),
    )

    # Cards responsivos
    def create_metric_card(title, value, icon, color, bg_color):
        card_width = 280 if is_mobile else (320 if is_tablet else 300)
        card_height = 130 if is_mobile else 150
        icon_size = 20 if is_mobile else 24
        value_size = 28 if is_mobile else 36
        title_size = 13 if is_mobile else 14
        padding = 18 if is_mobile else 22
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=icon_size, color=color),
                        bgcolor=f"{color}15",
                        border_radius=12,
                        padding=10 if is_mobile else 12,
                    ),
                    ft.Text(title, size=title_size, color="#6B7280", weight="w500", expand=True),
                ], alignment="spaceBetween"),
                ft.Text(value, size=value_size, weight="bold", color="#1F2937"),
            ], spacing=10 if is_mobile else 12, tight=True),
            padding=padding,
            width=card_width,
            height=card_height,
            bgcolor=bg_color,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=8, color="#00000010", offset=ft.Offset(0, 4)),
            border=ft.border.all(1, "#E5E7EB"),
        )

    # Layout responsivo dos cards - apenas para administradores
    if role == "admin":
        if is_mobile:
            cards = ft.Column(
                [
                    create_metric_card("Total de Alunos", alunos_count, ft.Icons.SCHOOL, "#3B82F6", "#FFFFFF"),
                    create_metric_card("Turmas Ativas", turmas_count, ft.Icons.GROUP, "#10B981", "#FFFFFF"),
                    create_metric_card("Professores", prof_count, ft.Icons.PERSON, "#F59E0B", "#FFFFFF"),
                ],
                spacing=16,
            )
        else:
            cards = ft.Row(
                [
                    create_metric_card("Total de Alunos", alunos_count, ft.Icons.SCHOOL, "#3B82F6", "#FFFFFF"),
                    create_metric_card("Turmas Ativas", turmas_count, ft.Icons.GROUP, "#10B981", "#FFFFFF"),
                    create_metric_card("Professores", prof_count, ft.Icons.PERSON, "#F59E0B", "#FFFFFF"),
                ],
                alignment="start",
                spacing=16 if is_tablet else 20,
                wrap=True,
            )
    else:
        # Para outros roles, não mostrar cards de métricas
        cards = ft.Container()

    # Ações rápidas responsivas baseadas no role
    def create_action_button(text, icon, color, route):
        button_width = 300 if is_mobile else (220 if is_tablet else 200)
        text_size = 13 if is_mobile else 14
        icon_size = 18 if is_mobile else 20
        padding_h = 20 if is_mobile else 16
        padding_v = 14 if is_mobile else 12
        
        return ft.ElevatedButton(
            text, 
            icon=icon, 
            on_click=lambda e: go(route),
            style=ft.ButtonStyle(
                bgcolor=color, 
                color=ft.Colors.WHITE, 
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.padding.symmetric(horizontal=padding_h, vertical=padding_v),
            ),
            width=button_width,
            height=50 if is_mobile else 45,
        )
    
    quick_actions = []
    if role == "admin":
        quick_actions = [
            create_action_button("Gerenciar Usuários", ft.Icons.PEOPLE, "#3B82F6", "usuarios"),
            create_action_button("Adicionar Professor", ft.Icons.PERSON_ADD, "#10B981", "professores"),
            create_action_button("Criar Turma", ft.Icons.ADD, "#8B5CF6", "turmas"),
        ]
    elif role == "secretaria":
        quick_actions = [
            create_action_button("Matricular Aluno", ft.Icons.SCHOOL, "#3B82F6", "alunos"),
            create_action_button("Gerenciar Turmas", ft.Icons.GROUP, "#10B981", "turmas"),
            create_action_button("Enviar Comunicado", ft.Icons.ANNOUNCEMENT, "#F59E0B", "comunicados"),
        ]
    elif role == "professor":
        quick_actions = [
            create_action_button("Minhas Turmas", ft.Icons.GROUP, "#3B82F6", "minhas_turmas"),
            create_action_button("Lançar Notas", ft.Icons.GRADE, "#10B981", "notas"),
            create_action_button("Controle de Frequência", ft.Icons.CHECK_CIRCLE, "#F59E0B", "frequencia"),
        ]
    elif role == "aluno":
        quick_actions = [
            create_action_button("Meu Perfil", ft.Icons.PERSON, "#3B82F6", "perfil"),
            create_action_button("Ver Notas", ft.Icons.GRADE, "#10B981", "perfil"),
            create_action_button("Meu Horário", ft.Icons.SCHEDULE, "#8B5CF6", "horario"),
        ]

    # Card de ações rápidas responsivo
    if quick_actions:
        if is_mobile:
            actions_layout = ft.Column(quick_actions, spacing=12)
        else:
            actions_layout = ft.Row(quick_actions, spacing=16, wrap=True)
    else:
        actions_layout = ft.Text("Nenhuma ação disponível", color="#6B7280")
    
    actions_card = ft.Container(
        content=ft.Column([
            ft.Text("Ações Rápidas", 
                   size=16 if is_mobile else 18, 
                   weight="bold", color="#1F2937"),
            actions_layout,
        ], spacing=16),
        padding=16 if is_mobile else 20,
        bgcolor="#FFFFFF",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=8, color="#00000010", offset=ft.Offset(0, 4)),
        border=ft.border.all(1, "#E5E7EB"),
    )

    body = ft.Column([
        header,
        cards,
        ft.Container(height=16 if is_mobile else 24),
        actions_card,
    ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)

    return ft.Container(
        content=body, 
        expand=True, 
        padding=16 if is_mobile else 20
    )
