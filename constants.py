from pathlib import Path


ASSETS_DIR = Path("./assets")
DB_FILE = ASSETS_DIR / "data" / "database.db"
GET_ALL_STUDENTS_QUERY = "SELECT * FROM students"
COURSES = ['Select a course', 'Math', 'Astronomy', 'Biology', 'Physics']