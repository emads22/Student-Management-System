from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QGridLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QDialog, QComboBox, QVBoxLayout)
from PyQt6.QtGui import QAction
import sys
import sqlite3
from constants import *


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

        # Add sub-items to menu items, called actions
        add_student_action = QAction("Add Student", self)
        # Connect the "triggered" signal of the "Add Student" action to the insert_student method of the MainWindow class
        add_student_action.triggered.connect(self.insert_student)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole)  # add this line only if help sub-menu didn't appear

        # Create a table widget for displaying student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("Id", "Names", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)  # Hide the indexes column

        # Load table data initially
        self.load_table_data()

        # Set the central widget of the main window to the table widget
        self.setCentralWidget(self.table)

    # Method to load data into the table
    def load_table_data(self):
        """
        Load data from the database and populate the table with it.

        This method connects to the SQLite database, executes a query to retrieve
        all student records, and populates the table widget with the fetched data.

        """
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

        # Close the database connection to release resources
        connection.close()

    def insert_student(self):
        dialog = InsertStudentDialog()
        dialog.exec()


class InsertStudentDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add a Student")

        # Layout
        layout = QVBoxLayout()

        # Create widgets
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter a name")
        
        course_combobox = QComboBox()
        course_combobox.addItems(COURSES)
        course_combobox.setCurrentIndex(0)

        phone_input = QLineEdit()
        phone_input.setPlaceholderText("Enter a phone number")

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.accept)

        # add widgets to layout
        layout.addWidget(name_input)
        layout.addWidget(course_combobox)
        layout.addWidget(phone_input)
        layout.addWidget(submit_button)

        self.setLayout(layout)


# Main function to create and run the application
def main():
    app = QApplication(sys.argv)
    # Set application style to Fusion
    app.setStyle("Fusion")
    # Create an instance of the main window
    app_window = MainWindow()
    # Show the main window
    app_window.show()
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
