from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QDialog,
                             QComboBox, QVBoxLayout, QMessageBox,
                             QToolBar, QAbstractItemView, QStatusBar,
                             QLabel, QGridLayout)
from PyQt6.QtGui import QAction, QIcon
import sqlite3
import logging
from app_logging import handle_logging
import re
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

        # Set the minimum size of the main window
        self.setMinimumSize(417, 500)  # Set width and height of the window

        # Set window title
        self.setWindowTitle("Student Management System")

        # Create menu items for File and Help
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add sub-items to menu items, called actions (also add an icon for each to be used in the toolbar)
        add_student_action = QAction(QIcon(str(ADD_ICON)), "Add Student", self)
        # Connect the "triggered" signal of the "Add Student" action to the insert method of the MainWindow class
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole)  # add this line only if help sub-menu didn't appear

        search_student_action = QAction(
            QIcon(str(SEARCH_ICON)), "Search", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

        clear_selection_action = QAction(
            QIcon(str(CLEAR_ICON)), "Clear All", self)
        clear_selection_action.triggered.connect(self.clear_selection)
        edit_menu_item.addAction(clear_selection_action)

        # Create a table widget for displaying student data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.table.verticalHeader().setVisible(False)  # Hide the indexes column
        # Set the table to read-only and not editable
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        # Detect a cell clicked in the table
        self.table.cellClicked.connect(self.cell_clicked)

        # Load table data initially
        self.load_table_data()

        # Set the central widget of the main window to the table widget
        self.setCentralWidget(self.table)

        # Create a toolbar and add its elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)
        toolbar.addAction(clear_selection_action)

        # Add the toolbar to the main window
        self.addToolBar(toolbar)

        # Create a statusbar and add it to the main window
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

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
            success_msg = "Table data loaded successfully."
            logging.info(success_msg)

        except sqlite3.Error as e:
            # log the error
            error_msg = f"Error loading table data"
            QMessageBox.critical(self, "Error", error_msg)
            logging.error(f"{error_msg}: {e}")

    def cell_clicked(self):
        """
        Handle the event when a cell is clicked in the table.
        """
        # Create 'Edit Record' button and Connect its 'clicked' signal to 'edit' method
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        # Create 'Delete Record' button and Connect its 'clicked' signal to 'delete' method
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Reconfigure the status bar and clean it ti avoid duplicate buttons at each select
        self.clear_statusbar()

        # Add 'Edit Record' and 'Delete Record' buttons to the status bar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def insert(self):
        """
        Opens a dialog for inserting a new student.
        """
        # Create an instance of InsertDialog and pass the parent
        dialog = InsertDialog(parent=self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def search(self):
        """
        Opens a dialog for searching a student.
        """
        # Create an instance of SearchDialog and pass the parent
        dialog = SearchDialog(parent=self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def edit(self):
        """
        Opens a dialog for editing a student record.
        """
        # Create an instance of EditDialog and pass the parent
        dialog = EditDialog(parent=self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def delete(self):
        """
        Opens a dialog for deleting a student record.
        """
        # Create an instance of DeleteDialog and pass the parent
        dialog = DeleteDialog(parent=self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def about(self):
        """
        Opens a dialog for about the app info.
        """
        # Create an instance of AboutDialog
        dialog = AboutDialog(self)
        # Execute the dialog (blocks until the dialog is closed)
        dialog.exec()

    def clear_selection(self):
        """
        Clear the selection in the table widget and status bar.

        This method clears any selected items in the table widget, effectively deselecting all currently selected rows and columns, and clearing the status bar.
        """
        self.table.clearSelection()
        self.clear_statusbar()

    def clear_statusbar(self):
        """
        Clear the status bar by removing any QPushButton widgets from it.

        This method finds all child widgets of type QPushButton within the current widget
        (main window) and removes them from the status bar.

        Returns:
            None
        """
        # Find all child widgets of type QPushButton within the current widget (main window)
        children_btns = self.findChildren(QPushButton)

        # Check if any QPushButton child widgets were found
        if children_btns:
            # Iterate over each QPushButton found and Remove it from the status bar
            for child_btn in children_btns:
                self.statusbar.removeWidget(child_btn)

    def close_dialog(self, dialog):
        """
        Close a dialog window and clear selections in the main window.

        This method takes a dialog window as input and closes it. After closing the dialog,
        it clears the selections in the main window.

        Args:
            dialog: The dialog window to be closed.

        Returns:
            None
        """
        # Close the dialog window
        dialog.close()

        # Clear the selections in the main window
        self.clear_selection()


class InsertDialog(QDialog):
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

        # Set the fixed size of the dialog
        self.setFixedSize(200, 200)

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
        button.setFixedHeight(30)
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
        # Get inputs from the user
        name = self.student_name.text().strip().title()
        course = self.course_name.currentText()
        phone = self.phone_number.text().strip()

        # Validate inputs
        valid, warning = self.validate_insert_inputs(name, course, phone)

        # If inputs are not valid, display a warning message
        if not valid:
            QMessageBox.warning(self, "Invalid Input", warning)

            # Based on warning code, set focus to the respective input field (1: Name input field, 2: Course input field, 3: Phone number input field)
            match int(warning[0]):
                case 1:
                    self.student_name.setFocus()  # Set focus to student name input field
                case 2:
                    self.course_name.setFocus()   # Set focus to course input field
                case 3:
                    self.phone_number.setFocus()  # Set focus to phone number input field

        else:
            # Once all inputs are valid, proceed to Establish a connection to the SQLite database and create a cursor object within a with statement
            try:
                with sqlite3.connect(DB_FILE) as connection:
                    cursor = connection.cursor()

                    # Execute the SQL query to insert a new student record
                    cursor.execute(INSERT_STUDENT_QUERY,
                                   (name, course, phone))
                    # Commit changes to the database
                    connection.commit()

                    # Reset the inputs
                    self.clear_inputs()
                    # Reload the table data after the insert dialog is finished
                    self.parent_window.load_table_data()
                    # Log success message
                    success_msg = f'Student record for "{
                        name}" added successfully.'
                    QMessageBox.information(self, "Success", success_msg)
                    logging.info(success_msg)

            except sqlite3.Error as e:
                # Rollback changes if an error occurs
                error_msg = f'Error adding student record for "{name}"'
                QMessageBox.critical(self, "Error", error_msg)
                logging.error(f"{error_msg}: {e}")

    def validate_insert_inputs(self, name, course, phone):
        """
        Validates the inputs for adding a new student record.

        Args:
            name (str): The name of the student.
            course (str): The course of the student.
            phone (str): The phone number of the student.

        Returns:
            tuple: A tuple containing a boolean indicating whether the inputs are valid 
                   and a warning message if any, otherwise None.
        """
        warning_msg = ""

        # Validate name
        if not re.match(NAME_PATTERN, name):
            warning_msg += "1- Name is invalid. Please use alphabet letters in the format:\n   <first_name last_name>. "

        # Validate course
        if course == 'Select Course':
            warning_msg += "\n2- Please select a course. "

        # Validate phone number
        if not re.match(PHONE_NUMBER_PATTERN, phone):
            warning_msg += "\n3- Phone number is invalid. It must be 8 digits in length. "

        # Check if any warning messages were generated
        if warning_msg:
            return False, warning_msg.strip()  # Return False and the warning message

        # Return True indicating all inputs are valid
        return True, None

    def clear_inputs(self):
        """
        Clear all input fields in the dialog.
        """
        # Clear input fields
        self.student_name.clear()
        self.course_name.setCurrentIndex(0)  # Assuming the default index is 0
        self.phone_number.clear()


class SearchDialog(QDialog):
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

        # Set the fixed size of the dialog
        self.setFixedSize(200, 100)

        self.setWindowTitle("Search Student")

        # Layout
        layout = QVBoxLayout()

        # Create widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        button = QPushButton("Search")
        button.setFixedHeight(30)
        button.clicked.connect(self.search_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
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
                row_i = record.row()

                # Iterate over each column in the table
                for col_i in range(self.parent_window.table.columnCount()):
                    # Set the current cell as selected, indicating it's part of the found record
                    self.parent_window.table.item(
                        row_i, col_i).setSelected(True)

            # Log a success message
            success_msg = f'Student record for "{
                this_name}" found and highlighted successfully.'
            logging.info(success_msg)

            # Close the dialog if the student is found
            self.close()

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
            error_msg = f"Error searching in database for {student_name}"
            QMessageBox.critical(self, "Error", error_msg)
            logging.error(f"{error_msg}: {e}")

        finally:
            # Close the cursor and connection
            if 'cursor' in locals() and cursor:  # or simply `if cursor:`
                cursor.close()

        # Return True if student exists, False otherwise (in case of error list will be empty still so bool() returns False)
        return bool(this_student_rows)


class EditDialog(QDialog):
    """
    Dialog for editing a student record.
    """

    def __init__(self, parent):
        """
        Initializes the dialog window.
        """
        super().__init__()

        # Get hold of the parent window calling this dialog in order to access it
        self.parent_window = parent

        # Set the fixed size of the dialog
        self.setFixedSize(200, 200)

        self.setWindowTitle("Update Student Data")

        # Get this selected user data
        # Get the index of the currently selected row in the table
        row_i = self.parent_window.table.currentRow()
        # Get the student's id of the item in the first column (index 0) of the currently selected row
        self.student_id = self.parent_window.table.item(row_i, 0).text()
        # Get the student's name of the item in the second column (index 1) of the currently selected row
        self.initial_name = self.parent_window.table.item(row_i, 1).text()
        # Get the student's course of the item in the third column (index 2) of the currently selected row
        self.initial_course = self.parent_window.table.item(row_i, 2).text()
        # Get the student's phone number of the item in the fourth column (index 3) of the currently selected row
        self.initial_phone = self.parent_window.table.item(row_i, 3).text()

        # Layout
        layout = QVBoxLayout()

        # Create widgets and populate them with selected student data
        self.student_name = QLineEdit(self.initial_name)

        self.course_name = QComboBox()
        self.course_name.addItems(COURSES)
        self.course_name.setCurrentText(self.initial_course)

        self.phone_number = QLineEdit(self.initial_phone)

        button = QPushButton("Save")
        button.setFixedHeight(30)
        button.clicked.connect(self.update_student)

        # Add widgets to layout
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.phone_number)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        """
        Updates a student record in the SQLite database.
        """
        # Prompt the user for confirmation before updating
        if self.confirm_update():
            # Get inputs from the user
            name = self.student_name.text().strip().title()
            course = self.course_name.currentText()
            phone = self.phone_number.text().strip()

            # Validate inputs
            valid, warning = self.validate_update_inputs(name, course, phone)

            # If inputs are not valid, display a warning message
            if not valid:
                QMessageBox.warning(self, "Invalid Input", warning)

                # Based on warning code, set focus to the respective input field (1: Name input field, 2: Course input field, 3: Phone number input field)
                match int(warning[0]):
                    case 1:
                        self.student_name.setFocus()  # Set focus to student name input field
                    case 2:
                        self.course_name.setFocus()   # Set focus to course input field
                    case 3:
                        self.phone_number.setFocus()  # Set focus to phone number input field

            else:
                # if user hasn't made any modifications to this student record
                if warning:
                    QMessageBox.information(
                        self, "Info", warning)

                else:
                    # Once all inputs are valid and new data entered (modified), proceed to Establish a connection to the SQLite database and create a cursor object within a with statement
                    try:
                        with sqlite3.connect(DB_FILE) as connection:
                            cursor = connection.cursor()

                            # Execute the SQL query to insert a new student record
                            cursor.execute(UPDATE_STUDENT_QUERY,
                                           (name, course, phone, self.student_id))
                            # Commit changes to the database
                            connection.commit()

                            # Close the dialog if the student is updated
                            self.parent_window.close_dialog(self)
                            # Reload the table data after the update dialog is finished
                            self.parent_window.load_table_data()
                            # Log success message
                            success_msg = f'Student record for "{
                                name}" updated successfully.'
                            QMessageBox.information(
                                self, "Success", success_msg)
                            logging.info(success_msg)

                    except sqlite3.Error as e:
                        # Rollback changes if an error occurs
                        error_msg = f'Error updating student record for "{
                            name}"'
                        QMessageBox.critical(self, "Error", error_msg)
                        logging.error(f"{error_msg}: {e}")

    def validate_update_inputs(self, name, course, phone):
        """
        Validates the inputs for updating a student record.

        Args:
            name (str): The name of the student.
            course (str): The course of the student.
            phone (str): The phone number of the student.

        Returns:
            tuple: A tuple containing a boolean indicating whether the inputs are valid 
                   and a warning message if any, otherwise None.
        """
        warning_msg = ""

        # If no modifications recorded then return True (valid) with a message of no changes made
        if (name == self.initial_name and
            course == self.initial_course and
                phone == self.initial_phone):
            return True, "No modifications have been made, no update required. "

        # Validate name
        if not re.match(NAME_PATTERN, name):
            warning_msg += "1- Name is invalid. Please use alphabet letters in the format:\n   <first_name last_name>. "

        # Validate course
        if course == 'Select Course':
            warning_msg += "\n2- Please select a course. "

        # Validate phone number
        if not re.match(PHONE_NUMBER_PATTERN, phone):
            warning_msg += "\n3- Phone number is invalid. It must be 8 digits in length. "

        # Check if any warning messages were generated
        if warning_msg:
            return False, warning_msg.strip()  # Return False and the warning message

        # Return True indicating all inputs are valid
        return True, None

    def confirm_update(self):
        """
        Display a confirmation dialog for updating a student record.

        This function creates a QMessageBox instance to prompt the user for confirmation before updating a student record.
        The dialog asks the user if they are sure they want to update the record.
        The user can confirm the update by clicking the "Yes" button or cancel it by clicking the "No" button.

        Returns:
            bool: True if the user confirms the update, False if the user cancels it.
        """
        # Create a QMessageBox instance
        msg_box = QMessageBox()

        msg_box.setWindowTitle(f"Update Confirmation")
        # Set the icon and text for the confirmation message box
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setText(f"Are you sure you want to update this record?")

        # Add buttons for confirmation and cancellation
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Set the default button to No, so pressing Enter defaults to cancel
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        # Execute the message box and wait for the user's response
        response = msg_box.exec()

        # Check the user's response
        if response == QMessageBox.StandardButton.Yes:
            # Return True to indicate the update was confirmed
            return True
        else:
            # Return False if the user cancels the update
            return False


class DeleteDialog(QDialog):
    """
    Dialog for deleting a student record.
    """

    def __init__(self, parent):
        """
        Initializes the dialog window.
        """
        super().__init__()

        # Get hold of the parent window calling this dialog in order to access it
        self.parent_window = parent

        # Set the fixed size of the dialog
        # self.setFixedSize(200, 100)

        self.setWindowTitle("Delete Student")

        # Get this selected user data
        # Get the index of the currently selected row in the table
        row_i = self.parent_window.table.currentRow()
        # Get the student's id of the item in the first column (index 0) of the currently selected row
        self.student_id = self.parent_window.table.item(row_i, 0).text()
        # Get the student's name of the item in the second column (index 1) of the currently selected row
        self.student_name = self.parent_window.table.item(row_i, 1).text()

        # Layout
        layout = QGridLayout()

        # Create widgets
        confirmation = QLabel(f'Are you sure you want to delete the student record for "{
                              self.student_name.title()}"?')

        # Create a grid layout for buttons
        buttons_grid = QGridLayout()

        yes_btn = QPushButton("Yes")
        yes_btn.setFixedWidth(50)
        yes_btn.clicked.connect(self.delete_student)

        no_btn = QPushButton("No")
        no_btn.setFixedWidth(50)
        # use lambda to add args
        no_btn.clicked.connect(lambda: self.parent_window.close_dialog(self))

        # Add buttons to the button grid
        buttons_grid.addWidget(yes_btn, 1, 0)
        buttons_grid.addWidget(no_btn, 1, 1)

        # Add widgets to layout
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addLayout(buttons_grid, 1, 1)

        self.setLayout(layout)

    def delete_student(self):
        """
        Deletes the current selected student record in the SQLite database.
        """
        # Establish a connection to the SQLite database and create a cursor object within a with statement
        try:
            with sqlite3.connect(DB_FILE) as connection:
                cursor = connection.cursor()

                # Execute the SQL query to insert a new student record
                cursor.execute(DELETE_STUDENT_QUERY, (self.student_id, ))
                # Commit changes to the database
                connection.commit()

                # Close the dialog if the student is deleted
                self.parent_window.close_dialog(self)
                # Reload the table data after the delete dialog is finished
                self.parent_window.load_table_data()
                # Log success message
                success_msg = f'Student record for "{
                    self.student_name}" deleted successfully.'
                QMessageBox.information(self, "Success", success_msg)
                logging.info(success_msg)

        except sqlite3.Error as e:
            # Rollback changes if an error occurs
            error_msg = f'Error deleting student record for "{
                self.student_name}"'
            QMessageBox.critical(self, "Error", error_msg)
            logging.error(f"{error_msg}: {e}")


class AboutDialog(QMessageBox):
    """
    Dialog to display info about the app.
    """

    def __init__(self, parent):
        """
        Initializes the dialog window.
        """
        super().__init__()

        self.setWindowTitle("About")
        content = """
<h3>About This App</h3>
<p>Student Management System is a comprehensive Python application designed to streamline the management of student records within educational institutions. Built using PyQt6 for the graphical user interface and SQLite for data storage, this system offers a user-friendly interface for administrators to efficiently handle student data.
</p>
<p>
The primary goal of this system is to simplify the process of managing student information, including their names, courses, and contact details. It provides a centralized platform where administrators can seamlessly perform tasks such as adding new students, searching for specific records, editing existing entries, and deleting outdated information.
</p>
<p>
The application's database schema is included, offering users the flexibility to customize and expand the database structure according to their specific requirements. Users are free to add new columns or data as preferred, ensuring adaptability to evolving needs and preferences.
</p>
<p>
By leveraging Object-Oriented Programming (OOP) principles, the application is structured into modular components, enhancing maintainability and scalability. Each component, from the main window to the various dialog boxes, encapsulates specific functionalities, promoting code reusability and clarity.
</p>
<p>
The graphical interface features intuitive controls, including a toolbar for quick access to common actions and a status bar that dynamically adjusts based on user interactions. Notably, the status bar displays contextual buttons for editing and deleting student records only when a row is selected, ensuring a streamlined user experience.
</p>
<p>
With robust error handling mechanisms in place, the system maintains reliability and transparency in database operations. Administrators can rely on detailed log messages to track successful operations and diagnose any errors or exceptions that may occur during runtime. The error handling architecture is designed to be expandable, allowing for easy integration of additional error handling functionalities as needed.
</p>
<p>
Overall, Student Management System serves as a powerful tool for educational institutions, offering an efficient and organized approach to managing student records. Whether it's maintaining up-to-date information or performing routine administrative tasks, this application empowers administrators to effectively oversee student data management with ease.</p>
<p>Developed by: emads22</p>
<p>Version: 1.0.0</p>
<p>© 2024 E></p>
<p>All rights reserved.</p>
"""
        self.setText(content)