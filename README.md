# Student Management System

## Overview
Student Management System is a comprehensive Python application designed to streamline the management of student records within educational institutions. Built using PyQt6 for the graphical user interface and MySQL for data storage, this system offers a user-friendly interface for administrators to efficiently handle student data.

The primary goal of this system is to simplify the process of managing student information, including their names, courses, and contact details. It provides a centralized platform where administrators can seamlessly perform tasks such as adding new students, searching for specific records, editing existing entries, and deleting outdated information.

The application's database schema is included, offering users the flexibility to customize and expand the database structure according to their specific requirements. Users are free to add new columns or data as preferred, ensuring adaptability to evolving needs and preferences.

**Database Creation and Population:** Database creation queries and population scripts for both MySQL and SQLite databases are available in the `asset/data/` folder under the `MySQL` directory for MySQL database and the `SQLite` directory for SQLite database.

By leveraging Object-Oriented Programming (OOP) principles, the application is structured into modular components, enhancing maintainability and scalability. Each component, from the main window to the various dialog boxes, encapsulates specific functionalities, promoting code reusability and clarity.

The graphical interface features intuitive controls, including a toolbar for quick access to common actions and a status bar that dynamically adjusts based on user interactions. Notably, the status bar displays contextual buttons for editing and deleting student records only when a row is selected, ensuring a streamlined user experience.

With robust error handling mechanisms in place, the system maintains reliability and transparency in database operations. Administrators can rely on detailed log messages to track successful operations and diagnose any errors or exceptions that may occur during runtime. The error handling architecture is designed to be expandable, allowing for easy integration of additional error handling functionalities as needed.

**Note:** This version of the application now uses MySQL as the default database. If you prefer to use SQLite, you can use the `legacy_ui.py` file instead of `ui.py`. Additionally, don't forget to add the MySQL connection data (host, port, user, password, and database) in the `constants.py` file before running the application.

## Features
- **Add Student**: Allows users to add new student records to the database.
- **Search**: Enables users to search for specific student records based on their name.
- **Edit Record**: Allows users to modify existing student records.
- **Delete Record**: Enables users to remove student records from the database.

## Technologies Used
- **mysql-connector-python**: A library for connecting to MySQL databases.
- **PyQt6**: A set of Python bindings for the Qt application framework.
- **python-dotenv**: A library for managing environment variables in .env files.
- **logging**: A module for tracking events that happen when software runs.
- **sqlite3**: A module for working with SQLite databases.
- **re**: A module for regular expression operations.

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Configure the necessary parameters such as MySQL connection data (host, port, user, password, and database) in `constants.py`.
5. Run the script using `python main.py`.

## Usage
1. Run the script using `python main.py`.
2. Use the "Add Student" button in the toolbar to insert new student records.
3. Use the "Search" button in the Edit menu to find specific student records.
4. Select a row in the table to enable the "Edit Record" and "Delete Record" buttons in the status bar.
5. Click the "Edit Record" button in the status bar to modify the selected student record.
6. Click the "Delete Record" button in the status bar to remove the selected student record from the database.

## Logger
The application utilizes a logging module to handle logging events. It logs success messages, errors, and critical events related to database operations and user interactions.

## Object-Oriented Programming (OOP) Models
The application follows an Object-Oriented Programming (OOP) approach with the following main models:
- **MainWindow**: Represents the main window of the application and manages the user interface.
- **InsertDialog**: Dialog for adding a new student record.
- **SearchDialog**: Dialog for searching a student record.
- **EditDialog**: Dialog for editing an existing student record.
- **DeleteDialog**: Dialog for deleting a student record.
- **AboutDialog**: Dialog to display information about the application.

## Toolbar and Statusbar
The application features a toolbar containing buttons for common actions such as adding a new student, searching, and clearing selections. When a row is selected in the table, the status bar displays two buttons, "Edit Record" and "Delete Record", allowing users to edit or delete the selected student record.

## Contributing
Contributions are welcome! Here are some ways you can contribute to the project:
- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or enhancements

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.

