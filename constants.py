from pathlib import Path


ASSETS_DIR = Path("./assets")
DB_FILE = ASSETS_DIR / "data" / "database.db"
ADD_ICON = ASSETS_DIR / "icons" / "add.png"
SEARCH_ICON = ASSETS_DIR / "icons" / "search.png"
CLEAR_ICON = ASSETS_DIR / "icons" / "clear.png"
TABLE_HEADERS = ("Id", "Names", "Course", "Mobile")
COURSES = ['Select Course','Math', 'Astronomy', 'Biology', 'Physics']

# SQL Queries
GET_ALL_STUDENTS_QUERY = "SELECT * FROM students"
# id field is defined as AUTOINCREMENT when defining the table in database
INSERT_STUDENT_QUERY = "INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)"
SEARCH_STUDENT_QUERY = "SELECT * FROM students WHERE name = ?"
UPDATE_STUDENT_QUERY = "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?"
DELETE_STUDENT_QUERY = "DELETE FROM students WHERE id = ?"

# for name pattern allow alphabetical characters with 1 space betwen like 'John Doe'
NAME_PATTERN = r'^[a-zA-Z]+ [a-zA-Z]+$'
# for phone number pattern it must be 8 digits
PHONE_NUMBER_PATTERN = r'^\d{8}$'