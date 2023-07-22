
import pyWinhook, pythoncom, sys, logging
import os
import pyautogui
import moviepy
import pygetwindow as gw

import os
import pyautogui
import moviepy.editor
import hashlib
import socket
import datetime
import time
# Importar el módulo tkinter
import tkinter as tk
from tkinter import messagebox
from multiprocessing import Process

# Crear la ventana principal
window = tk.Tk()
window.title("Cadena de custodia")
window.geometry("600x500")


# nombre de fichero log + DDMMAAHHMMSS.txt


#crea una carpeta capturasdepantalla en la carpeta del usuario
def createFolder():
    try:
        os.mkdir('C:\\users\\%s\\screenShots' % os.getlogin())
    except OSError:
        print ("Creation of the directory %s failed" % 'C:\\users\\%s\\screenShots' % os.getlogin())
    else:
        print ("Successfully created the directory %s " % 'C:\\users\\%s\\screenShots' % os.getlogin())



createFolder()

# Generar nombre para archivo log
log_filename = 'log_'+ pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt' 

# Crear carpeta para screenshots
screenshots_dir = 'C:\\users\\%s\\screenshots' % os.getlogin()
os.mkdir(screenshots_dir)

# Ruta completa a archivo log
log_file = os.path.join(screenshots_dir, log_filename)

def OnKeyboardEvent(event):
    
    logging.basicConfig(filename=f'{log_file}', level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10,chr(event.Ascii))
    return True


def OnMouseEvent(event):
    #print('Click en ({}, {})'.format(event.Position[0], event.Position[1]))
    current_time = datetime.datetime.now()
    logging.basicConfig(filename=f'{log_file}', level=logging.DEBUG, format='%(message)s')
    log_message = f"Click en ({event.Position[0]}, {event.Position[1]}) en {current_time}"
    logging.log(10,log_message)
    
    return True

def keyandmouseLogger():
    # crea un hook manager    
    hooks_manager = pyWinhook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.MouseAllButtonsDown = OnMouseEvent
    hooks_manager.HookKeyboard()
    hooks_manager.HookMouse()
    pythoncom.PumpMessages()
    print("captura de raton y teclado  iniciado")
    return True


def screenshotdateAndTime():
    i = 0
    print("La captura de pantalla ha iniciado")
    while True:
        screenshot = pyautogui.screenshot()
        screenshot.save('C:\\users\\screenShots\\%s\\%s_%s.png' % (os.getlogin(), socket.gethostname(), datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
        i += 1
        time.sleep(15)

# Crear una función para iniciar la aplicación
def start():
    global p1, p2
    print("La aplicación ha iniciado")
    #keyandmouseLogger()
    
    p1 = Process(target=keyandmouseLogger)
    p2 = Process(target=screenshotdateAndTime)

    try:
        p1.start()
        print("Iniciando proceso 1")
        p2.start()
        print("Iniciando proceso 2")
    except Exception as e:
        print("Error iniciando procesos:", e)

# Crear una función para terminar la aplicación
def stop():
    global p1,p2
    if messagebox.askyesno("Terminar", "¿Seguro que quieres salir?"):
        showHash()
        print("La aplicación ha terminado")
        # termina proceso de captura de teclado y mouse
        p1.terminate()
        p1.join()
        p1 = None
        #Termina proceso de captura de capturas de pantalla
        p2.terminate()
        p2.join()
        p2 = None
        # esperar a que se cierre el popup de showHash antes de cerrar la ventana
        window.after(6000, window.destroy)
       # window.destroy()

# Crear un botón para iniciar la aplicación
start_button = tk.Button(window, text="Iniciar", command=start)
#start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
start_button.place(x=160, y=50)


# Crear un botón para terminar la aplicación
stop_button = tk.Button(window, text="Terminar", command=stop)
stop_button.place(x=290, y=50)
#stop_button.pack()


hashcalculado = "12345784784fjhjhf67890"

#hash_text = tk.Text(window)
#hash_text.pack(side="bottom")
#hash_text.insert(tk.END, "El hash de la carpeta comprimida es: " + hashcalculado)

def showHash():
    popup = tk.Toplevel(window)
    print("El hash de la carpeta comprimida es: " + hashcalculado)
    popup.geometry("400x200+200+200")
    hash_text = tk.Text(popup)
    hash_text.pack(side="bottom")
    hash_text.insert(tk.END, "El hash desde ShowHash la carpeta comprimida es: " + hashcalculado)
    popup.attributes('-topmost', True)
    window.iconbitmap("robot.ico")
        # Agregar un botón "Salir"
    exit_button = tk.Button(popup, text="Salir", command=popup.destroy)
    exit_button.pack(side="bottom")
    #popup.after(5000, popup.destroy)

window.mainloop()


# Añade una func que guarde capturas de pantallas cada 30 segundos durante 10 minutos y guardelas en la carpeta del usuario con el nombre en formato AAAA-MM-DD-HH-MM-SS.png, tambien debe almacenar cada minuto durante 10 minutos el nombre de la ventana activa en el mismo archivo log.txt y un video de 15 segundos de lo que se esta haciendo en el computador en el mismo directorio con el nombre en formato AAAA-MM-DD-HH-MM-SS.mp4, para capturar el video usa la libreria moviepy 1.0.3 y para capturar la ventana activa usa la libreria pygetwindow 0.0.9





#video.save('C:\\users\\%s\\%s.mp4' % (os.getlogin(), pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))


#Muy util
# crea una intergfaz grafica con dos botones iniciar y terminar, cuando se presione iniciar debe comenzar a capturar las capturas de pantalla y el video, cuando se presione terminar debe detener la captura de capturas de pantalla y el video, y debe mostrar un mensaje de que la captura de capturas de pantalla y el video ha terminado, y debe mostrar un boton que diga ver capturas de pantalla y video, cuando se presione debe abrir la carpeta del usuario donde se guardaron las capturas de pantalla y el video


    


# genera una funcion que genere un hash sha512 de un archivo de video que reciba como parametro y lo guarde en el archivo log.txt

def hashVideo(filename):
    filename = os.path.join('C:\\users', os.getlogin(), filename)
    with open(filename, 'rb') as f:
        bytes = f.read()
        readable_hash = hashlib.sha512(bytes).hexdigest();
        write(readable_hash)
        logging.log(10,readable_hash)
        
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

def hashCarpeta(filename):
    filename = os.path.join('C:\\users', os.getlogin(), filename)
    with open(filename, 'rb') as f:
        bytes = f.read()
        readable_hash = hashlib.sha512(bytes).hexdigest();
        logging.log(10,readable_hash)
        
    return True


now = pyautogui.datetime.datetime.now()
# 10 minutos = 600 segundos
# 30 segundos = 30 segundos
# 20 capturas de pantalla




