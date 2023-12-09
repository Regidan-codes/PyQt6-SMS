import sqlite3

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')

        # add top left icons
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # expanding top left icons
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Adding table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    # populating data in table
    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM STUDENTS")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Adding student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Adding course name widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Adding Mobile number widget
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile_number)

        # Add submit button
        button = QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO STUDENTS  (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()


app = QApplication(sys.argv)
student_management = MainWindow()
student_management.show()
student_management.load_data()
sys.exit(app.exec())