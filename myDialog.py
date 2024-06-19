from PyQt6.QtWidgets import QDialog,QPushButton
from PyQt6.QtGui import QIcon,QPixmap,QPalette,QBrush,QFont,QColor
from PyQt6.QtCore import Qt
import myQLineEdit

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Custom keyboard layers')
        self.setFixedSize(600,472)
        icon = QIcon(QPixmap("data\\Icon\\icon.png")) # добавление иконки на титульную полоску
        self.setWindowIcon(icon)
        
        self.pixmap = QPixmap("data\\devimg.jpg")
        self.pixmap = self.pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        # Создаем палитру и устанавливаем фон
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(self.pixmap))
        self.setPalette(palette)

        font = QFont()
        font.setFamily("Arial")  # Задаем семейство шрифта
        font.setPointSize(12)    # Задаем размер шрифта
        
        yline = 105
        self.key1 = myQLineEdit.newQLineEdit(self,font,"Key1",50,110,105)
        self.key2 = myQLineEdit.newQLineEdit(self,font,"Key2",50,430,105)
        yline = 247
        xline = 152
        self.key3 = myQLineEdit.newQLineEdit(self,font,"Key3",50,xline,yline)
        self.key4 = myQLineEdit.newQLineEdit(self,font,"Key4",50,round(xline*1.78),yline)
        self.key5 = myQLineEdit.newQLineEdit(self,font,"Key5",50,round(xline*2.56),yline)
        yline = 340
        self.key6 = myQLineEdit.newQLineEdit(self,font,"Key6",50,xline,yline)
        self.key7 = myQLineEdit.newQLineEdit(self,font,"Key7",50,round(xline*1.78),yline)
        self.key8 = myQLineEdit.newQLineEdit(self,font,"Key8",50,round(xline*2.56),yline)

        self.new_name = myQLineEdit.newQLineEdit(self,font,"castom name..",50,xline-50,yline+100,200,25)

        self.button_ok = QPushButton('Добавить',self)
        self.button_exit = QPushButton('Назад',self)
        self.button_exit.clicked.connect(self.accept)
        self.button_ok.clicked.connect(lambda:print("Add new custom!"))
        self.button_ok.move(xline+160,yline+100)
        self.button_exit.move(xline+250,yline+100)