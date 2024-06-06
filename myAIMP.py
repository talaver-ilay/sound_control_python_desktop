import pyaimp

def get_aimp_title():
    try:
        client = pyaimp.Client()
        aimp_title = client.get_current_track_info()
        aimp_title = remove_before_last_backslash(aimp_title['filename'])# в нвзвании песни убрать путь
        return aimp_title
    except RuntimeError as re: 
        return 'Not connected!'
    except Exception as e:
        return 'Not connected!'

def get_aimp_state():
    try:
        client = pyaimp.Client()
        state = {'PlayBackState.Paused':'paused', # привести к стандартному виду
                'PlayBackState.Stopped':'stopped',
                'PlayBackState.Playing':'playing'}
        return state[str(client.get_playback_state())]
    except RuntimeError as re: 
        return 'paused'
    except Exception as e:
        return 'paused'

def remove_before_last_backslash(string): # в нвзвании песни убрать путь 
    if '\\' not in string:
        return string
    else:
        return string.rsplit('\\', 1)[-1]   
        

