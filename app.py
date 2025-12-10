from flask import Flask, render_template, request, redirect
from models import db, Student, Infraction

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# HOME PAGE — LIST ALL STUDENTS
@app.route("/")
def home():
    students = Student.query.all()
    return render_template("home.html", students=students)


# ADD NEW STUDENT
@app.route("/students/new", methods=["GET", "POST"])
def new_student():
    if request.method == "POST":
        s = Student(first_name=request.form["first_name"],
                    last_name=request.form["last_name"])
        db.session.add(s)
        db.session.commit()
        return redirect("/")
    return render_template("new_student.html")


# STUDENT DETAILS PAGE
@app.route("/students/<int:id>")
def student_detail(id):
    student = Student.query.get_or_404(id)
    return render_template("student_detail.html", student=student)


# ADD INFRACTION
@app.route("/infraction/add/<int:id>", methods=["POST"])
def add_infraction(id):
    student = Student.query.get_or_404(id)
    desc = request.form["description"]
    points = int(request.form["points"])

    inf = Infraction(student=student, description=desc, points=points)
    db.session.add(inf)
    db.session.commit()

    return redirect(f"/students/{id}")


# QUICK ACTION BUTTONS
@app.route("/infraction/quick/<int:id>/<string:type>")
def quick_infraction(id, type):
    student = Student.query.get_or_404(id)

    mapping = {
        "late": ("Late", -5),
        "offtask": ("Off Task", -5)
    }

    desc, points = mapping[type]

    inf = Infraction(student=student, description=desc, points=points)
    db.session.add(inf)
    db.session.commit()

    return redirect("/")


# DELETE AN INFRACTION
@app.route("/infraction/delete/<int:id>")
def delete_infraction(id):
    inf = Infraction.query.get_or_404(id)
    student_id = inf.student_id
    db.session.delete(inf)
    db.session.commit()
    return redirect(f"/students/{student_id}")


# CONFIRM DELETE STUDENT
@app.route("/students/delete/<int:id>")
def delete_student_confirm(id):
    student = Student.query.get_or_404(id)
    return render_template("confirm_delete.html", student=student)


# DELETE STUDENT
@app.route("/students/delete/yes/<int:id>")
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


