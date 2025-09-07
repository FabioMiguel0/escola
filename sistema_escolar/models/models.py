from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

    students = relationship("Student", back_populates="user")
    teachers = relationship("Teacher", back_populates="user")

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    grade = Column(String)

    user = relationship("User", back_populates="students")
    grades = relationship("Grade", back_populates="student")
    subjects = relationship("Subject", secondary="student_subjects")

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    user = relationship("User", back_populates="teachers")
    subjects = relationship("Subject", back_populates="teachers")

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    students = relationship("Student", secondary="student_subjects")
    teachers = relationship("Teacher", back_populates="subjects")

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    score = Column(Integer)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject") 

class StudentSubjects(Base):
    __tablename__ = 'student_subjects'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)