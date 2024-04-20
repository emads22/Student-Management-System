-- `students` Table
CREATE TABLE students(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    course TEXT, 
    mobile INTEGER
);

-- `sqlite_sequence` Table
CREATE TABLE sqlite_sequence(
    name,
    seq
);