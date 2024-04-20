from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QDialog,
                             QComboBox, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QAction
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

        clear_selection_action = QAction("Clear All", self)
        clear_selection_action.triggered.connect(self.clear_selection)
        edit_menu_item.addAction(clear_selection_action)

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
        try:
            # Establish a connection to the SQLite database and create a cursor object
            with sqlite3.connect(DB_FILE) as connection:
                cursor = connection.cursor()

                # Execute the SQL query to retrieve all student records
                cursor.execute(GET_ALL_STUDENTS_QUERY)

                # Fetch all the rows returned by the query
                all_students_rows = cursor.fetchall()

                # Reset the table to remove existing data
                self.table.setRowCount(0)

                # Iterate over each row fetched from the database
                for row_i, row in enumerate(all_students_rows):
                    # Insert a new row into the table
                    self.table.insertRow(row_i)

                    # Iterate over each column data in the current row
                    for col_i, col_data in enumerate(row):
                        # Create a QTableWidgetItem and set its value to the current column value
                        table_item = QTableWidgetItem(str(col_data))
                        # Set the QTableWidgetItem in the corresponding cell of the table
                        self.table.setItem(row_i, col_i, table_item)
            # log success message
            logging.info("Table data loaded successfully.")

        except sqlite3.Error as e:
            # log the error
            logging.error("Error loading table data:", e)

    def insert_student(self):
        """
        Opens a dialog for inserting a new student.
        """
        # Create an instance of InsertStudentDialog and pass the parent
        dialog = InsertStudentDialog(parent=self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def search_student(self):
        """
        Opens a dialog for searching a student.
        """
        # Create an instance of InsertStudentDialog and pass the parent
        dialog = SearchStudentDialog(parent=self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def clear_selection(self):
        """
        Clear the selection in the table widget.

        This method clears any selected items in the table widget, effectively deselecting all currently selected rows and columns.
        """
        self.table.clearSelection()


class InsertStudentDialog(QDialog):
    """
    Dialog for adding a new student.
    """

    def __init__(self, parent):
        """
        Initializes the dialog window.
        """
        super().__init__()

        # Get hold of the parent window calling this dialog in order to access it
        self.parent_window = parent

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
        # Establish a connection to the SQLite database and create a cursor object within a with statement
        try:
            with sqlite3.connect(DB_FILE) as connection:
                cursor = connection.cursor()

                # Prepare data to insert
                name = self.student_name.text().title()
                course = self.course_name.currentText()
                phone = self.phone_number.text()

                # Execute the SQL query to insert a new student record
                cursor.execute(INSERT_STUDENT_QUERY, (name, course, phone))
                # Commit changes to the database
                connection.commit()

                # Reset the inputs
                self.clear_inputs()
                # Reload the table data after the insert dialog is finished
                self.parent_window.load_table_data()
                # Log success message
                logging.info("Student added successfully.")

        except sqlite3.Error as e:
            # Rollback changes if an error occurs
            logging.error("Error adding student:", e)

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

    def __init__(self, parent):
        """
        Initializes the dialog window.
        """
        super().__init__()

        # Get hold of the parent window calling this dialog in order to access it
        self.parent_window = parent

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
        Searches for a student in the SQLite database.
        If found, highlights the records in the table and logs the success message.
        If not found, displays a warning message and clears the input field for new entry.
        """
        # Get the student name input
        this_name = self.student_name.text().title()

        # Check if the student exists in the database
        if not self.exists_in_db(this_name):
            # Display a warning message if the student is not found
            QMessageBox.warning(self, "Student Not Found",
                                f"No records found for student: {this_name}")
            # Clear the input field for new entry
            self.student_name.clear()

        else:
            # Find all items in the table that match the student's name exactly (case-sensitive)
            records_found = self.parent_window.table.findItems(
                this_name, Qt.MatchFlag.MatchFixedString)

            # Iterate over each matching record found in the table
            for record in records_found:
                # Get the row index of the current record
                row_index = record.row()

                # Iterate over each column in the table
                for col_index in range(self.parent_window.table.columnCount()):
                    # Set the current cell as selected, indicating it's part of the found record
                    self.parent_window.table.item(
                        row_index, col_index).setSelected(True)

            # Log a success message
            logging.info("Student found and highlighted successfully.")

            # Close the dialog if the student is found
            self.accept()

    def exists_in_db(self, student_name):
        """
        Checks if a student exists in the SQLite database.
        """
        connection = None
        this_student_rows = []

        try:
            # Establish connection and create a cursor
            with sqlite3.connect(DB_FILE) as connection:
                cursor = connection.cursor()

                # Execute the query to search for the student
                cursor.execute(SEARCH_STUDENT_QUERY, (student_name, ))

                # Fetch all matching rows
                this_student_rows = cursor.fetchall()

        except sqlite3.Error as e:
            # Log the error with details
            logging.error(f"Error while searching in database for {
                          student_name}: {e}")

        finally:
            # Close the cursor and connection
            if 'cursor' in locals() and cursor:  # or simply `if cursor:`
                cursor.close()

        # Return True if student exists, False otherwise (in case of error list will be empty still so bool() returns False)
        return bool(this_student_rows)
