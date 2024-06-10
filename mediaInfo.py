import mySystem, myAIMP, myWinamp

class media_info:
    def __init__(self,Name = 'System'):
        self.progname = Name
        self.name = Name
        self.state = None
        self.title = None
        self.mute_state = None
        self.volume = None
        self.mySys = mySystem.Sysmedia()

    def data_update(self,name):
        self.progname = name
        self.volume = self.mySys.get_volume()
        self.mute_state = self.mySys.get_mute_state()

        if self.progname == 'Aimp':
            self.state = myAIMP.get_state()
            self.title = myAIMP.get_title()
        elif self.progname == 'Winamp':
            self.state = myWinamp.get_state()
            self.title = myWinamp.get_title()
        elif self.progname == 'System':
            self.state = self.mySys.get_state()
            self.title = self.mySys.get_title()
        self.dictionary_media = {'name':self.progname,'volume':self.volume,'state':self.state,'mute':self.mute_state,'title':self.title}
        return self.dictionary_media
        
