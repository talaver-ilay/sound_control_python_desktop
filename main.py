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

def send_media(device,state,title):
    device.state_pack(state) 
    device.title_pack(title)


def main():
    device = myhid.init_device(vid, pid) 
    myMedia = mediaInfo.media_info() # обект системных медиа данных
    
    while(True):
        device.progNameUpdate(window.prog_name_combo.currentText()) # сообщить устройству какие настройки управления применит

        device.volume_pack(myMedia.get_volume()) # новое значение громкости
        device.mute_pack(myMedia.get_mute_state())

        if device.progName == 'Aimp':
            send_media(device,myAIMP.get_state(),myAIMP.get_title())
        elif device.progName == 'Winamp':
            send_media(device, myWinamp.get_state(), myWinamp.get_title())
        else:
            send_media(device, myMedia.get_state(), myMedia.get_title())
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





