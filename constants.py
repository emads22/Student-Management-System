from pathlib import Path


ASSETS_DIR = Path("./assets")
DB_FILE = ASSETS_DIR / "data" / "database.db"
TABLE_HEADERS = ("Id", "Names", "Course", "Mobile")
COURSES = ['Math', 'Astronomy', 'Biology', 'Physics']

# SQL Queries
GET_ALL_STUDENTS_QUERY = "SELECT * FROM students"
# id field is defined as AUTOINCREMENT when defining the table in database
INSERT_STUDENT_QUERY = "INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)"
SEARCH_STUDENT_QUERY = "SELECT * FROM students WHERE name = ?"
