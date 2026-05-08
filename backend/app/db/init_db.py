from app.auth.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.models import StudentRecord, User

SAMPLE_STUDENTS = [
    ("UAB1001", "Aarav Shah", "Data Structures", 5, 91, 94, 9.4, "CSE"),
    ("UAB1002", "Mia Johnson", "AI Foundations", 5, 88, 89, 9.1, "CSE"),
    ("UAB1003", "Noah Smith", "Signals", 4, 79, 83, 8.2, "ECE"),
    ("UAB1004", "Sophia Lee", "Circuits", 4, 95, 96, 9.7, "ECE"),
    ("UAB1005", "Liam Brown", "Thermodynamics", 3, 58, 61, 6.1, "ME"),
    ("UAB1006", "Olivia Davis", "Algorithms", 5, 42, 54, 5.2, "CSE"),
    ("UAB1007", "Ethan Wilson", "Databases", 6, 73, 78, 7.6, "IT"),
    ("UAB1008", "Isabella Garcia", "Networks", 6, 84, 88, 8.7, "IT"),
]

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@uab.edu").first():
            db.add(User(email="admin@uab.edu", full_name="UAB Admin", role="admin", hashed_password=hash_password("admin123")))
        if not db.query(User).filter(User.email == "student@uab.edu").first():
            db.add(User(email="student@uab.edu", full_name="Demo Student", role="student", hashed_password=hash_password("student123")))
        if db.query(StudentRecord).count() == 0:
            for row in SAMPLE_STUDENTS:
                db.add(StudentRecord(StudentID=row[0], Name=row[1], Course=row[2], Semester=row[3], Marks=row[4], Attendance=row[5], CGPA=row[6], Department=row[7]))
        db.commit()
    finally:
        db.close()
