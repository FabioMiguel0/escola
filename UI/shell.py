import flet as ft
from services.user_service import menu_for_role

class Shell:
    def __init__(self, page: ft.Page, username="Usuário", role="aluno", current_route=None, on_route_change=None, content_builder=None):
        self.page = page
        self.username = username
        self.role = role
        self.current_route = current_route
        self.on_route_change = on_route_change
        self.content_builder = content_builder

        # estado UI responsiva
        self._menu_open = False
        
        # Função para detectar tamanho da tela
        def get_screen_width():
            try:
                return getattr(page, "window_width", 1200)
            except:
                return 1200
        
        self.get_screen_width = get_screen_width

        # reconstrói a UI quando a janela for redimensionada
        def _on_resize(e):
            if callable(self.on_route_change):
                # força rebuild chamando a função de rota actual
                self.on_route_change(self.current_route)
        # ligar handler (main.go irá rebuild via on_route_change)
        try:
            self.page.on_resize = _on_resize
        except Exception:
            pass

    def _on_route_click(self, route: str):
        # fecha menu em mobile ao navegar
        self._menu_open = False
        if callable(self.on_route_change):
            self.on_route_change(route)

    def _build_nav_items(self):
        items = []
        
        screen_width = self.get_screen_width()
        is_mobile = screen_width < 768
        is_tablet = 768 <= screen_width < 1024
        
        # Mapeamento de ícones para cada rota
        icon_map = {
            "dashboard": ft.Icons.DASHBOARD,
            "alunos": ft.Icons.SCHOOL,
            "professores": ft.Icons.PERSON,
            "turmas": ft.Icons.GROUP,
            "disciplinas": ft.Icons.BOOK,
            "notas": ft.Icons.GRADE,
            "frequencia": ft.Icons.CHECK_CIRCLE,
            "comunicados": ft.Icons.ANNOUNCEMENT,
            "documentos": ft.Icons.DESCRIPTION,
            "calendario": ft.Icons.CALENDAR_TODAY,
            "usuarios": ft.Icons.PEOPLE,
            "perfil": ft.Icons.PERSON,
            "desempenho": ft.Icons.TRENDING_UP,
            "boletim": ft.Icons.ASSIGNMENT,
            "horario": ft.Icons.SCHEDULE,
            "minhas_turmas": ft.Icons.GROUP,
            "minhas_disciplinas": ft.Icons.SUBJECT,
        }
        
        # Tamanhos responsivos
        icon_size = 16 if is_mobile else 20
        text_size = 12 if is_mobile else 14
        padding_horizontal = 12 if is_mobile else 16
        padding_vertical = 10 if is_mobile else 12
        spacing = 8 if is_mobile else 12
        
        for route, label in menu_for_role(self.role):
            icon = icon_map.get(route, ft.Icons.CIRCLE)
            is_active = route == self.current_route
            bg_color = "#3B82F6" if is_active else "transparent"
            text_color = "#FFFFFF" if is_active else "#374151"
            icon_color = "#FFFFFF" if is_active else "#6B7280"
            
            items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, size=icon_size, color=icon_color),
                        ft.Text(label, 
                               size=text_size,
                               color=text_color, 
                               weight="bold" if is_active else "normal"),
                    ], spacing=spacing),
                    padding=ft.padding.symmetric(horizontal=padding_horizontal, vertical=padding_vertical),
                    border_radius=12,
                    bgcolor=bg_color,
                    on_click=lambda e, r=route: self._on_route_click(r),
                )
            )
        
        # Separador e logout
        items.append(ft.Divider(height=1, color="#E5E7EB"))
        items.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EXIT_TO_APP, size=20, color="#6B7280"),
                    ft.Text("Sair", color="#374151"),
                ], spacing=12),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                on_click=lambda e: self._on_route_click("logout"),
            )
        )
        return items

    def _get_window_width(self):
        # tenta várias propriedades para compatibilidade
        try:
            w = getattr(self.page, "window_width", None)
            if w:
                return w
            if hasattr(self.page, "client_size") and getattr(self.page.client_size, "width", None):
                return self.page.client_size.width
        except Exception:
            pass
        return 1000

    def build(self):
        # constrói o conteúdo principal usando content_builder
        try:
            content_control = self.content_builder() if callable(self.content_builder) else self.content_builder
        except Exception as ex:
            content_control = ft.Text(f"Erro ao construir conteúdo: {ex}")

        # largura actual do ecrã
        w = self._get_window_width()
        narrow = w < 900    # breakpoint: mobile/tablet
        is_mobile = w < 768
        is_tablet = 768 <= w < 1024

        # se estivermos na tela de login, não mostrar a barra lateral — centrar o conteúdo
        if self.current_route == "login":
            # calcula width responsivo para o formulário de login
            login_w = int(min(560, max(320, w * 0.8)))
            centered = ft.Column(
                [
                    ft.Container(content=content_control, width=login_w)
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
            return ft.View("/", controls=[centered])

        # navegação (lista de botões)
        nav_items = self._build_nav_items()
        nav_column = ft.Column(
            [
                # Header da sidebar responsivo
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.SCHOOL, 
                                              size=20 if is_mobile else 24, 
                                              color="#FFFFFF"),
                                bgcolor="#3B82F6",
                                border_radius=12,
                                padding=8 if is_mobile else 12,
                            ),
                            ft.Text("Sistema Escolar", 
                                   size=14 if is_mobile else 18, 
                                   weight="bold", color="#1F2937"),
                        ], spacing=8 if is_mobile else 12),
                        ft.Text(f"Olá, {self.username}", 
                               size=12 if is_mobile else 14, 
                               color="#6B7280", weight="w500"),
                    ], spacing=6 if is_mobile else 8),
                    padding=16 if is_mobile else 20,
                    bgcolor="#F9FAFB",
                ),
                # Itens do menu responsivos
                ft.Container(
                    content=ft.Column(nav_items, spacing=4, scroll=ft.ScrollMode.AUTO),
                    padding=ft.padding.symmetric(horizontal=12 if is_mobile else 16, vertical=8),
                    expand=True,
                ),
            ],
            spacing=0,
            tight=True,
        )

        # layout para ecrãs largos: sidebar fixa + conteúdo expansível
        if not narrow:
            sidebar_width = 240 if is_mobile else (260 if is_tablet else 280)
            nav = ft.Container(
                content=nav_column, 
                width=sidebar_width, 
                bgcolor="#FFFFFF",
                shadow=ft.BoxShadow(blur_radius=8, color="#00000010", offset=ft.Offset(2, 0)),
            )
            content_view = ft.Container(
                expand=True, 
                padding=16 if is_mobile else 20, 
                content=content_control,
                bgcolor="#F9FAFB"
            )
            view = ft.View(
                "/",
                controls=[
                    ft.Row(
                        [
                            nav,
                            ft.VerticalDivider(width=1, thickness=1, color="#E5E7EB"),
                            content_view,
                        ],
                        expand=True,
                    )
                ],
            )
            return view

        # layout para ecrãs estreitos: top bar + opcional menu expansível
        # construir AppBar (simples)
        menu_btn = ft.IconButton(ft.icons.MENU, on_click=self._toggle_menu)
        title = ft.Text("Sistema Escolar", weight="bold")
        top_bar = ft.Row([menu_btn, title], alignment="start")

        # menu móvel: mostrado acima do conteúdo quando self._menu_open = True
        mobile_menu = ft.Column(nav_items, visible=self._menu_open, spacing=0, scroll="auto")

        content_view = ft.Container(expand=True, padding=12, content=content_control)
        view = ft.View(
            "/",
            controls=[
                ft.Column(
                    [
                        top_bar,
                        ft.Divider(),
                        mobile_menu,
                        content_view,
                    ],
                    spacing=8,
                    expand=True,
                )
            ],
        )
        return view

    def _toggle_menu(self, e=None):
        # alterna menu e força rebuild via on_route_change para refletir mudança
        self._menu_open = not self._menu_open
        if callable(self.on_route_change):
            self.on_route_change(self.current_route)
