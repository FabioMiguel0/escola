from flet import Column, Row, Text, AppBar, IconButton, icons, View

class Shell:
    def __init__(self, page, username, role, on_route_change, content_builder):
        self.page = page
        self.username = username
        self.role = role
        self.on_route_change = on_route_change
        self.content_builder = content_builder

    def build(self):
        return View(
            controls=[
                AppBar(
                    title=Text("Sistema Escolar"),
                    leading=IconButton(icons.menu, on_click=self.open_menu),
                    trailing=[
                        IconButton(icons.logout, on_click=self.logout),
                    ],
                ),
                Column(
                    [
                        Row(
                            [
                                Text(f"Bem-vindo, {self.username}"),
                                Text(f"Função: {self.role}"),
                            ],
                            alignment="spaceBetween",
                        ),
                        self.content_builder(),
                    ]
                ),
            ]
        )

    def open_menu(self, e):
        # Logic to open the navigation menu
        pass

    def logout(self, e):
        self.on_route_change("logout")