import winamp
    
def get_state():
    try:
        mywinamp = winamp.Winamp()
        return mywinamp.getPlayingStatus()
    except RuntimeError as re: 
        return 'paused'
    except Exception as e:
        return 'paused'
    
def get_title():
    try:
        mywinamp = winamp.Winamp()
        winamp_title = mywinamp.getCurrentTrackName()
        return winamp_title
    except RuntimeError as re:
        return 'Not connected!'
    except Exception as e:
        return 'Not connected!'