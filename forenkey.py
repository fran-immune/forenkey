
import pyWinhook, pythoncom, sys, logging
import os
import pyautogui
import moviepy
import pygetwindow as gw
import numpy
import os
import pyautogui
import moviepy.editor
import hashlib
import socket
import datetime
import time
import tkinter as tk
from tkinter import messagebox
from multiprocessing import Process
import cv2

#crea directorio para guardar capturas de pantalla
screenshots_dir = os.path.join('C:\\users', os.getlogin(), 'screenShotsCCR\\')
logs_dir = os.path.join('C:\\users', os.getlogin(), 'logsCCR\\')
# Crear la ventana principal
window = tk.Tk()
window.title("Cadena de custodia")
window.geometry("600x500")



# nombre de fichero log + DDMMAAHHMMSS.txt


#crea una carpeta capturasdepantalla en la carpeta del usuario

def createFolder():
    try:
        os.mkdir('C:\\users\\%s\\screenShotsCCR' % os.getlogin())
        os.mkdir('C:\\users\\%s\\logsCCR' % os.getlogin())
    except OSError:
        print ("Creation of the directory %s failed" % 'C:\\users\\%s\\screenShotsCCR' % os.getlogin())
    else:
        print ("Successfully created the directory %s " % 'C:\\users\\%s\\screenShotsCCR' % os.getlogin())



createFolder()


# Generar nombre para archivo log
log_filename = 'log_'+ pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt' 


# Ruta completa a archivo log
log_file = os.path.join(logs_dir, log_filename)

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

# construir una funcion que reciba como parametro el nombre de una captura de pantalla, y un directorio, y haga un video añadiendo cada captura
# de pantalla al video, y lo guarde en el directorio con el nombre en formato AAAA-MM-DD-HH-MM-SS.mp4

video_out = cv2.VideoWriter('video_'+socket.gethostname()+'_'+pyautogui.datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.avi', 
                            cv2.VideoWriter_fourcc(*'MJPG'), 5, (1920,1080))
def videoMaker(filename, directory):
    import cv2
    import os
    from os.path import isfile, join
    import re
    import numpy as np
    import glob
    import datetime
    import time
    from datetime import datetime
    from datetime import timedelta
    from datetime import date
    from datetime import time
    from datetime import timezone
    from datetime import tzinfo
    from datetime import timedelta
    from datetime import datetime
    print("videoMaker iniciado")
    # Directorio donde se encuentran las capturas de pantalla
    pathIn= directory
    # Directorio donde se guardara el video
    pathOut = directory
    # Nombre del video
    fps = 5
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    # Ordenar los archivos por fecha de creacion
    files.sort(key=lambda x: os.path.getmtime(join(pathIn, x)))

    for i in range(len(files)):
        filename=pathIn +files[i]
        print(filename)
        # leer la imagen
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        # insertar la imagen en el array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut + filename + '.avi',cv2.VideoWriter_fourcc(*'MJPG'), fps, size)
    for i in range(len(frame_array)):
        # escribir el video
        out.write(frame_array[i])
        out.release()
    print("videoMaker terminado")
    return True



#videoMaker('videoPru', screenshots_dir)

def screenshotdateAndTime():
    i = 0
    fps = 5
    frame_array = []
    print("screenshotdateAndTime iniciado")
    screenshots_dir = os.path.join('C:\\users', os.getlogin(), 'screenShotsCCR')
    video_out = cv2.VideoWriter('video_'+socket.gethostname()+'_'+pyautogui.datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.avi', 
                            cv2.VideoWriter_fourcc(*'MJPG'), 5, (1920,1080))
    print("La captura de pantalla ha iniciado")
    nombre_video = socket.gethostname() + '_' + pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
    ruta_completa_video = os.path.join(screenshots_dir, nombre_video)
    while True: 
        # Generar nombre para captura de pantalla con nombre del host mas fecha y hora
        nombre_archivo = socket.gethostname() + '_' + pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
       
        ruta_completa = os.path.join(screenshots_dir, nombre_archivo)
        screenshot = pyautogui.screenshot()
        screenshot.save(ruta_completa)

        img = cv2.imread(ruta_completa) #pudiera ser nombre archivo
        print(img)
        frame_array.append(img)

        video_out.write(frame_array[i])
        print("imprime valor de la variable img a ver si es none")
        print("captura de pantalla añadida al video")

        i += 1
        time.sleep(5)

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
    global p1,p2, video_out
    if messagebox.askyesno("Terminar", "¿Seguro que quieres salir?"):
        video_out.release()
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
        #UnhookKeyboard() 
        #UnhookMouse()
        print("capturas detenidasAntesdestroy")
        window.after(6000, window.destroy)
        print("capturas detenidasAfterdestroy")
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




