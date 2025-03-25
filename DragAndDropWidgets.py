from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QLabel,
                             QDialog, QVBoxLayout, QGraphicsOpacityEffect, QLineEdit, QDateEdit,
                             QFormLayout, QMessageBox, QTimeEdit, QScrollArea)
from PyQt6.QtGui import QDrag, QPixmap, QIcon, QFont
from PyQt6.QtCore import QMimeData, Qt, QDate, pyqtSignal, QSize
import random
from PyQt6.QtSql import QSqlDatabase,QSqlQuery,QSqlRelationalTableModel,QSqlRelationalDelegate
import sys

class DragTargetIndicator(QLabel):
    def __init__(self,parent=None):
        super().__init__()
        self.setContentsMargins(25,5,25,5)
        self.setMinimumHeight(80)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.setGraphicsEffect(self.opacity_effect)
        self.setStyleSheet("background-color:#FEF9FF;border-radius:5px;")
class TaskInputWindow(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.cancel_button = QPushButton("Cancel")
        self.setFixedSize(360, 220)
        self.setWindowTitle("Add New Task")
        self.setUpWindow()


    def setUpWindow(self):
        self.setModal(True)
        self.date_value = False
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color:#EDE3E9;color:black;")
        # widgets within and their attributes

        # widgets and widget attributes
        top_label = QLabel("Add Task")
        self.task_input = QLineEdit()
        self.date_input = QDateEdit()
        self.time_input = QTimeEdit()
        self.save_button = QPushButton("Save Task")
        self.save_button.setEnabled(False)
        self.cancel_button = QPushButton("Cancel")

        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd-MMM-yyyy")
        self.time_input.setDisplayFormat("hh:mm ap")

        top_label.setFont(QFont("Arial", 17))
        top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.task_input.setMinimumWidth(250)
        self.date_input.setMinimumWidth(250)
        self.time_input.setMinimumWidth(250)
        self.time_input.setStyleSheet("border: 1px solid black")
        self.task_input.setStyleSheet("border: 1px solid black")
        self.date_input.setStyleSheet("border: 1px solid black")
        self.save_button.setStyleSheet("border: 1px dotted black;background-color:#E6E4CE")
        self.cancel_button.setStyleSheet("border: 1px dotted black;background-color:#EBC3DB")

        # slots and signals
        self.cancel_button.clicked.connect(self.reject)
        self.task_input.textEdited.connect(self.enable_add)
        self.date_input.dateChanged.connect(self.date_changed)

        # layouts
        buttons_lay = QHBoxLayout()
        buttons_lay.addWidget(self.cancel_button)
        buttons_lay.addWidget(self.save_button)

        task_lay = QFormLayout()
        task_lay.addRow("Task Name:",self.task_input)
        task_lay.addRow("Due Date:",self.date_input)
        task_lay.addRow("Due Time",self.time_input)

        main_lay = QVBoxLayout()
        main_lay.addWidget(top_label)
        main_lay.addLayout(task_lay)
        main_lay.addSpacing(30)
        main_lay.addLayout(buttons_lay)
        self.setLayout(main_lay)
    def date_changed(self):
        self.date_value = True
        return self.date_value

    def enable_add(self):
        if len(self.task_input.text()) > 0:
            self.save_button.setEnabled(True)
        elif len(self.task_input.text()) <=0:
            self.save_button.setEnabled(False)

class DragItem(QWidget):
    def __init__(self):
        super().__init__()
        self.task_label = QLabel()
        self.date_label = QLabel()
        self.time_label = QLabel()
        self.task_status = 0
        self.setFixedSize(320,100)
        self.setUpItem()
    def __str__(self):
        return self.task_label.text() + "--" + self.date_label.text() + self.time_label.text()
    def setUpItem(self):
        # widget attributes
        self.setContentsMargins(25, 5, 25, 5)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)
        self.setStyleSheet("background-color:#FEF9FF; border-radius:5px;color:black;")
        # widgets within and their attributes
        self.task_label.setWordWrap(True)
        self.task_label.setObjectName("taskName")
        self.done_button = QPushButton()
        self.done_button.setCheckable(True)
        self.done_button.setIcon(QIcon("ICONS/check_b.png"))
        self.done_button.setIconSize(QSize(15, 15))

        self.due_label = QLabel("Due:")

        self.date_label.setObjectName("dueDate")

        self.time_label.setObjectName("dueTime")

        # signals and slots
        self.done_button.toggled.connect(self.mark_as_complete)

        #layout set up
        h_box_lay = QHBoxLayout()
        date_h_box = QHBoxLayout()
        date_h_box.addWidget(self.due_label)
        date_h_box.addWidget(self.date_label)
        date_h_box.addWidget(self.time_label)

        h_box_lay.addLayout(date_h_box)
        h_box_lay.addWidget(self.done_button)


        main_lay = QVBoxLayout()
        main_lay.addWidget(self.task_label)
        main_lay.addLayout(h_box_lay)

        self.data = self.task_label.text() + self.date_label.text() + self.time_label.text()
        self.setLayout(main_lay)
    def mark_as_complete(self,passed):
        """ 1.changes the done_button icon lowers label opacity and adds strike through
        """

        font = QLabel.font(self)
        self.opacity_effect = QGraphicsOpacityEffect()
        opacity_2 =  QGraphicsOpacityEffect()
        opacity_3 =  QGraphicsOpacityEffect()
        opacity_4 = QGraphicsOpacityEffect()
        if passed == True:
            self.task_status = 1
            self.opacity_effect = QGraphicsOpacityEffect()
            self.opacity_effect.setOpacity(0.3)
            opacity_2.setOpacity(0.3)
            opacity_3.setOpacity(0.3)
            opacity_4 .setOpacity(0.3)

            self.done_button.setIcon(QIcon("ICONS/check_g.png"))
            self.done_button.setIconSize(QSize(15, 15))
            font.setStrikeOut(True)
        else:
            self.task_status = 0
            font.setStrikeOut(False)
            self.opacity_effect.setOpacity(1)
            opacity_2.setOpacity(1)
            opacity_3.setOpacity(1)
            self.done_button.setIcon(QIcon("ICONS/check_b.png"))
            self.done_button.setIconSize(QSize(15, 15))

        self.date_label.setFont(font)
        self.due_label.setFont(font)
        self.task_label.setFont(font)
        self.time_label.setFont(font)

        self.task_label.setGraphicsEffect(self.opacity_effect)
        self.date_label.setGraphicsEffect(opacity_2)
        self.due_label.setGraphicsEffect(opacity_3)
        self.time_label.setGraphicsEffect(opacity_4)



    def set_data(self,task_data,date_data,time_data):
        self.task_label.setText(task_data)
        self.date_label.setText(date_data)
        self.time_label.setText(time_data)
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)

class DragWidget(QWidget):

    orderChanged = pyqtSignal(list)

    def __init__(self,*args,orientation=Qt.Orientation.Vertical,**kwargs):
        super().__init__()
        self.task_list = []
        self.task_group_label = QLabel("TASK GROUP")
        self.setAcceptDrops(True)
        self.orientation = orientation
        self.setMinimumSize(325,350)
        self.setUpContainer()
    def __str__(self):
        return self.task_group_label.text()
    def setUpContainer(self):

        colors = {1:{"background":"#D4C1EC","button":"#736CED"},
                  2:{"background":"#0FA3B1","button":"#0A2463"},
                  3:{"background":"#E3C0D3","button":"#B5446E"},
                  4:{"background":"#BCF8EC","button":"#0091AD"},
                  5:{"background":"#C49E85","button":"#6B4B3E"},
                  6:{"background":"#BCD2EE","button":"#0A1045"},
                  7:{"background":"#FCF6BD","button":"#F3B700"}}
        choice = random.randrange(1,8)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color:{colors[choice]['background']};border-radius:3px")

        # widgets within and their attributes
        self.add_task_button = QPushButton("ADD TASK")

        self.add_task_button.setStyleSheet(f"border: 1.5px dashed {colors[choice]['button']};")

        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon("ICONS/edit.png"))
        self.edit_button.setIconSize(QSize(15,15))

        self.task_group_label.setFont(QFont("Arial", 15))
        self.task_group_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.drag_target_indicator = DragTargetIndicator()
        items_area = QWidget()

        self.drag_target_indicator.hide()



        # slots and signals
        self.add_task_button.clicked.connect(self.create_new_item)

        #layout setup
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.task_group_label)
        top_layout.addSpacing(100)
        top_layout.addWidget(self.edit_button)

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
            self.main_layout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()
            self.main_layout = QHBoxLayout()
        self.blayout.addWidget(self.drag_target_indicator)
        items_area.setLayout(self.blayout)
        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(items_area)
        self.main_layout.addWidget(self.add_task_button)

        self.setLayout(self.main_layout)

    def dragEnterEvent(self, e):
        e.accept()
    def dragLeaveEvent(self,e):
        self.drag_target_indicator.hide()
        e.accept()
    def dragMoveEvent(self, e):
        index = self._find_drop_location(e)
        if index is not None:
            self.blayout.insertWidget(index,self.drag_target_indicator)
            e.source().hide()
            self.drag_target_indicator.show()
        e.accept()
    def dropEvent(self,e):

        widget = e.source()
        self.drag_target_indicator.hide()
        index = self.blayout.indexOf(self.drag_target_indicator)
        if index is not None:
            self.blayout.insertWidget(index,widget)

            widget.show()
            self.blayout.activate()
        e.accept()

    def _find_drop_location(self,e):
        pos = e.position()
        spacing = self.blayout.spacing()

        for n in range (self.blayout.count()):
            w = self.blayout.itemAt(n).widget()

            if self.orientation == Qt.Orientation.Vertical:
                drop_here = (
                    pos.y() >= w.y() - spacing
                    and pos.y() <= w.y() + w.size().height() + spacing
                )

            else:
                drop_here = (
                    pos.x() >= w.x() - spacing
                    and pos.x() <= w.x() + w.size().width() + spacing
                )
            if drop_here:
                break
        return n

    def add_item(self,item):
        self.blayout.addWidget(item)
        self.task_list.append(item)
    def get_item_data(self):
        data = []
        for n in range (self.blayout.count()):
            w = self.blayout.itemAt(n).widget()
            if w != self.drag_target_indicator:
                data.append(w.data)
        return data
    def create_new_item(self):
        self.input_collector = TaskInputWindow(self)
        self.input_collector.show()
        self.input_collector.save_button.clicked.connect(self.save_task)
    def save_task(self):
        """ collecting the data from the dialog and creating a new item which is then added to
        drag container"""
        task_name = self.input_collector.task_input.text()
        task_time = self.input_collector.time_input.time().toString("hh-MM")

        if self.input_collector.date_value:
            due_date = self.input_collector.date_input.date().toString()

        else:
            due_date = ""

        new_item = DragItem()
        new_item.set_data(task_name,due_date,task_time)
        self.add_item(new_item)
        self.input_collector.task_input.clear()
        self.input_collector.save_button.setEnabled(False)

    def load_item (self,t_list):
        for task_details in t_list:
            name = task_details[0]
            date = task_details[1]
            time = task_details[2]
            status = task_details[3]
            old_item = DragItem()
            old_item.set_data(name,date,time)
            if status == 1:
                old_item.mark_as_complete(True)
                print(f"task {name} was checked")
            self.add_item(old_item)


