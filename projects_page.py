from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QComboBox, QScrollArea, QMenu
from DragAndDropWidgets import *
import sys
class TaskGroupNameInput(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(360, 220)
        self.task_group_input = QLineEdit()
        self.setWindowTitle("Add New Task")
        self.setUpWindow()

    def setUpWindow(self):
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#EDE3E9;color:black;")

        # widgets within and their attributes
        top_label = QLabel("NEW TASK GROUP")

        self.save_group_name_button = QPushButton("Save")
        self.cancel_group_button = QPushButton("Cancel")
        top_label.setFont(QFont("Arial", 17))
        top_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.save_group_name_button.setStyleSheet("border: 1px dotted black;background-color:#E6E4CE")
        self.cancel_group_button.setStyleSheet("border: 1px dotted black;background-color:#EBC3DB")

        # slots and signals
        self.cancel_group_button.clicked.connect(self.reject)
        # layouts
        buttons_lay = QHBoxLayout()
        buttons_lay.addWidget(self.cancel_group_button)
        buttons_lay.addWidget(self.save_group_name_button)

        inner_lay = QVBoxLayout()
        inner_lay.addWidget(top_label)
        inner_lay.addWidget(self.task_group_input)

        main_lay = QVBoxLayout()
        main_lay.addLayout(inner_lay)
        main_lay.addSpacing(50)
        main_lay.addLayout(buttons_lay)
        self.setLayout(main_lay)
class ProjectNameInput(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(360, 220)
        self.save_project_name_button = QPushButton("Save")
        self.project_name_input = QLineEdit()
        self.project_due_input = QDateEdit()
        self.setWindowTitle("Set Project Name")
        self.setUpWindow()

    def setUpWindow(self):
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#EDE3E9;color:black;")

        self.project_due_input.setCalendarPopup(True)
        self.project_due_input.setMinimumDate(QDate.currentDate())
        self.project_due_input.setDisplayFormat("dd-MMM-yyyy")

        # widgets within and their attributes
        top_label = QLabel("Project Name")
        self.cancel_project_button = QPushButton("Cancel")
        top_label.setFont(QFont("Arial", 17))
        top_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.save_project_name_button.setStyleSheet("border: 1px dotted "
                                                 "black;background-color:#E6E4CE")
        self.cancel_project_button.setStyleSheet("border: 1px dotted "
                                                 "black;background-color:#EBC3DB")

        # slots and signals
        self.cancel_project_button.clicked.connect(self.reject)
        # layouts
        buttons_lay = QHBoxLayout()
        buttons_lay.addWidget(self.cancel_project_button)
        buttons_lay.addWidget(self.save_project_name_button)

        inner_lay = QFormLayout()
        inner_lay.addRow("Project Name:", self.project_name_input)
        inner_lay.addRow("Project Due:", self.project_due_input)

        main_lay = QVBoxLayout()
        main_lay.addWidget(top_label)
        main_lay.addLayout(inner_lay)
        main_lay.addSpacing(50)
        main_lay.addLayout(buttons_lay)
        self.setLayout(main_lay)

class CustomLayout(QHBoxLayout):
    """"""


class ProjectPageTasks(QWidget):
    """ Creates the Layout of the task group section of the project page"""
    def __init__(self):
        super().__init__()
        self.task_groups_list = []
        self.add_task_group = QPushButton()
        self.setUpGroups()
    def setUpGroups(self):
        self.add_task_group = QPushButton()
        self.group_sort = QComboBox()
        self.add_task_group.setIcon(QIcon("ICONS/add.png"))
        self.add_task_group.setIconSize(QSize(20, 20))
        self.add_task_group.setStyleSheet("background-color:#E8B4BC")

        # signals and slots
        self.add_task_group.clicked.connect(self.collect_input)

        # set up layout
        top_lay = QHBoxLayout()
        top_lay.addSpacing(200)
        top_lay.addWidget(self.group_sort)

        self.project_lay = QVBoxLayout()
        self.project_lay.addLayout(top_lay)

        self.main_widget_lay = QHBoxLayout()
        self.main_widget_lay.addWidget(self.add_task_group)
        self.project_lay.addLayout(self.main_widget_lay)
        self.setLayout(self.project_lay)

    def collect_input(self):
        self.group_name_input = TaskGroupNameInput(self)
        self.group_name_input.show()
        self.group_name_input.save_group_name_button.clicked.connect(self.add_group)
    def add_group(self):
        self.group_name_input.close()
        new_group = DragWidget()
        self.main_widget_lay.addWidget(new_group)
        self.main_widget_lay.addSpacing(30)
        group_name = self.group_name_input.task_group_input.text()
        new_group.task_group_label.setText(group_name)

    def load_group(self,group_name,task_list):
        old_group = DragWidget()
        old_group.task_group_label.setText(group_name)
        old_group.load_item(task_list)
        self.main_widget_lay.addWidget(old_group)
        self.main_widget_lay.addSpacing(30)


class ProjectPageMain(QWidget):
    def __init__(self):
        super().__init__()
        self.project_name = QLabel('Project Name Here')
        self.project_due = QLabel()
        self.delete_act = QAction("Delete Project")
        self.project_id = None
        self.main = ProjectPageTasks()
        self.setUpProjectDisplay()
    def setUpProjectDisplay(self):
        self.main_lay = QVBoxLayout()
        topper_lay = QHBoxLayout()

        self.edit_button = QPushButton()
        edit_menu = QMenu()
        self.change_name_act = QAction("Change Project Name")
        edit_menu.addAction(self.change_name_act)
        edit_menu.addAction(self.delete_act)
        self.edit_button.setMenu(edit_menu)

        self.project_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        topper_lay.addWidget(self.project_name)
        topper_lay.addSpacing(10)
        topper_lay.addWidget(self.project_due)
        topper_lay.addSpacing(100)

        topper_lay.addWidget(self.edit_button)

        # signals and slots


        self.main_lay.addLayout(topper_lay)
        # setting up the scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setWidget(self.main)
        self.main_lay.addWidget(scroll_area)
        self.setLayout(self.main_lay)
