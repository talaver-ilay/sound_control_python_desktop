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
        self.progName_packet = None
        self.mute_packet = None
        self.connect_packet = None
        
        
    def progName_pack(self,Name = 'System'): # сообщить устройству какая программа используеться
        if Name != None and Name != '' and Name != 'Add custom..':
            dictionary_prog = {'System':0x00,'Winamp':0x01,'Aimp':0x02}
            pack = [0x03,0x04, dictionary_prog[Name]]
            if pack != self.progName_packet:
                self.progName_packet = pack
                return self.progName_packet
           
    
    def volume_pack(self,new_value): # отправить значение громкости в %
        new_pack = [0x03,0x01,new_value]
        if self.volume_packet != new_pack: # исключить повтор
            self.volume_packet = new_pack
            return self.volume_packet
      
    def state_pack(self,new_state):
        state_list = {'playing':[0x03,0x02,0x1],
                    'paused':[0x03,0x02,0x2],
                    'stopped':[0x03,0x02,0x03],
                    'else':[0x03,0x02,0x00]}
        if self.state_packet != state_list[new_state]:# исключить повтор
            self.state_packet = state_list[new_state]
            return self.state_packet
        
    def mute_pack(self, new_state):
        mute_list = {'mute':[0x03,0x05,0x01],'unmute':[0x03,0x05,0x00],} 
        if self.mute_packet != mute_list[new_state]:# исключить повтор
            self.mute_packet = mute_list[new_state]
            return self.mute_packet
        
    def connect_pack(self,state):
        connect_list = {'connect':0x01,'disconnect':0x00}
        self.connect_packet = [0x03,0x06,connect_list[state]]
        return self.connect_packet
    
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
            return self.title_packet

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
    
    def pack_update(self,dictionary_media):
        self.dictionary_packet = {'name':self.progName_pack(dictionary_media['name']),
                                  'volume':self.volume_pack(dictionary_media['volume']),
                                  'state':self.state_pack(dictionary_media['state']),
                                  'mute':self.mute_pack(dictionary_media['mute']),
                                  'title':self.title_pack(dictionary_media['title']) }
        return self.dictionary_packet
    
    def send_all(self):
        for pack in self.dictionary_packet.values():
            self.send_pack(pack)

def init_device(vid,pid,exit = False): # подключиться к устройству
    device = None
    while device is None:
        time.sleep(1)
        try:
            device = CustomHIDDevice(vid, pid)
            print(device.product)
            device.send_pack(device.connect_pack('connect'))
            return device
        except hid.HIDException as ex:
            print("None device...")
            time.sleep(1)
            if exit: return

def disc_device(vid,pid,exit = False):
    device = init_device(vid, pid, exit)
    if not exit:
        device.send_pack(device.connect_pack('disconnect'))
