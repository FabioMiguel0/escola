import os
import sys
import importlib
import traceback
import flet as ft

# garante imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# serviços e seed opcional
from services.db import create_tables_and_seed
try:
    seed = importlib.import_module("services.seed")
except ModuleNotFoundError:
    seed = None

from UI import LoginView
from UI.shell import Shell
from services.user_service import menu_for_role
from view.dashboard_view import DashboardView
from view.aluno_view import AlunoView
from view.professor_view import ProfessorView
from view.comunicado_view import ComunicadoView
from view.turma_view import TurmaView
from view.disciplina_view import DisciplinaView
from view.frequencia_view import FrequenciaView
from view.nota_view import NotaView
from view.documento_view import DocumentoView
from view.calendario_view import CalendarioView
from view.horarios_admin_view import HorariosAdmin


def main(page: ft.Page):
    page.title = "Sistema Escolar"
    page.window_width = 1200
    page.window_height = 800
    page.scroll = "auto"
    page.bgcolor = "#F8FAFC"

    # Configurações básicas
    try:
        page.theme_mode = ft.ThemeMode.LIGHT
    except Exception:
        pass
    page.padding = 0
    page.spacing = 0
    page.responsive = True
    page.adaptive = True
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }

    # limpa client storage se possível
    try:
        page.client_storage.clear()
    except Exception:
        pass

    # cria BD / seed (se disponível)
    try:
        create_tables_and_seed()
        if seed and hasattr(seed, "seed_all"):
            try:
                seed.seed_all()
            except Exception as ex:
                print("[SEED] seed_all failed:", ex)
    except Exception as ex:
        print("[DB] create_tables_and_seed error:", ex)

    # estado da aplicação
    state = {"user": None, "user_id": None, "role": None, "route": "login"}

    permissions = {
        "admin": {"dashboard", "usuarios", "professores", "disciplinas", "turmas", "alunos", "documentos", "comunicados", "calendario", "frequencia", "notas"},
        "secretaria": {"dashboard", "alunos", "turmas", "documentos", "comunicados", "calendario", "disciplinas"},
        "professor": {"dashboard", "frequencia", "notas", "comunicados", "minhas_turmas", "horario", "minhas_disciplinas", "documentos"},
        "aluno": {"perfil", "desempenho", "boletim", "horario"},
        "responsavel": {"dashboard", "comunicados", "calendario"},
        "suporte": {"dashboard"},
    }

    shell = None

    def build_content():
        r = state.get("route", "dashboard")
        role = state.get("role")
        try:
            if r == "login":
                return LoginView(page, go=go)
            if r == "home":
                r = "dashboard"
                state["route"] = r
                role = state.get("role")
            if r == "dashboard":
                return DashboardView(page, role=role, username=state.get("user"), go=go)
            if r == "alunos":
                return AlunoView(page, role=role, current_user_id=state.get("user_id"))
            if r == "turmas":
                return TurmaView(page, role=role)
            if r == "professores":
                return ProfessorView(page, role=role, current_user_id=state.get("user_id"))
            if r == "disciplinas":
                return DisciplinaView(page)
            if r == "notas":
                return NotaView(page, role=role, aluno_id=state.get("user_id"))
            if r == "frequencia":
                return FrequenciaView(page)
            if r == "documentos":
                return DocumentoView(page, user=state.get("user"), role=state.get("role"), user_id=state.get("user_id"))
            if r == "comunicados":
                return ComunicadoView(page)
            if r == "calendario":
                return CalendarioView(page)
            if r == "horarios_admin":
                return HorariosAdmin(page)
            return ft.Container(content=ft.Text(f"Tela '{r}' em construção..."), expand=True)
        except Exception as ex:
            tb = traceback.format_exc()
            print("[BUILD_CONTENT] exception:", tb)
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Erro interno ao construir a view", color=ft.Colors.RED, weight="bold"),
                        ft.Text(str(ex)),
                        ft.Divider(),
                        ft.Text(tb, selectable=True, size=10),
                    ]
                ),
                expand=True,
                padding=12,
            )

    def build_shell():
        nonlocal shell
        shell = Shell(
            page=page,
            username=state.get("user") or "Usuário",
            role=state.get("role") or "aluno",
            current_route=state.get("route") or "dashboard",
            on_route_change=go,
            content_builder=lambda: build_content()
        )
        return shell.build()

    def go(view: str, user=None, role=None, user_id=None):
        if user is not None:
            state["user"] = user
        if role is not None:
            state["role"] = role
        if user_id is not None:
            state["user_id"] = user_id
        if view == "logout":
            state["user"] = None
            state["role"] = None
            state["user_id"] = None
            view = "login"
        state["route"] = view

        try:
            page.views.clear()
            page.views.append(build_shell())
            page.update()
        except Exception as ex:
            tb = traceback.format_exc()
            print("[GO] error building shell:", tb)
            page.views.clear()
            page.views.append(ft.View("/", controls=[ft.Text(f"Erro ao construir UI: {ex}")]))
            page.update()

    # inicialização: evita tela em branco
    try:
        page.views.clear()
        page.views.append(ft.View("/", controls=[ft.Text("Carregando...")]))
        page.update()
    except Exception:
        pass

    # auto-login para desenvolvimento
    if os.environ.get("AUTO_LOGIN") == "1":
        state.update({"user": "admin", "role": "admin", "user_id": 1, "route": "dashboard"})
        page.views.clear()
        page.views.append(build_shell())
        page.update()
    else:
        go("login")


if __name__ == "__main__":
    # no Render: usar PORT env e view web
    port_env = os.environ.get("PORT")
    if port_env:
        try:
            port = int(port_env)
        except Exception:
            port = 8000
        print(f"[START] running web on port={port}")
        ft.app(target=main, view=ft.WEB_BROWSER, port=port, address="0.0.0.0")
    else:
        # execução local: prefere janela nativa
        print("[START] running locally (native window preferred)")
        try:
            ft.app(target=main)
        except Exception as ex:
            print("[START] native start failed, falling back to web browser mode:", ex)
            ft.app(target=main, view=ft.WEB_BROWSER)