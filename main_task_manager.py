from PyQt6.QtWidgets import QWidget,QApplication,QMainWindow,QMessageBox
import sys
from task_manager import*
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlRelationalDelegate, \
    QSqlTableModel
from PyQt6.QtCore import Qt
from DragAndDropWidgets import *
from projects_page import *
import datetime
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.projects_list = []
        self.createConnection()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initializeUI()

    def initializeUI(self):
        self.createModel()
        self.setUpMainWindow()
        self.group_count = 0
        self.show()

    def input_collectors(self):

        self.task_details_input_collector = TaskInputWindow(self)
        self.task_group_details_input_collector = TaskGroupNameInput(self)

    def createConnection(self):
        """ Creates database """
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("assets/databse.db")

        if not self.database.open():
            QMessageBox.critical(self, "Fail", "Error:Databse "
                                               "connection failed",
                                 QMessageBox.StandardButton.Ok)
            sys.exit(1)
        needed_tables = {"tasks", "projects", "task_groups"}
        tables_not_found = needed_tables - set(self.database.tables())
        if tables_not_found:
            # first time message and setting up the database tables
            QMessageBox.information(self, "WELCOME", "YAYY THANKS FOR TRYING OUT THE ORGANIZER",
                                    QMessageBox.StandardButton.Ok)
            task_query = QSqlQuery()
            task_query.exec("DROP TABLE tasks")
            task_query.exec("""CREATE TABLE tasks(
                            group_id INTEGER REFERENCES task_groups(group_id),
                           task_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                           task_name VARCHAR(120) NOT NULL,
                           task_date DATE,
                           task_time TIME,
                           task_status INTEGER DEFAULT 0


               )""")
            project_query = QSqlQuery()
            project_query.exec("DROP TABLE projects")
            project_query.exec("""CREATE TABLE projects(
                       project_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                       project_name VARCHAR(120) NOT NULL,
                       project_due_date DATE,
                       project_progress INTEGER DEFAULT 0,
                       project_status INTEGER DEFAULT 0


               )""")
            group_query = QSqlQuery()
            group_query.exec("DROP TABLE task_groups")
            group_query.exec(""" CREATE TABLE task_groups(
                       group_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                       project_id INTEGER REFERENCES projects(project_id),
                       group_name VARCHAR(200) NOT NULL,
                       group_status INTEGER DEFAULT 0
               )""")


    def changePage(self,index):
        self.ui.stackedWidget.setCurrentIndex(index)
    def createModel(self):
        self.tasks_model = QSqlRelationalTableModel()
        self.tasks_model.setTable("tasks")
        self.tasks_model.select()

        self.projects_model = QSqlRelationalTableModel()
        self.projects_model.setTable('projects')
        self.projects_model.select()

        self.task_groups_model = QSqlRelationalTableModel()
        self.task_groups_model.setTable('task_groups')
        self.task_groups_model.select()


    def setUpMainWindow(self):
        self.ui.sidebar.hide()  # for minimizer functionality
        # changing the pages of stacked widget
        self.ui.home_button.clicked.connect(lambda: self.changePage(0))
        self.ui.proj_button.clicked.connect(lambda: self.changePage(1))
        self.ui.tasks_button.clicked.connect(lambda: self.changePage(2))
        self.ui.stats_button.clicked.connect(lambda: self.changePage(3))
        self.ui.quit_button.clicked.connect(self.close)

        # creating the table view for tasks in home page

        self.ui.tasks_table_view.setModel(self.tasks_model)
        self.ui.tasks_table_view.horizontalHeader().setVisible(False)
        self.ui.tasks_table_view.verticalHeader().setVisible(False)
        self.ui.tasks_table_view.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tasks_table_view.hideColumn(0)
        self.ui.tasks_table_view.hideColumn(2)
        self.ui.tasks_table_view.hideColumn(4)
        self.ui.tasks_table_view.hideColumn(5)
        self.ui.tasks_table_view.setColumnWidth(1,100)
        self.ui.tasks_table_view.setColumnWidth(3,400)
        # setting the delegate what is this idk yet
        tasks_delegate = QSqlRelationalDelegate()
        self.ui.tasks_table_view.setItemDelegate(tasks_delegate)
        # setting up the projects page
        self.setUpProjectsPage()
        self.ui.project_buttoncb.setMinimumSize(100,30)
        self.ui.project_buttoncb.activated.connect(self.switch_project_page)

        c_query = QSqlQuery()
        c_query.exec("SELECT COUNT (project_id) FROM projects")
        while (c_query.next()):
            self.projs_in_db = c_query.value(0)

    def setUpProjectsPage(self):
        main_page_widget = QWidget()
        add_project_button = QPushButton()
        add_project_button.clicked.connect(self.create_new_project)

        main_page_lay = QVBoxLayout()
        main_page_lay.addWidget(add_project_button)
        main_page_widget.setLayout(main_page_lay)

        self.ui.main_project_stackedWidget.addWidget(main_page_widget)
        self.ui.project_buttoncb.addItem(QIcon("ICONS/project.png"),"PROJECTS")

        self.load_existing_projects()

    def create_new_project(self):
        self.project_name_collector = ProjectNameInput(self)
        self.project_name_collector.show()
        self.project_name_collector.save_project_name_button.clicked.connect(self.create_new_project_page)
    def create_new_project_page(self):


        new_proj = ProjectPageMain()
        proj_name = self.project_name_collector.project_name_input.text()
        proj_date = self.project_name_collector.project_due_input.date()
        proj_id = self.projs_in_db + 1

        self.ui.main_project_stackedWidget.addWidget(new_proj)


        new_proj.project_name.setText(proj_name)
        new_proj.project_due.setText(proj_date.toString())
        new_proj.project_id = proj_id
        new_proj.delete_act.triggered.connect(self.delete_project_page)

        self.ui.project_buttoncb.addItem(proj_name)

        # saving the project into the database
        query = QSqlQuery()
        query.prepare("INSERT INTO projects(project_id,project_name,project_due_date) VALUES(?,?,"
                      "?)")
        query.addBindValue(proj_id)
        query.addBindValue(proj_name)
        query.addBindValue(proj_date)
        query.exec()


        self.project_name_collector.close()
        self.projects_list.append(new_proj)


    def checker(self,id):
        print(" group created")

    def load_existing_projects(self):
        query = QSqlQuery()
        query.exec("SELECT project_id,project_name,project_due_date FROM projects")
        while query.next():
            id = query.value(0)
            name = query.value(1)
            date = query.value(2)
            # creating the project page objects
            old_proj = ProjectPageMain()
            self.ui.main_project_stackedWidget.addWidget(old_proj)
            old_proj.project_name.setText(name)
            old_proj.project_due.setText(date)
            old_proj.project_id = id
            old_proj.delete_act.triggered.connect(self.delete_project_page)
            self.ui.project_buttoncb.addItem(name)
            self.projects_list.append(old_proj)

            # loading the groups of the project
            g_query = QSqlQuery()
            g_query.exec(f"SELECT group_id,group_name FROM task_groups WHERE project_id ={id}")
            while g_query.next():
                tasks = []
                group_i = g_query.value(0)
                group_n = g_query.value(1)
                t_query = QSqlQuery()
                t_query.exec(f"SELECT task_name,task_date,task_time FROM tasks WHERE group_id = "
                             f"{group_i}")
                while t_query.next():
                    task = []
                    t_name = t_query.value(0)
                    t_date = t_query.value(1)
                    t_time = t_query.value(2)
                    task.append(t_name)
                    task.append(t_date)
                    task.append(t_time)
                    tasks.append(task)
                old_proj.main.load_group(group_n,tasks)
    def switch_project_page(self,index):
        self.changePage(1)
        self.ui.main_project_stackedWidget.setCurrentIndex(index)
    def delete_project_page(self):
        to_del = self.ui.project_buttoncb.currentIndex()
        widget_to_del = self.ui.main_project_stackedWidget.currentWidget()
        self.ui.main_project_stackedWidget.removeWidget(widget_to_del)
        self.ui.project_buttoncb.removeItem(to_del)




    def closeEvent(self, event):
        p_query = QSqlQuery()
        g_query = QSqlQuery()
        t_query = QSqlQuery()

        p_query.prepare("INSERT INTO projects(project_name,project_due_date) VALUES(?,?)")
        g_query.prepare("INSERT INTO task_groups(project_id,group_name) VALUES(?,?)")
        t_query.prepare("INSERT INTO tasks(group_id,task_name,task_date,task_time) VALUES(?,?,?,?)")
        for project in self.projects_list:# project is a projectPageMain obj
            proj_id = project.project_id
            for group in project.main.task_groups_list:# group is dragWidget obj
                self.group_count+=1
                g_query.addBindValue(proj_id)
                g_query.addBindValue(group.task_group_label.text())
                g_query.exec()
                for task in group.task_list:# task is dragItem obj
                    t_query.addBindValue(self.group_count)
                    t_query.addBindValue(task.task_label.text())
                    t_query.addBindValue(task.date_label.text())
                    t_query.addBindValue(task.time_label.text())
                    t_query.exec()


        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
