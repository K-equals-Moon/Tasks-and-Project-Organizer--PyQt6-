from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, Qt, QSize
import sys

class TaskInputWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.output = []
        self.setFixedSize(360,220)
        self.setWindowTitle("Add New Task")
        self.setUpWindow()
        self.show()
    def setUpWindow(self):
        self.date_value = False
        top_label = QLabel("Add Task")
        top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_label.setFont(QFont("Arial",17))

        self.task_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd-MMM-yyyy")
        self.date_input.dateChanged.connect(self.date_changed)

        self.task_input.resize(QSize(250,20))
        self.date_input.resize(QSize(250,20))


        task_lay = QFormLayout()
        self.save_button = QPushButton("Save Task")
        self.save_button.setEnabled(False)
        cancel_button = QPushButton("Cancel")
        # slots and signals
        cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save_task)
        self.task_input.textEdited.connect(self.enable_add)

        # layouts
        buttons_lay = QHBoxLayout()
        buttons_lay.addWidget(cancel_button)
        buttons_lay.addWidget(self.save_button)
        task_lay.addRow("Task Name:",self.task_input)

        task_lay.addRow("Due Date:",self.date_input)
        main_lay = QVBoxLayout()
        main_lay.addWidget(top_label)
        main_lay.addLayout(task_lay)
        main_lay.addLayout(buttons_lay)
        self.setLayout(main_lay)
    def date_changed(self):
        self.date_value = True
        return self.date_value

    def enable_add(self):
        if len(self.task_input.text()) > 0:
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def save_task(self):
        task_name = self.task_input.text()
        self.output.append(task_name)
        if self.date_value:
            due_date = self.date_input.date().toString()
        else:
            due_date = ""
        self.output.append(due_date)
        self.printer()
        self.task_input.clear()
    def printer(self):
        print(self.output)

app = QApplication([])
window = TaskInputWindow()
sys.exit(app.exec())

