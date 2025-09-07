import flet as ft

class ScheduleView:
    def __init__(self, page: ft.Page, role: str, current_user_id: int):
        self.page = page
        self.role = role
        self.current_user_id = current_user_id

    def build(self):
        # Here you would typically fetch the schedule data from the database
        # For demonstration, we will use a static example
        schedule_data = [
            {"day": "Monday", "time": "08:00 - 09:00", "subject": "Mathematics"},
            {"day": "Monday", "time": "09:00 - 10:00", "subject": "Physics"},
            {"day": "Tuesday", "time": "10:00 - 11:00", "subject": "Chemistry"},
            {"day": "Wednesday", "time": "08:00 - 09:00", "subject": "Biology"},
            {"day": "Thursday", "time": "09:00 - 10:00", "subject": "History"},
            {"day": "Friday", "time": "10:00 - 11:00", "subject": "Physical Education"},
        ]

        schedule_items = [
            ft.Row(
                [
                    ft.Text(item["day"]),
                    ft.Text(item["time"]),
                    ft.Text(item["subject"]),
                ],
                alignment="spaceBetween",
            )
            for item in schedule_data
        ]

        return ft.Column(
            [
                ft.Text("Teacher's Schedule", size=20, weight="bold"),
                ft.Divider(),
                *schedule_items,
            ],
            spacing=10,
            padding=20,
        )