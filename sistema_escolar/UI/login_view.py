from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container

class LoginView:
    def __init__(self, page: Page, go):
        self.page = page
        self.go = go
        self.username_field = TextField(label="Username", autofocus=True)
        self.password_field = TextField(label="Password", password=True)
        self.login_button = ElevatedButton(text="Login", on_click=self.login)

    def build(self):
        return Container(
            content=Column(
                [
                    Text("Welcome to the Sistema Escolar", size=24, weight="bold"),
                    self.username_field,
                    self.password_field,
                    Row([self.login_button], alignment="center"),
                ],
                alignment="center",
                spacing=20,
            ),
            padding=20,
            alignment="center",
        )

    def login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        # Here you would typically validate the username and password
        # For now, we will just simulate a successful login
        if username and password:  # Replace with actual validation logic
            self.go("home", user=username, role="admin", user_id=1)  # Example role and user_id
        else:
            self.page.add(Text("Invalid username or password", color="red"))