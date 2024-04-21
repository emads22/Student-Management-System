from pathlib import Path
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


ASSETS_DIR = Path("./assets")
ADD_ICON = ASSETS_DIR / "icons" / "add.png"
SEARCH_ICON = ASSETS_DIR / "icons" / "search.png"
CLEAR_ICON = ASSETS_DIR / "icons" / "clear.png"

# SQLITE data
DB_FILE = ASSETS_DIR / "data" / "SQLite" / "database.db"

# MYSQL data
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
DATABASE = "school"

# GUI table data
TABLE_HEADERS = ("Id", "Names", "Course", "Mobile")
COURSES = ['Select Course', 'Math', 'Astronomy', 'Biology', 'Physics']

# SQLITE Queries
GET_ALL_STUDENTS_SQLITE_QUERY = "SELECT * FROM students"
# id field is defined as AUTOINCREMENT when defining the table in database
INSERT_STUDENT_SQLITE_QUERY = "INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)"
SEARCH_STUDENT_SQLITE_QUERY = "SELECT * FROM students WHERE name = ?"
UPDATE_STUDENT_SQLITE_QUERY = "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?"
DELETE_STUDENT_SQLITE_QUERY = "DELETE FROM students WHERE id = ?"

# MYSQL Queries
GET_ALL_STUDENTS_MYSQL_QUERY = "SELECT * FROM students"
# id field is defined as AUTOINCREMENT when defining the table in database
INSERT_STUDENT_MYSQL_QUERY = "INSERT INTO students (name, course, mobile) VALUES(%s, %s, %s)"
SEARCH_STUDENT_MYSQL_QUERY = "SELECT * FROM students WHERE name = %s"
UPDATE_STUDENT_MYSQL_QUERY = "UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s"
DELETE_STUDENT_MYSQL_QUERY = "DELETE FROM students WHERE id = %s"

# for name pattern allow alphabetical characters with 1 space betwen like 'John Doe'
NAME_PATTERN = r'^[a-zA-Z]+ [a-zA-Z]+$'
# for phone number pattern it must be 8 digits
PHONE_NUMBER_PATTERN = r'^\d{8}$'
