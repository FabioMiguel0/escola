import flet as ft

class ClassesView:
    def __init__(self, page, role, current_user_id):
        self.page = page
        self.role = role
        self.current_user_id = current_user_id

    def build(self):
        # Here you would typically fetch the classes for the teacher from the database
        # For demonstration purposes, we'll use a static list of classes
        classes = [
            {"name": "Matemática", "time": "08:00 - 09:30"},
            {"name": "História", "time": "10:00 - 11:30"},
            {"name": "Ciências", "time": "13:00 - 14:30"},
        ]

        class_items = [
            ft.ListTile(title=ft.Text(cls["name"]), subtitle=ft.Text(cls["time"]))
            for cls in classes
        ]

        return ft.Column(
            controls=[
                ft.Text("Minhas Turmas", size=24, weight="bold"),
                ft.ListView(controls=class_items),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )