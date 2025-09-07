from flet import Column, Text, Container, Page

def GradesView(page: Page, aluno_id: int):
    # This function creates the view for students to see their grades
    grades = get_grades_for_student(aluno_id)  # Assume this function fetches grades from the database

    return Container(
        content=Column(
            [
                Text("Suas Notas", size=24, weight="bold"),
                *[Text(f"Disciplina: {grade['subject']}, Nota: {grade['grade']}") for grade in grades],
            ]
        ),
        padding=20,
        expand=True,
    )

def get_grades_for_student(aluno_id: int):
    # Placeholder function to simulate fetching grades from a database
    return [
        {"subject": "Matemática", "grade": "A"},
        {"subject": "História", "grade": "B"},
        {"subject": "Ciências", "grade": "A"},
    ]