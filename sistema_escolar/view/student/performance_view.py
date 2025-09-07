from flet import Page, Column, Text

def PerformanceView(page: Page, student_id: int):
    # This function builds the performance view for the student
    performance_data = get_performance_data(student_id)  # Assume this function fetches performance data

    content = Column()
    content.controls.append(Text("Desempenho do Aluno", size=24, weight="bold"))

    for subject, performance in performance_data.items():
        content.controls.append(Text(f"{subject}: {performance}", size=18))

    page.add(content)

def get_performance_data(student_id: int):
    # This function is a placeholder for fetching performance data from the database
    # Replace this with actual database logic
    return {
        "Matemática": "A",
        "Português": "B",
        "Ciências": "A",
        "História": "C",
        "Geografia": "B"
    }