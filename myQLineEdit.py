from PyQt6.QtWidgets import QLineEdit
class newQLineEdit(QLineEdit):
    def __init__(self,obj,font,massege,transparency = 100,move_x = 0,move_y = 0,size_x = 50,size_y = 30):
        super().__init__(obj)
        transparency = transparency*255/100
        self.setStyleSheet("background-color: rgba(255, 255, 255, {});".format(transparency))
        self.resize(50,30)
        self.move(move_x,move_y)
        self.setFont(font)
        self.setPlaceholderText(massege)