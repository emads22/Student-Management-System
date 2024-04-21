-- Create `school` Database
CREATE DATABASE school;


-- Select Database 
USE school;


-- Create `students` Table
CREATE TABLE students(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(255), 
    course VARCHAR(255), 
    mobile VARCHAR(255)
);



-- RUN THIS SCRIPT IN CLI
--      1. Navigate to the Directory with this script:      cd <path/to/this/script/directory>
--      2. Login to MySQL Server:                           mysql -u <username> -p
--      3. Select Database:                                 USE school;
--      4. Run the Script:                                  source db_mysql_schema.sql
--      5. Exit MySQL CLI (Optional):                       exit;





