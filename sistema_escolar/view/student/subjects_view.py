from flet import Column, Text, Container, Page

def SubjectsView(page: Page, role: str, current_user_id: int):
    # This function creates the view for students to see their subjects
    subjects = get_subjects_for_student(current_user_id)  # Assume this function fetches subjects from the database

    return Container(
        content=Column(
            [
                Text("Suas Disciplinas", size=24, weight="bold"),
                *[Text(subject, size=18) for subject in subjects],
            ],
            alignment="start",
            spacing=10,
        ),
        padding=20,
        expand=True,
    )

def get_subjects_for_student(student_id: int):
    # Placeholder function to simulate fetching subjects from a database
    return ["Matemática", "Português", "História", "Ciências"]  # Example subjects