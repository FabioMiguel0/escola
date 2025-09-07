from flet import Column, Text, Container, Page

def ReportCardView(page: Page, student_id: int):
    # This function will create the report card view for the student
    # Here you would typically fetch the student's report card data from the database
    # For demonstration purposes, we will use a placeholder text

    report_card_data = {
        "student_name": "John Doe",
        "grades": {
            "Math": "A",
            "Science": "B+",
            "History": "A-",
            "English": "B",
        },
        "average": "B+",
    }

    # Create the report card layout
    report_card_content = Column(
        controls=[
            Text(f"Report Card for {report_card_data['student_name']}", size=24, weight="bold"),
            Text("Grades:", size=20),
            *[Text(f"{subject}: {grade}") for subject, grade in report_card_data["grades"].items()],
            Text(f"Average Grade: {report_card_data['average']}", size=20),
        ]
    )

    return Container(content=report_card_content, padding=20)