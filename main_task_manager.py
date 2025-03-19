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
        self.projects_count = 0
        self.createConnection()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initializeUI()

    def initializeUI(self):
        self.createModel()
        self.setUpMainWindow()
        self.show()

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
        self.projects_count +=1
        self.new_proj = ProjectPageMain()
        self.ui.main_project_stackedWidget.addWidget(self.new_proj)
        self.new_proj.project_name.setText(self.project_name_collector.project_name_input.text())
        self.new_proj.project_due.setText(self.project_name_collector.project_due_input.date(

        ).toString())
        self.new_proj.project_id = self.projects_count
        self.new_proj.delete_act.triggered.connect(self.delete_project_page)

        proj_name = self.new_proj.project_name.text()
        self.ui.project_buttoncb.addItem(proj_name)
        # saving the project into the database
        query = QSqlQuery()
        query.prepare("INSERT INTO projects(project_id,project_name,project_due_date) VALUES(?,?,"
                      "?)")
        date = self.new_proj.project_due.text()
        query.addBindValue(self.new_proj.project_id)
        query.addBindValue(proj_name)
        query.addBindValue(date)
        query.exec()


        # switching the page to the newly opened project
        self.project_name_collector.close()

        # saving task groups created into database
        self.new_proj.main.add_task_group.clicked.connect(self.create_new_group)


    def load_existing_projects(self):
        query = QSqlQuery()
        query.exec("SELECT project_name,project_due_date FROM projects")
        while query.next():

            name = query.value(0)
            date = query.value(1)
            # creating the project page objects
            old_proj = ProjectPageMain()
            self.ui.main_project_stackedWidget.addWidget(old_proj)
            old_proj.project_name.setText(name)
            old_proj.project_due.setText(date)
            old_proj.delete_act.triggered.connect(self.delete_project_page)
            self.ui.project_buttoncb.addItem(name)
    def switch_project_page(self,index):
        self.changePage(1)
        self.ui.main_project_stackedWidget.setCurrentIndex(index)
    def delete_project_page(self):
        to_del = self.ui.project_buttoncb.currentIndex()
        widget_to_del = self.ui.main_project_stackedWidget.currentWidget()
        self.ui.main_project_stackedWidget.removeWidget(widget_to_del)
        self.ui.project_buttoncb.removeItem(to_del)




    def closeEvent(self, event):
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
