import os
import sys
import flet as ft

# garante imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuração simplificada para Render

from services.db import create_tables_and_seed
import importlib
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
from view.users_view import UsersView
from view.student.performance_view import PerformanceView
from view.student.report_card_view import ReportCardView
from view.student.grades_view import GradesView
from view.student.profile_view import ProfileView  # <<< novo import
from view.teacher.classes_view import ClassesView
from view.teacher.schedule_view import ScheduleView
from view.teacher.subjects_taught_view import SubjectsTaughtView


def main(page: ft.Page):
    page.title = "Sistema Escolar"
    page.window_width = 1200
    page.window_height = 800
    page.scroll = "auto"
    page.bgcolor = "#F8FAFC"
    
    # Configurações para mobile e compatibilidade
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    
    # Configurações responsivas
    page.responsive = True
    page.adaptive = True
    
    # Configurações para melhor compatibilidade
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }
    
    # Configurações de performance
    page.client_storage.clear()
    
    # Headers para melhor compatibilidade
    try:
        page.client_storage.set("app_version", "1.0.0")
        page.client_storage.set("device_type", "unknown")
    except:
        pass

    create_tables_and_seed()

    state = {"user": None, "user_id": None, "role": None, "route": "dashboard"}

    permissions = {
        "admin": {"dashboard", "usuarios", "professores", "disciplinas", "turmas", "alunos", "documentos", "comunicados", "calendario", "frequencia", "notas"},
        "secretaria": {"dashboard", "alunos", "turmas", "documentos", "comunicados", "calendario", "disciplinas"},
        "professor": {"dashboard", "frequencia", "notas", "comunicados", "minhas_turmas", "horario", "minhas_disciplinas", "documentos"},  # ADICIONADO 'documentos'
        # aluno: agora tem rota "perfil" que agrega tudo (mantive também as rotas separadas)
        "aluno": {"perfil", "desempenho", "boletim", "horario"},
        "responsavel": {"dashboard", "comunicados", "calendario"},
        "suporte": {"dashboard"},
    }

    # mantemos um shell reconstruível que recebe current_route e on_route_change
    shell = None

    def build_shell(page, state, build_content):
        global shell
        shell = Shell(
            page=page,
            username=state.get("user") or "Usuário",
            role=state.get("role") or "aluno",
            current_route=state.get("route") or "dashboard",
            on_route_change=go,
            content_builder=lambda: build_content()
        )
        return shell.build()

    def build_content():
        # retorna um control (container) conforme state["route"]
        r = state.get("route", "dashboard")
        role = state.get("role")
        print(f"[BUILD_CONTENT] route={r} role={role}")
        try:
            # página de login (quando não autenticado ou após logout)
            if r == "login":
                # LoginView deve aceitar o parâmetro 'go' para notificar main.go quando o login for feito.
                return LoginView(page, go=go)
            # opcional: rota 'home' mapeada para dashboard
            if r == "home":
                r = "dashboard"
                state["route"] = r
                role = state.get("role")
            # resto das rotas continua abaixo
            if r == "dashboard":
                return DashboardView(page, role=role, username=state.get("user"), go=go)
            # se aluno clicou em "notas" (menu antigo) redireciona para perfil
            if r == "notas" and role == "aluno":
                return ProfileView(page, aluno_id=state.get("user_id"))
            if r == "perfil":
                return ProfileView(page, aluno_id=state.get("user_id"))
            if r == "usuarios":
                # passa o usuário logado para que ele não possa rebaixar a si mesmo
                return UsersView(page, current_user=state.get("user"))
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
            if r == "desempenho":
                return PerformanceView(page, aluno_id=state.get("user_id"))
            if r == "boletim":
                return ReportCardView(page, aluno_id=state.get("user_id"))
            if r == "minhas_turmas":
                return ClassesView(page, role=role, current_user_id=state.get("user_id"))
            if r == "horario":
                return ScheduleView(page, role=role, current_user_id=state.get("user_id"))
            if r == "minhas_disciplinas":
                return SubjectsTaughtView(page, role=role, current_user_id=state.get("user_id"))
            if r == "frequencia":
                return FrequenciaView(page)
            if r == "comunicados":
                return ComunicadoView(page)
            if r == "documentos":
                return DocumentoView(page, user=state.get("user"), role=state.get("role"), user_id=state.get("user_id"))
            if r == "calendario":
                return CalendarioView(page)
            # fallback
            return ft.Container(content=ft.Text(f"Tela '{r}' em construção..."), expand=True)
        except Exception as ex:
            import traceback
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

    def go(view: str, user=None, role=None, user_id=None):
        # atualiza estado se fornecido
        if user is not None:
            state["user"] = user
        if role is not None:
            state["role"] = role
        if user_id is not None:
            state["user_id"] = user_id

        # trata logout: limpa estado e mostra login
        if view == "logout":
            state["user"] = None
            state["role"] = None
            state["user_id"] = None
            view = "login"
        
        # define a rota actual e reconstrói o shell/content
        state["route"] = view

        # limpa views e cria novamente o shell com route atual (assim o item activo é destacado)
        page.views.clear()
        try:
            page.views.append(build_shell(page, state, build_content))
        except Exception as ex:
            # fallback minimal para mostrar erro na UI
            page.views.append(ft.View("/", controls=[ft.Text(f"Erro ao construir UI: {ex}")]))
        page.update()

    # inicia com login se não houver user, ou com home se AUTO_LOGIN
    if os.environ.get("AUTO_LOGIN") == "1":
        go("home", user="admin", role="admin", user_id=1)
    else:
        # Renderiza algo imediatamente para evitar tela em branco enquanto carrega
        try:
            page.views.clear()
            page.views.append(ft.View("/", controls=[ft.Text("Carregando...")]))
            page.update()
        except Exception:
            pass
        go("login")


def build(page: ft.Page):
    # estado simples
    state = {"user": None, "role": "aluno", "user_id": None, "route": "login"}

    def view_for_route(route):
        # devolve um control / Container para a rota atual
        # ...existing code...
        if route == "login":
            return LoginView(page, on_login=on_login)
        if route == "documentos":
            return DocumentoView(page, user=state.get("user"), role=state.get("role"), user_id=state.get("user_id"))
        if route == "comunicados":
            return ComunicadoView(page, user=state.get("user"))
        # default
        return ft.Text("Rota não implementada")

    def go(route, **kwargs):
        state.update(kwargs)
        state["route"] = route
        # content_builder precisa ser callable que devolve o control da view central
        content_builder = lambda: view_for_route(route)
        shell = Shell(page,
                      username=state.get("user") or "Usuário",
                      role=state.get("role"),
                      current_route=state.get("route"),
                      on_route_change=go,
                      content_builder=content_builder)
        page.views.clear()
        page.views.append(shell.build())
        page.update()

    # handler de login que define estado e navega
    def on_login(user, role, user_id):
        state["user"], state["role"], state["user_id"] = user, role, user_id
        go("dashboard")

    # inicía na rota guardada
    go(state["route"])
if __name__ == "__main__":
    # Configuração SIMPLES e DEFINITIVA para Render
    env_port = os.environ.get("PORT")
    # Em produção (PORT definido), seguimos web. Localmente, abrimos como app desktop (sem browser)
    port = int(env_port) if env_port else None
    
    print("=" * 50)
    print("🚀 INICIANDO SISTEMA ESCOLAR")
    print("=" * 50)
    print(f"Porta: {port if port is not None else 'N/A (desktop)'}")
    print(f"Ambiente: {'RENDER' if os.environ.get('PORT') else 'LOCAL-DESKTOP'}")
    
    # Web em produção; desktop localmente
    if os.environ.get("PORT"):
        # Produção / Web
        try:
            ft.app(
                target=main,
                view=ft.WEB_BROWSER,
                port=port,
                host="0.0.0.0",
                web_renderer=ft.WebRenderer.CANVAS_KIT,
                assets_dir="assets",
                route_url_strategy="path",
                use_color_emoji=True
            )
        except OSError as ex:
            if "10048" in str(ex) or "address already in use" in str(ex).lower():
                print("Porta em uso. Tentando iniciar com uma porta aleatória livre...")
                ft.app(
                    target=main,
                    view=ft.WEB_BROWSER,
                    port=0,
                    host="0.0.0.0",
                    web_renderer=ft.WebRenderer.CANVAS_KIT,
                    assets_dir="assets",
                    route_url_strategy="path",
                    use_color_emoji=True
                )
            else:
                raise
    else:
        # Desktop (sem navegador)
        ft.app(
            target=main,
            view=ft.FLET_APP,
            assets_dir="assets",
            use_color_emoji=True
        )
