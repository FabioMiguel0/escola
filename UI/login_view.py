import flet as ft

def LoginView(page: ft.Page, go):
    page.auto_scroll = True
    user_field = ft.TextField(
        label="Usuário",
        border_radius=12,
        border_color="#D1D5DB",
        focused_border_color="#3B82F6",
        label_style=ft.TextStyle(color="#6B7280", weight="w500"),
    )
    pwd_field = ft.TextField(
        label="Senha", 
        password=True, 
        can_reveal_password=True,
        border_radius=12,
        border_color="#D1D5DB",
        focused_border_color="#3B82F6",
        label_style=ft.TextStyle(color="#6B7280", weight="w500"),
    )
    msg = ft.Text("", color="#EF4444", size=14)

    def on_login(e):
        username = (user_field.value or "").strip()
        # autenticação de teste: ajusta para usar user_service se desejar
        if username == "aluno":
            go("dashboard", user=username, role="aluno", user_id=2)
        elif username == "professor":
            go("dashboard", user=username, role="professor", user_id=3)
        elif username == "admin":
            go("dashboard", user=username, role="admin", user_id=1)
        else:
            msg.value = "Credenciais inválidas (use aluno/professor/admin)"
            page.update()

    login_btn = ft.ElevatedButton(
        "Entrar", 
        on_click=on_login,
        style=ft.ButtonStyle(
            bgcolor="#3B82F6", 
            color=ft.Colors.WHITE, 
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.padding.symmetric(horizontal=32, vertical=16),
        ),
        width=320,
    )
    
    # Card de login moderno
    login_card = ft.Container(
        content=ft.Column([
            # Header do card
            ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.SCHOOL, size=48, color="#3B82F6"),
                    bgcolor="#3B82F615",
                    border_radius=16,
                    padding=16,
                ),
                ft.Text("Sistema Escolar", size=24, weight="bold", color="#1F2937"),
                ft.Text("Faça login para continuar", size=16, color="#6B7280"),
            ], horizontal_alignment="center", spacing=12),
            
            ft.Divider(height=1, color="#E5E7EB"),
            
            # Formulário
            ft.Column([
                user_field,
                pwd_field,
                login_btn,
                msg,
            ], spacing=16),
        ], spacing=20),
        padding=32,
        width=400,
        bgcolor="#FFFFFF",
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, color="#00000020", offset=ft.Offset(0, 8)),
        border=ft.border.all(1, "#E5E7EB"),
    )
    
    # Container centralizado horizontal e verticalmente
    container = ft.Container(
        content=ft.Row([
            ft.Container(expand=True),  # Espaço à esquerda
            ft.Column([
                ft.Container(expand=True),  # Espaço acima
                login_card,
                ft.Container(expand=True),  # Espaço abaixo
            ], horizontal_alignment="center"),
            ft.Container(expand=True),  # Espaço à direita
        ]),
        expand=True,
        bgcolor="#F9FAFB",
        padding=20,
    )
    
    return container