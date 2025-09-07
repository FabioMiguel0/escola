import flet as ft
from services.user_service import list_users
from services.permission_service import has_permission, grant_permission, revoke_permission

def UsersView(page: ft.Page, current_user: str = None):
    """
    Mostra um dropdown apenas com usuários cujo role == 'secretaria'.
    Ao selecionar um usuário, mostra uma matriz (roles x ações) indicando
    quais ações cada papel pode realizar.
    Proteções contra auto-rebaixamento já são tratadas no serviço.
    """
    page.auto_scroll = True

    usuarios = list_users()
    # filtra apenas secretarias (ajuste se quiser outro filtro)
    secretarias = [u for u in usuarios if (u.get("role") or "") == "secretaria"]

    if not secretarias:
        container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Usuários (Secretaria)", size=18),
                    ft.Divider(),
                    ft.Text("Não há usuários com papel 'secretaria' cadastrados.", color=ft.Colors.RED),
                    ft.Container(height=12),
                    ft.Text("Atribua o papel 'secretaria' a um usuário através da tela de Usuários (admin)."),
                ]
            ),
            expand=True,
            padding=12,
        )
        return container

    options = [ft.dropdown.Option(str(u["id"]), text=u["username"]) for u in secretarias]
    initial_value = str(secretarias[0]["id"])
    user_dd = ft.Dropdown(label="Selecionar secretário(a)", options=options, value=initial_value)

    info = ft.Text("", size=12)
    matricular_cb = ft.Checkbox(label="Permissão: Matricular alunos", value=False)
    save_perm_btn = ft.ElevatedButton("Aplicar permissão", on_click=lambda e: on_apply_permission(), width=160)

    def render_for_user(uid):
        u = next((x for x in secretarias if str(x["id"]) == str(uid)), None)
        if not u:
            info.value = "Usuário não encontrado"
            matricular_cb.value = False
        else:
            info.value = f"Selecionado: {u['username']}"
            matricular_cb.value = has_permission(u["id"], "matricular")
        page.update()

    def on_user_change(e):
        render_for_user(user_dd.value)

    def on_apply_permission():
        uid = int(user_dd.value)
        u = next((x for x in secretarias if x["id"] == uid), None)
        if not u:
            page.snack_bar = ft.SnackBar(ft.Text("Usuário inválido")); page.snack_bar.open = True; page.update(); return
        try:
            if matricular_cb.value:
                grant_permission(uid, "matricular")
            else:
                revoke_permission(uid, "matricular")
            page.snack_bar = ft.SnackBar(ft.Text("Permissão atualizada")); page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}")); page.snack_bar.open = True
        page.update()
        render_for_user(uid)

    render_for_user(initial_value)

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Usuários (Secretaria) — Permissões", size=18),
                ft.Divider(),
                user_dd,
                ft.Container(height=8),
                info,
                ft.Row([matricular_cb, save_perm_btn], spacing=12),
            ],
            expand=True,
            tight=True,
        ),
        expand=True,
        padding=12,
    )

    user_dd.on_change = on_user_change
    return container