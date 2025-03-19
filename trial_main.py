from PyQt6.QtWidgets import QWidget,QApplication,QMainWindow
import sys
from trial import*

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initializeUI()
        self.show()
    def initializeUI(self):
        self.ui.sidebar.hide()
        # changing the pages
        self.ui.home_button.clicked.connect(lambda:self.changePage(0))
        self.ui.proj_button.clicked.connect(lambda:self.changePage(1))
        self.ui.tasks_button.clicked.connect(lambda:self.changePage(2))
        self.ui.stats_button.clicked.connect(lambda:self.changePage(3))
        self.ui.quit_button.clicked.connect(self.close)
    def changePage(self,index):
        self.ui.stackedWidget.setCurrentIndex(index)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
