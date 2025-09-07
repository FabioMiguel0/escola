import flet as ft
from services.user_service import list_users


def LoginView(page: ft.Page, go):
    page.window_width = 600
    page.window_height = 380
    page.scroll = "auto"

    users = list_users()

    # Controls
    title = ft.Text("Sistema Escolar", size=28, weight="bold")
    subtitle = ft.Text("Entre com seu usuário", size=12, color=ft.Colors.GREY)

    username = ft.TextField(label="Usuário", width=360, autofocus=True)
    password = ft.TextField(label="Senha (opcional)", password=True, can_reveal_password=True, width=360)

    # quick-select dropdown (preenche o campo username)
    if users:
        dd_options = [ft.dropdown.Option(str(u["id"]), text=f"{u['username']} ({u.get('role')})") for u in users]
        quick_dd = ft.Dropdown(label="Selecionar usuário (opcional)", options=dd_options, value=dd_options[0].key)
    else:
        quick_dd = ft.Dropdown(label="Selecionar usuário (opcional)", options=[], value=None)

    info = ft.Text("", size=12, color=ft.Colors.RED)

    def on_quick_change(e):
        try:
            uid = int(quick_dd.value)
            u = next((x for x in users if x["id"] == uid), None)
            if u:
                username.value = u["username"]
        except Exception:
            pass
        page.update()

    def on_enter(e):
        uname = (username.value or "").strip()
        if not uname:
            info.value = "Informe o nome de usuário" 
            page.update()
            return
        # procura usuário pelo username
        u = next((x for x in users if x["username"] == uname), None)
        if not u:
            info.value = "Usuário não encontrado"
            page.update()
            return
        # sucesso: navega para home passando id e role
        go("home", user=u["username"], role=u.get("role") or "aluno", user_id=u["id"])

    # Modern button (removido 'shape' — compatível com mais versões do flet)
    enter_btn = ft.ElevatedButton(
        "Entrar",
        on_click=on_enter,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=220,
        height=48,
    )

    # layout centralizado
    col = ft.Column(
        [
            title,
            subtitle,
            ft.Container(height=18),
            username,
            password,
            ft.Container(height=6),
            quick_dd,
            ft.Container(height=12),
            ft.Row([enter_btn], alignment="center"),
            ft.Container(height=8),
            info,
        ],
        horizontal_alignment="center",
        tight=True,
    )

    wrapper = ft.Container(
        content=ft.Column([col], alignment="center", horizontal_alignment="center"),
        alignment=ft.alignment.center,
        padding=24,
    )

    view = ft.View("/login", controls=[wrapper])
    return view
