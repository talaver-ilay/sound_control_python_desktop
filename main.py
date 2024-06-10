from PyQt6.QtWidgets import QApplication
import sys
import QWindow
import myhid,hid
import time
import mediaInfo,myAIMP,myWinamp
vid = 1155
pid = 22352

def disc_device():
    device = myhid.init_device(vid, pid)
    device.connect_pack('disconnect')

def main():
    device = myhid.init_device(vid, pid) 
    myMedia = mediaInfo.media_info() # обект системных медиа данных
    device.progNameUpdate(window.prog_name_combo.currentText())
    window.prog_name_combo.currentTextChanged.connect(lambda:{device.progNameUpdate(window.prog_name_combo.currentText())})
    device.connect_pack('connect')
    
    while(True):
        # device.progNameUpdate(progName) # сообщить устройству какие настройки управления применить
        #progName = window.prog_name_combo.currentText()
        device.volume_pack(myMedia.get_volume()) # новое значение громкости
        device.mute_pack(myMedia.get_mute_state())
        if device.progName == 'Aimp':
            device.state_pack(myAIMP.get_aimp_state()) # состояние воспроизведения AIMP
            device.title_pack(myAIMP.get_aimp_title()) # название песни AIMP
        elif device.progName == 'Winamp':
            device.state_pack(myWinamp.get_state()) # состояние воспроизведения Winamp
            device.title_pack(myWinamp.get_title()) # название песни Winamp
        else:
            device.state_pack(myMedia.get_state()) # состояние воспроизведения системный
            device.title_pack(myMedia.get_title()) # название песни
        try:
            device.get_indexed_string(2) # проверка подключения устройства
        except hid.HIDException as ex:
            device = myhid.init_device(vid, pid) # перезапуск
            myMedia = mediaInfo.media_info()
        
        time.sleep(1/10)

app = QApplication(sys.argv)
app.setStyle("Fusion") # дизайн окна
window =  QWindow.MainWindow() # обект 
window.show() 
thread = QWindow.WorkerThread(main) # отдельный поток
thread.finished.connect(thread.deleteLater)
thread.start()
app.aboutToQuit.connect(lambda:{print("Application is about to quit"),disc_device()})
app.exec()






