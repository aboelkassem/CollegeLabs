from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    encoding = db.Column(db.LargeBinary, unique=False, nullable=False)
    attendances = db.relationship('Attendance', backref='student', lazy='subquery')

    def __repr__(self):
        return str({
            "id": self.id,
            "code": self.email,
            "encoding": self.encoding,
            "attendances": self.attendances
        })


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return str({
            "id": self.id,
            "date": self.date,
            "student_id": self.student_id
        })
