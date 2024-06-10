import hid
import mychar, time
'''
'volume' :[0x03, 0x01, 0-100%]
'state':
    'playing':[0x03, 0x02, 0x01]
    'paused' :[0x03, 0x02, 0x02]
    'stopped':[0x03, 0x02, 0x00] or [0x03, 0x02, 0x03]
    'else'   :[0x03, 0x02, 0x00]
'title'  :[0x03, 0x03, ".."]
'program':
    'System' :[0x03, 0x04, 0x00]
    'Winamp' :[0x03, 0x04, 0x01]
    'Aimp'   :[0x03, 0x04, 0x02] 
'''
class CustomHIDDevice(hid.Device):
    def __init__(self, vid, pid):
        super().__init__(vid, pid)
        self.device = self
        self.vid = vid
        self.pid = pid
        self.state_packet = []
        self.volume_packet = []
        self.title_packet = []
        self.progName = None
        self.mute = None
        
    def progNameUpdate(self,Name = 'System'): # сообщить устройству какая программа используеться
        print(Name)
        if Name != None and Name != '':
            if Name != self.progName:
                AllName = {'System':0x00,'Winamp':0x01,'Aimp':0x02}
                pack = [0x03,0x04,AllName[Name]]
                self.send_pack(pack)
                self.progName = Name
                
    def send_pack(self,pack): # отправка посылка
        if pack is not None:
            try:
                print(pack)
                self.device.write(bytes(pack))
                return 0
            except hid.HIDException as ex:
                self.device = init_device(self.vid, self.pid)
                print("Reboot")
                return 1
    
    def volume_pack(self,new_value): # отправить значение громкости в %
        new_pack = [0x03,0x01,new_value]
        if self.volume_packet != new_pack: # исключить повтор
            self.volume_packet = new_pack
            return self.send_pack(self.volume_packet)
    
    def state_pack(self,new_state):
        state_list = {'playing':[0x03,0x02,0x1],
                    'paused':[0x03,0x02,0x2],
                    'stopped':[0x03,0x02,0x03],
                    'else':[0x03,0x02,0x00]}
        if self.state_packet != state_list[new_state]:# исключить повтор
            self.state_packet = state_list[new_state]
            return self.send_pack(self.state_packet)
    def mute_pack(self,new_state):
        mute_list = {'mute':[0x03,0x05,0x01],
                    'unmute':[0x03,0x05,0x00],}
        
        if self.mute != mute_list[new_state]:# исключить повтор
            self.mute = mute_list[new_state]
            return self.send_pack(self.mute)
        
    def connect_pack(self,state):
        connect_list = {'connect':0x01,'disconnect':0x00}
        pack = [0x03,0x06,connect_list[state]]
        return self.send_pack(pack)
    
    def title_pack(self,new_title):
        new_pack = [0x03,0x03]
        for i in [' ','>','>']:
            new_pack.append(i)
        for char_title in new_title: 
            new_pack.append(char_title)
        new_pack.append(' ')
        for index,value in enumerate(new_pack[2:]):
            try:
                new_pack[index+2] = mychar.ru[value]   # ищем символ в таблице mychar
            except:
                new_pack[index+2] = mychar.ru[' ']     # если нет символа в таблице ставим пробел
        if self.title_packet != new_pack:              # исключить повтор
            self.title_packet = new_pack
            return self.send_pack(self.title_packet)
        
def init_device(vid,pid): # подключиться к устройству
    device = None
    while device is None:
        time.sleep(1)
        try:
            device = CustomHIDDevice(vid, pid)
            print(device.product)
            return device
        except hid.HIDException as ex:
            print("None device...")
            time.sleep(1)
