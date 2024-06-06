import asyncio
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
import asyncio

def audio_device():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return  interface.QueryInterface(IAudioEndpointVolume)

class media_info:
    def __init__(self,audio = audio_device()):
        self.volume_interface = audio
        self.current_session = asyncio.run(open_sessions())
        
    def get_volume(self):    # значение системной громкости
        return round(self.volume_interface.GetMasterVolumeLevelScalar()*100)
    
    def get_state(self): # получить доступ к состоянию воспроизведения
        if self.current_session != None:
            state = self.current_session.get_playback_info().playback_status
            state_={4:'playing',5:'paused',0:'paused'}
            return state_[state]
        else:
            self.current_session = asyncio.run(open_sessions())
            return 'paused'
        
    def get_mute_state(self): # получить доступ к состоянию воспроизведения
        mute_state = self.volume_interface.GetMute()
        if mute_state:           
            return 'mute'
        else: return 'unmute' 
    
    async def get_sessions_title(self): # название текущей песни
        if self.current_session != None:
            try:
                info = await self.current_session.try_get_media_properties_async()
                info_dict = {attr: getattr(info, attr) for attr in dir(info) if not attr.startswith('_')}
                return info_dict.get('title')
            except OSError:
                self.current_session = None
                return 'Not connected!'        
        else:
            try:
                self.current_session = asyncio.run(open_sessions())
            except RuntimeError:
                return 'Not connected!'
    def get_title(self):
        return asyncio.run(self.get_sessions_title())


async def open_sessions(): # получить доступ к системному медиа async
        try:
            sessions = await MediaManager.request_async()
            return sessions.get_current_session()
        except Exception as e:
            print(f'Error: {str(e)}')  