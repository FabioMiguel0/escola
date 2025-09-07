import os
import sys
import flet as ft

# garante imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db import create_tables_and_seed
from UI import LoginView, Shell   
from services.user_service import menu_for_role
from view.dashboard_view import DashboardView
from view.student.grades_view import GradesView
from view.student.subjects_view import SubjectsView
from view.student.performance_view import PerformanceView
from view.student.report_card_view import ReportCardView
from view.teacher.classes_view import ClassesView
from view.teacher.schedule_view import ScheduleView
from view.teacher.subjects_taught_view import SubjectsTaughtView


def main(page: ft.Page):
    page.title = "Sistema Escolar"
    page.window_width = 1100
    page.window_height = 700
    page.scroll = "auto"

    create_tables_and_seed()

    state = {"user": None, "user_id": None, "role": None, "route": "dashboard"}

    permissions = {
        "admin": {"dashboard", "usuarios", "professores", "disciplinas", "turmas", "alunos", "documentos", "comunicados", "calendario", "frequencia", "notas"},
        "secretaria": {"dashboard", "alunos", "turmas", "documentos", "comunicados", "calendario", "disciplinas"},
        "professor": {"dashboard", "frequencia", "notas", "comunicados", "classes", "schedule", "subjects_taught"},
        "aluno": {"dashboard", "grades", "subjects", "performance", "report_card", "notas", "comunicados", "calendario"},
        "responsavel": {"dashboard", "comunicados", "calendario"},
        "suporte": {"dashboard"},
    }

    def build_content():
        r = state.get("route", "dashboard")
        role = state.get("role")
        print(f"[BUILD_CONTENT] route={r} role={role}")
        try:
            if r == "dashboard":
                return DashboardView(page, role=role, username=state.get("user"), go=go)
            if r == "grades":
                return GradesView(page, aluno_id=state.get("user_id"))
            if r == "subjects":
                return SubjectsView(page, aluno_id=state.get("user_id"))
            if r == "performance":
                return PerformanceView(page, aluno_id=state.get("user_id"))
            if r == "report_card":
                return ReportCardView(page, aluno_id=state.get("user_id"))
            if r == "classes":
                return ClassesView(page, role=role)
            if r == "schedule":
                return ScheduleView(page, role=role)
            if r == "subjects_taught":
                return SubjectsTaughtView(page, role=role)
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
        if user is not None:
            state["user"] = user
        if role is not None:
            state["role"] = role
        if user_id is not None:
            state["user_id"] = user_id

        page.views.clear()

        if view == "login":
            page.views.append(LoginView(page, go))
            if not state.get("route"):
                state["route"] = "dashboard"
            page.update()
            return

        if view == "home":
            if not state.get("route"):
                state["route"] = "dashboard"

            def on_route_change(new_route: str):
                if new_route == "logout":
                    state["user"] = None
                    state["user_id"] = None
                    state["role"] = None
                    go("login")
                    return
                allowed = permissions.get(state.get("role", "aluno"), {"dashboard"})
                if new_route not in allowed:
                    state["route"] = "dashboard"
                else:
                    state["route"] = new_route
                go("home")

            try:
                page.views.append(
                    Shell(
                        page,
                        username=state.get("user") or "Usuário",
                        role=state.get("role") or "aluno",
                        on_route_change=on_route_change,
                        content_builder=build_content,
                    ).build()
                )
            except Exception as ex:
                page.views.append(ft.View("/error", controls=[ft.Column([ft.Text("Erro interno:"), ft.Text(str(ex))])]))

            try:
                go_to = page.client_storage.get("go_to")
                if go_to:
                    page.client_storage.set("go_to", None)
                    on_route_change(go_to)
            except Exception:
                pass

            page.update()
            return

        state["route"] = view
        go("home")

    if os.environ.get("AUTO_LOGIN") == "1":
        go("home", user="admin", role="admin", user_id=1)
    else:
        go("login")


if __name__ == "__main__":
    ft.app(target=main)