import json

from flask import Flask, Response, flash, make_response
from flask.templating import render_template
import cv2
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle
from datetime import datetime, timedelta
from sqlalchemy import desc

from config import Config
from core.face_recognizer import FaceRecognizer
from core.face_encoder import FaceEncoder
from core.face_detector import FaceDetector


load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

import api.models as entities

face_detector = FaceDetector()
face_encoder = FaceEncoder()
face_recognizer = FaceRecognizer()

camera = cv2.VideoCapture(0)

print("All class sucessfully loaded!")

current_recognized_students = []

def check_current_images():
    print("Loading all images from data folder")
    people_dir = 'data/images'
    images = os.listdir(people_dir)
    if len(images) == 0:
        print("No images found")
        return
    for img in images:
        img_file = cv2.imread(f'{people_dir}/{img}')
        student_code = int(os.path.splitext(img)[0])
        student = entities.Student().query.filter_by(code=student_code).first()

        if student:
            flash('Student code has already existed', 'warning')
        else:
            face_detector = FaceDetector()
            face_image = face_detector.extract_face(image_array=img_file)[0]
            face_embedding = face_encoder.get_embedding(image_array=face_image)
            face_byte_array = pickle.dumps(face_embedding)
            db.session.add(entities.Student(
                code=student_code,
                encoding=face_byte_array
            ))
            db.session.commit()


def get_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            try:
                extracted_faces = face_detector.extract_face(image_array=frame)
                for extracted_face in extracted_faces:
                    face_embedding = face_encoder.get_embedding(image_array=extracted_face)
                    checked_in_student = get_check_in_student(face_embedding)
                    if checked_in_student is None:
                        print("No student found, please add the student to database")
                    else:
                        if checked_in_student.code not in current_recognized_students:
                            current_recognized_students.append(checked_in_student.code)
            except:
                print("[Error] Face not found. Please try again!")
            ret, buffer = cv2.imencode('.jpg', img=frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def get_check_in_student(face_embedding):
    with app.app_context():
        students = entities.Student().query.all()

    similarities = [face_recognizer.compare(
        face_embedding, pickle.loads(student.encoding)) for student in students]

    print([(students[idx].code, similarity) for idx, similarity in enumerate(similarities)])

    max_similarity = max(similarities)

    print("Maximum similarities: {}".format(max_similarity))

    max_similarity_index = similarities.index(max_similarity)

    if max_similarity > 0.97:
        checked_in_student = students[max_similarity_index]
        print("student: {}".format(checked_in_student.code))
        # Check for saved attended recorded
        with app.app_context():
            student = entities.Student().query.filter_by(code=checked_in_student.code).first()
            if student:
                latest_attended = entities.Attendance().query.filter_by(student_id=student.id).order_by(desc(entities.Attendance.date)).first()
                current_date = datetime.now()
                if latest_attended is None:
                    db.session.add(entities.Attendance(
                        date=current_date,
                        student_id=student.id
                    ))
                    db.session.commit()
                else:
                    next_attendance = latest_attended.date + timedelta(hours=2)
                    if next_attendance < current_date:
                        db.session.add(entities.Attendance(
                            date=current_date,
                            student_id=student.id
                        ))
                        db.session.commit()
        return checked_in_student
    return None


@app.route('/')
def index():
    check_current_images()
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/attendances')
def attendances():
    with app.app_context():
        students = entities.Student().query.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return render_template('attendances.html', students=students, days=days)


@app.route('/active_students')
def active_students():
    response = make_response(json.dumps(current_recognized_students))
    response.content_type = 'application/json'
    return response

if __name__ == "__main__":
    app.run(debug=True)
