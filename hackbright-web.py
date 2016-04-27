from flask import Flask, request, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

import hackbright

db = SQLAlchemy()

def connect_to_db(app):
    """Connect to database"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hackbright'
    db.app = app
    db.init_app(app)

app = Flask(__name__)

app.secret_key = "THIS IS OUR SECRET KEY"

connect_to_db(app)

@app.route("/student_search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github','jhacks')
    grade = request.args.get('grade', '100')
    project = request.args.get('project', 'Markov')
    first, last, github = hackbright.get_student_by_github(github)
    (project, grade) = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grade=grade,
                           project=project)

    #print "%s is the GitHub account for %s %s" % (github, first, last)
    return html

@app.route("/student_add_form")
def student_add():
    """Add a student."""

    return render_template("student_add.html")

@app.route("/student_add", methods=['POST'])
def student_response():
    """Response to adding student"""

    first = request.form.get('first','jhacks')
    last = request.form.get('last','jhacks')
    github = request.form.get('github','jhacks')
    hackbright.make_new_student(first, last, github)

    return render_template("student_response.html",
                           first=first,
                           last=last,
                           github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
