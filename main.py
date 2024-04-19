from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QDialog, QComboBox, QVBoxLayout)
from PyQt6.QtGui import QAction
import sys
import sqlite3
import logging
from app_logging import handle_logging
from constants import *


# Set up logging using the custom handler
handle_logging()


# Define the main window class
class MainWindow(QMainWindow):
    """
    Main application window.

    This class represents the main window of the application. It inherits from
    QMainWindow and provides methods for managing the application's user interface.

    """

    def __init__(self):
        """
        Initialize the main window.

        This method initializes the main window and sets up the user interface.

        """
        super().__init__()

        # Set the size of the main window
        self.resize(400, 300)  # Set width and height of the window

        # Set window title
        self.setWindowTitle("Student Management System")

        # Create menu items for File and Help
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add sub-items to menu items, called actions
        add_student_action = QAction("Add Student", self)
        # Connect the "triggered" signal of the "Add Student" action to the insert_student method of the MainWindow class
        add_student_action.triggered.connect(self.insert_student)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole)  # add this line only if help sub-menu didn't appear

        search_student_action = QAction("Search", self)
        search_student_action.triggered.connect(self.search_student)
        edit_menu_item.addAction(search_student_action)

        # Create a table widget for displaying student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.table.verticalHeader().setVisible(False)  # Hide the indexes column

        # Load table data initially
        self.load_table_data()

        # Set the central widget of the main window to the table widget
        self.setCentralWidget(self.table)

    def load_table_data(self):
        """
        Load data from the database and populate the table with it.

        This method connects to the SQLite database, executes a query to retrieve
        all student records, and populates the table widget with the fetched data.

        """
        connection = None
        try:
            # Establish a connection to the SQLite database
            connection = sqlite3.connect(DB_FILE)

            # Create a cursor object and Execute the SQL query to retrieve all student records
            cursor = connection.cursor()
            cursor.execute(GET_ALL_STUDENTS_QUERY)

            # Fetch all the rows returned by the query
            all_students_rows = cursor.fetchall()

            # Reset the table to remove existing data
            self.table.setRowCount(0)

            # Iterate over each row fetched from the database
            for row_index, row in enumerate(all_students_rows):
                # Insert a new row into the table
                self.table.insertRow(row_index)

                # Iterate over each column data in the current row
                for col_index, col_data in enumerate(row):
                    # Create a QTableWidgetItem and set its value to the current column value
                    table_item = QTableWidgetItem(str(col_data))
                    # Set the QTableWidgetItem in the corresponding cell of the table
                    self.table.setItem(row_index, col_index, table_item)
            # log success message
            logging.info("Table data loaded successfully.")

        except sqlite3.Error as e:
            # log the error
            logging.error("Error loading table data:", e)

        finally:
            # Close the cursor the database connection to release resources
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def insert_student(self):
        """
        Opens a dialog for inserting a new student.
        """
        # Create an instance of InsertStudentDialog
        dialog = InsertStudentDialog()
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()
        # Reload the table data after the insert dialog is finished
        self.load_table_data()

    def search_student(self):
        """
        Opens a dialog for searching a student.
        """
        # Create an instance of InsertStudentDialog
        dialog = SearchStudentDialog()
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()


class InsertStudentDialog(QDialog):
    """
    Dialog for adding a new student.
    """

    def __init__(self):
        """
        Initializes the dialog window.
        """
        super().__init__()

        self.setWindowTitle("Insert Student Data")

        # Layout
        layout = QVBoxLayout()

        # Create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        self.course_name = QComboBox()
        self.course_name.addItems(COURSES)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone number")

        button = QPushButton("Register")
        button.clicked.connect(self.add_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.phone_number)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        """
        Adds a new student record to the SQLite database.
        """
        connection = None
        # Establish a connection to the SQLite database and Create a cursor object to execute queries
        try:
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()

            # Prepare data to insert
            name = self.student_name.text().title()
            course = self.course_name.currentText()
            phone = self.phone_number.text()

            # Execute the SQL query to insert a new student record
            cursor.execute(INSERT_STUDENT_QUERY, (name, course, phone))
            # Commit changes to the database
            connection.commit()

            # log success message
            logging.info("Student added successfully.")
            # Reset the inputs
            self.clear_inputs()

        except sqlite3.Error as e:
            # Rollback changes if an error occurs
            if connection:
                connection.rollback()
            # log the error
            logging.error("Error adding student:", e)

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            # # Close the dialog when pressing 'Register'
            # self.accept()

    def clear_inputs(self):
        """
        Clear all input fields in the dialog.
        """
        # Clear input fields
        self.student_name.clear()
        self.course_name.setCurrentIndex(0)  # Assuming the default index is 0
        self.phone_number.clear()


class SearchStudentDialog(QDialog):
    """
    Dialog for searching a student.
    """

    def __init__(self):
        """
        Initializes the dialog window.
        """
        super().__init__()

        self.setWindowTitle("Search Student")

        # Layout
        layout = QVBoxLayout()

        # Create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        button = QPushButton("Search")
        button.clicked.connect(self.search_this_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_this_student(self):
        """
        Search for a student in the SQLite database.
        """

        # Clear/Reset student name input field
        self.student_name.clear()


# Main function to create and run the application
def main():
    app = QApplication(sys.argv)
    # Set application style to Fusion
    app.setStyle("Fusion")
    # Create an instance of the main window
    main_window = MainWindow()
    # Show the main window
    main_window.show()
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
