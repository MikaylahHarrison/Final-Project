from flask import Flask, render_template

app = Flask(__name__)

# ------------------------------
# ROUTES FOR EACH SCREEN
# ------------------------------

@app.route("/")
def students_list():
    return render_template("index.html")       # Screen 2

@app.route("/student/<int:student_id>")
def student_detail(student_id):
    return render_template("student.html", student_id=student_id)   # Screen 5

@app.route("/new-student")
def new_student():
    return render_template("new-student.html")  # Screen 6

@app.route("/create-course")
def create_course():
    return render_template("create-course.html")  # Create Course - Rubrics screen

@app.route("/modify-buttons")
def modify_buttons():
    return render_template("modify-buttons.html")  # Screen 7

# ------------------------------
# DEVELOPMENT ENTRY POINT
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)


