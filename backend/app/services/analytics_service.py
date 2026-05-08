from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import StudentRecord

PASS_MARK = 50
RISK_CGPA = 6.0
RISK_ATTENDANCE = 65


def get_student(db: Session, student_id: str):
    return db.query(StudentRecord).filter(StudentRecord.StudentID == student_id).first()


def department_topper(db: Session, department: str):
    return (
        db.query(StudentRecord)
        .filter(func.lower(StudentRecord.Department) == department.lower())
        .order_by(StudentRecord.CGPA.desc())
        .first()
    )


def pass_rate(db: Session):
    departments = db.query(StudentRecord.Department).distinct().all()
    result = []

    for (department,) in departments:
        total = db.query(StudentRecord).filter(StudentRecord.Department == department).count()
        passed = (
            db.query(StudentRecord)
            .filter(StudentRecord.Department == department, StudentRecord.Marks >= PASS_MARK)
            .count()
        )
        result.append(
            {
                "department": department,
                "pass_rate": round((passed / total) * 100, 2) if total else 0,
            }
        )

    return result


def at_risk(db: Session):
    return db.query(StudentRecord).filter(
        (StudentRecord.CGPA < RISK_CGPA) | (StudentRecord.Attendance < RISK_ATTENDANCE)
    ).all()


def average_cgpa(db: Session):
    rows = db.query(StudentRecord.Department, func.avg(StudentRecord.CGPA)).group_by(StudentRecord.Department).all()
    return [{"department": department, "average_cgpa": round(average, 2)} for department, average in rows]


def cgpa_distribution(db: Session):
    bands = {"<6": 0, "6-7": 0, "7-8": 0, "8-9": 0, "9+": 0}

    for student in db.query(StudentRecord).all():
        if student.CGPA < 6:
            bands["<6"] += 1
        elif student.CGPA < 7:
            bands["6-7"] += 1
        elif student.CGPA < 8:
            bands["7-8"] += 1
        elif student.CGPA < 9:
            bands["8-9"] += 1
        else:
            bands["9+"] += 1

    return [{"band": band, "count": count} for band, count in bands.items()]


def semester_ranking(db: Session, semester: int):
    return (
        db.query(StudentRecord)
        .filter(StudentRecord.Semester == semester)
        .order_by(StudentRecord.CGPA.desc())
        .all()
    )


def answer_sql_question(db: Session, message: str) -> str:
    lower = message.lower()

    if "topper" in lower:
        department = next((dept for dept in ["CSE", "ECE", "ME", "IT"] if dept.lower() in lower), "CSE")
        student = department_topper(db, department)
        if not student:
            return f"No records found for {department}."
        return f"{student.Name} is the {department} topper with CGPA {student.CGPA}."

    if "average" in lower or "avg" in lower:
        rows = average_cgpa(db)
        return "Department average CGPA: " + ", ".join(
            f"{row['department']}: {row['average_cgpa']}" for row in rows
        )

    if "risk" in lower or "at-risk" in lower:
        rows = at_risk(db)
        return "At-risk students: " + ", ".join(
            f"{student.Name} ({student.Department}, CGPA {student.CGPA}, Attendance {student.Attendance}%)"
            for student in rows
        )

    if "pass" in lower:
        return "Pass rates: " + ", ".join(
            f"{row['department']}: {row['pass_rate']}%" for row in pass_rate(db)
        )

    return "I can answer topper, CGPA average, pass-rate, ranking, student detail, and at-risk analytics questions."
