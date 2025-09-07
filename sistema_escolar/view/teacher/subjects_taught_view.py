import flet as ft

class SubjectsTaughtView:
    def __init__(self, page: ft.Page, role: str, teacher_id: int):
        self.page = page
        self.role = role
        self.teacher_id = teacher_id

    def build(self):
        # Header
        header = ft.Text("Subjects Taught", size=24, weight="bold")

        # Placeholder for subjects list
        subjects_list = ft.Column()

        # Example subjects (this should be replaced with actual data retrieval)
        subjects = [
            {"name": "Mathematics", "code": "MATH101"},
            {"name": "Physics", "code": "PHYS101"},
            {"name": "Chemistry", "code": "CHEM101"},
        ]

        for subject in subjects:
            subjects_list.controls.append(
                ft.Row([
                    ft.Text(subject["name"]),
                    ft.Text(f"({subject['code']})", style="caption"),
                ])
            )

        # Main content
        content = ft.Column([
            header,
            ft.Divider(),
            subjects_list,
        ], spacing=10)

        return ft.Container(content=content, padding=20)