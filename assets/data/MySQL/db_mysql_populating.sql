-- Populating
INSERT INTO students (name, course, mobile) VALUES ('John Smith', 'Math', '11112233');
INSERT INTO students (name, course, mobile) VALUES ('Asha Patel', 'Astronomy', '22233344');
INSERT INTO students (name, course, mobile) VALUES ('Lokesh Rana', 'Biology', '33344455');
INSERT INTO students (name, course, mobile) VALUES ('Andy Johnson', 'Physics', '10011001');
INSERT INTO students (name, course, mobile) VALUES ('Kasia Popescu', 'Astronomy', '10011113');
INSERT INTO students (name, course, mobile) VALUES ('Paula Zephyr', 'Astronomy', '10111001');
INSERT INTO students (name, course, mobile) VALUES ('John Smith', 'Biology', '35784987');
INSERT INTO students (name, course, mobile) VALUES ('Sami Daher', 'Math', '57356879');
INSERT INTO students (name, course, mobile) VALUES ('Rami Naser', 'Biology', '54779870');
INSERT INTO students (name, course, mobile) VALUES ('Sara Hani', 'Biology', '54779476');
INSERT INTO students (name, course, mobile) VALUES ('Lora Mhanna', 'Math', '43534554');



-- RUN THIS SCRIPT IN CLI
--      1. Navigate to the Directory with this script:      cd <path/to/this/script/directory>
--      2. Login to MySQL Server:                           mysql -u <username> -p
--      3. Select Database:                                 USE school;
--      4. Run the Script:                                  source db_mysql_populating.sql
--      5. Exit MySQL CLI (Optional):                       exit;