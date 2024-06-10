from PyQt6.QtWidgets import QApplication
import sys
import QWindow
import myhid,hid
import time
import mediaInfo

vid = 1155
pid = 22352
#
def main():
    device = myhid.init_device(vid, pid) 
    myMedia = mediaInfo.media_info() # обект системных медиа данных
    while(True):
        dictionary_media = myMedia.data_update(window.prog_name_combo.currentText())
        device.pack_update(dictionary_media)
        device.send_all()
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
app.aboutToQuit.connect(lambda:{print("Application is about to quit"), myhid.disc_device(vid,pid)})
app.exec()





