"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackbright.db'
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
    # #my print statements
    # print 'my print statements:\n\n'
    # print 'db_cursor type: ', type(db_cursor)
    # print row
    # print type(row)

    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])


def make_new_student(first_name2, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """ INSERT INTO Students VALUES (:first_name1, :last_name, :github)"""
    db_cursor = db.session.execute(QUERY, {'first_name1': first_name2, 'last_name': last_name, 'github': github})
    db.session.commit()
    print "Successfully added student: %s %s" % (first_name2, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """SELECT title, description FROM projects where title = :title
            """
    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()
    # print "Row: ", row
    print "Project: %s \nDescription: %s" % (row[0], row[1])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """SELECT grade From Grades WHERE student_github=:github AND project_title=:title"""
    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})
    row = db_cursor.fetchone()
    print "Grade: %s" % (row[0])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """INSERT INTO Grades VALUES (:github, :title, :grade)"""
    db.session.execute(QUERY, {'github': github, 'title': title, 'grade': grade})
    db.session.commit()
    print "Successfully added grade: %s %s %s" % (github, title, grade)

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
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github = args[0]
            title = args[1]
            get_grade_by_github_title(github, title)

        elif command =="assign_grade":
            github = args[0]
            title = args[1]
            grade = args[2]
            assign_grade(github, title, grade)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db.session.close()
