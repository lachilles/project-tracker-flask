"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github})
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])
    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (:first_name, :last_name, :github)"""
    db_cursor = db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name, 'github': github})
    db.session.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT title, description, max_grade
        FROM Projects
        WHERE title = :title
        """
    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()
    print "Title: %s\nDescription: %s\nMax Grade: %d" % (row[0], row[1], row[2])
    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
        SELECT grade
        FROM Grades
        WHERE student_github = :github
          AND project_title = :title
        """
    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})
    row = db_cursor.fetchone()
    print "Student %s in project %s received grade of %s" % (
        github, title, row[0])
    return row


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """INSERT INTO Grades (student_github, project_title, grade)
               VALUES (:github, :title, :grade)"""
    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title, 'grade': grade})
    db.session.commit()
    print "Successfully assigned grade of %s for %s in %s" % (
        grade, github, title)

def get_grades_by_github(github):
    """Get a list of all grades for a student by their github username"""
    QUERY = """
        SELECT project_title, grade
        FROM Grades
        WHERE student_github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github})
    rows = db_cursor.fetchall()
    for row in rows:
        print "Student %s received grade of %s for project %s" % (
            github, row[1], row[0])
    return rows

def get_grades_by_title(title):
    """Get a list of all student grades for a project by its title"""

    QUERY = """
        SELECT student_github, grade
        FROM Grades
        WHERE project_title = :title
        """
    db_cursor = db.session.execute(QUERY, {'title': title})
    rows = db_cursor.fetchall()
    for row in rows:
        print "Student %s received grade of %s for project %s" % (
            row[0], row[1], title)
    return rows


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "student_grades":
            github = args[0]
            get_grades_by_github(github)

        elif command == "project_grades":
            title = args[0]
            get_grades_by_title(title)



if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db.session.close()
