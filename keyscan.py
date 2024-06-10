from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.esc:
        print('Прослушивание клавиатуры завершено')
        return False  # Завершает прослушивание
def keyboard_scan():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()