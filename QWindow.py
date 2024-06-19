from PyQt6.QtWidgets import QWidget,QComboBox,QVBoxLayout,QSystemTrayIcon,QMenu,QApplication,QPushButton,QDialog,QLabel
from PyQt6.QtGui import QIcon,QPixmap,QAction
from PyQt6.QtCore import QThread, pyqtSignal
import myJSON
import keyscan
import myDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300,100)
        self.setWindowTitle("ДДЮТ Sound Control")
        icon = QIcon(QPixmap("data\\Icon\\icon.png")) # добавление иконки на титульную полоску
        self.setWindowIcon(icon)
        self.fconfig = myJSON.FileJson()
        show_input_dialog()
        self.close()


        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("data\\Icon\\icon.png"))  

        tray_menu = QMenu()
        show_action = QAction("Показать окно", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(lambda:{self.fconfig.sprogname(self.prog_name_combo.currentText()),QApplication.quit()}) # 
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.iconActivated)
        self.tray_icon.show()
        
        layout = QVBoxLayout()
        self.prog_name_combo = QComboBox()
        self.prog_name_combo.setPlaceholderText('Выбрать программу..')
        self.prog_name_combo.addItem(QIcon(QPixmap("data\\Icon\\system.png")),"System")
        self.prog_name_combo.addItem(QIcon(QPixmap("data\\Icon\\aimp.png")),  "Aimp")
        self.prog_name_combo.addItem(QIcon(QPixmap("data\\Icon\\winamp.png")),"Winamp")
        self.prog_name_combo.setCurrentText(self.fconfig.finde_active_prog())
       
        self.CustomButton = MyButton('Add custom..',clicked=show_input_dialog,state=True)

        layout.addWidget(self.prog_name_combo)
        layout.addWidget(self.CustomButton)
        self.setLayout(layout)
    

    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()  # Показать окно при двойном клике на иконке

    def closeEvent(self, event):
        # Перехватываем событие закрытия окна
        event.ignore()  # Игнорируем это событие
        self.hide()  # Скрываем главное окно
        self.tray_icon.showMessage(
            "ДДЮТ Sound Control",
            "Приложение было свёрнуто в трей",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

class WorkerThread(QThread): # отдельный поток
    finished = pyqtSignal()
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)
        self.finished.emit()

class MyButton(QPushButton):
    def __init__(self, str, parent=None, clicked = None, state = False):
        super().__init__(str, parent)
        self.state = state
        self.setFixedHeight(22)
        self.setEnabled(self.state)
        self.setIcon(QIcon("data\\Icon\\custom.png"))
        if clicked:
            self.clicked.connect(clicked)

def show_input_dialog():
    dialog = myDialog.InputDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print('Close dialog!')
        