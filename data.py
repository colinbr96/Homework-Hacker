################################################################################
# Classes

class Course:
    def __init__(self, title, professor, code):
        self._title = title
        self._professor = professor
        self._code = code


class Assignment:
    def __init__(self, title, course, due_date):
        self._title = title
        self._course = course
        self._due_date = due_date
