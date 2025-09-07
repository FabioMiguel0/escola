def seed_database():
    # This function will seed the database with initial data.
    # Example data for users
    users = [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "secretario", "password": "secretario123", "role": "secretaria"},
        {"username": "professor1", "password": "prof123", "role": "professor"},
        {"username": "aluno1", "password": "aluno123", "role": "aluno"},
    ]

    # Example data for subjects
    subjects = [
        {"name": "Matemática"},
        {"name": "Português"},
        {"name": "História"},
        {"name": "Ciências"},
    ]

    # Example data for classes
    classes = [
        {"name": "Turma A", "year": 2023},
        {"name": "Turma B", "year": 2023},
    ]

    # Example data for students
    students = [
        {"name": "João Silva", "class_id": 1},
        {"name": "Maria Oliveira", "class_id": 1},
    ]

    # Example data for teachers
    teachers = [
        {"name": "Prof. Carlos", "subject_id": 1},
        {"name": "Prof. Ana", "subject_id": 2},
    ]

    # Here you would typically insert this data into your database
    # For example:
    # db.insert_users(users)
    # db.insert_subjects(subjects)
    # db.insert_classes(classes)
    # db.insert_students(students)
    # db.insert_teachers(teachers)

if __name__ == "__main__":
    seed_database()