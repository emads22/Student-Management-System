import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow


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
