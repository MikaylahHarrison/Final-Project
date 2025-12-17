from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ------------------------------
# In-memory storage
# ------------------------------
students = []
courses = []
quick_buttons = [
    {"label": "Late", "points": -5, "description": "Arrived late to class"},
    {"label": "Off Task", "points": -5, "description": "Not focusing"}
]

# ------------------------------
# ROUTES
# ------------------------------

@app.route("/")
def students_list():
    # Compute employability grade for each student
    for student in students:
        student['employability'] = 100 + sum([i['points'] for i in student.get('infractions', [])])
    return render_template("index.html", students=students)

@app.route("/new-student", methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        period = request.form.get('class_period')
        if first_name and last_name and period:
            students.append({
                'first_name': first_name,
                'last_name': last_name,
                'period': period,
                'infractions': []
            })
            return redirect(url_for('students_list'))
    return render_template("new-student.html")

@app.route("/student/<int:student_id>", methods=['GET', 'POST'])
def student_detail(student_id):
    if 1 <= student_id <= len(students):
        student = students[student_id - 1]

        if request.method == 'POST':
            quick_label = request.form.get("quick_label")
            if quick_label:
                # Quick button pressed
                for button in quick_buttons:
                    if button["label"] == quick_label:
                        student['infractions'].append({
                            "description": button["description"],
                            "points": button["points"],
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        break
            else:
                # Custom infraction
                description = request.form.get("description")
                points = request.form.get("points")
                if description and points:
                    student['infractions'].append({
                        "description": description,
                        "points": int(points),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            return redirect(url_for('student_detail', student_id=student_id))

        return render_template("student.html", student=student, student_id=student_id, quick_buttons=quick_buttons)
    else:
        return "Student not found", 404

@app.route("/student/<int:student_id>/remove", methods=['POST'])
def remove_student(student_id):
    if 1 <= student_id <= len(students):
        del students[student_id - 1]
    return redirect(url_for('students_list'))

@app.route("/student/<int:student_id>/remove-infraction/<int:infraction_index>", methods=['POST'])
def remove_infraction(student_id, infraction_index):
    if 1 <= student_id <= len(students):
        student = students[student_id - 1]
        if 0 <= infraction_index < len(student['infractions']):
            del student['infractions'][infraction_index]
    return redirect(url_for('student_detail', student_id=student_id))

@app.route("/create-course", methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        teacher_name = request.form.get('teacher_name')
        if course_name and teacher_name:
            courses.append({
                "course_name": course_name,
                "teacher_name": teacher_name
            })
        return redirect(url_for('create_course'))
    return render_template("create-course.html")

@app.route("/modify-buttons", methods=['GET', 'POST'])
def modify_buttons():
    global quick_buttons
    if request.method == 'POST':
        remove_label = request.form.get("remove_label")
        if remove_label:
            quick_buttons = [b for b in quick_buttons if b["label"] != remove_label]
        else:
            label = request.form.get("label")
            points = request.form.get("points")
            description = request.form.get("description")
            if label and points and description:
                quick_buttons.append({
                    "label": label,
                    "points": int(points),
                    "description": description
                })
        return redirect(url_for('modify_buttons'))
    return render_template("modify-buttons.html", quick_buttons=quick_buttons)

# ------------------------------
# RUN APP
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
