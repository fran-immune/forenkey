
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
# Crear la ventana q muestra hash
hash_window = tk.Toplevel(window) 
hash_window.title("Hash")
hash_window.geometry("400x200")
# Crear el texto 
hash_text = tk.Text(hash_window)
hash_text.pack()
# Agregar un botón "Salir"
exit_button = tk.Button(hash_window, text="Salir", command=hash_window.destroy)
exit_button.pack(side="bottom")


# Ocultarla 
hash_window.withdraw()


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

        #img = cv2.imread(ruta_completa) 
        img = cv2.imread(ruta_completa, cv2.IMREAD_UNCHANGED)
        print(img)
        frame_array.append(img)

        video_out.write(frame_array[i])
        video_out.release() # no se si esto va aqui


        print("imprime valor de la variable img a ver si es none")
        print("captura de pantalla añadida al video")

        i += 1
        time.sleep(5)

# Crear una función para iniciar la aplicación
def start():
    global p1, p2
    print("La aplicación ha iniciado")
    
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
        #showHash()
        print("La aplicación ha terminado")
          # Mostrar la ventana del hash
        hash_window.deiconify()  

  # Insertar el hash
        hash_text.insert(tk.END, "Hash: " + hashcalculado)

  # Center window
        hash_window.eval('tk::PlaceWindow . center')

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



def encrypt_and_compress_file(input_file, output_file, password):
    with py7zr.SevenZipFile(output_file, mode='w', password=password) as z:
        z.write(input_file)
    return True

def encrypt_and_compress_folder(input_folder, output_file, password):
    with py7zr.SevenZipFile(output_file, 'w', password=password) as z:
        z.writeall(input_folder, '')
    return True

def encrypt_and_compress(input_path, output_path, password):
    if os.path.isfile(input_path):
        encrypt_and_compress_file(input_path, output_path, password)
    elif os.path.isdir(input_path):
        encrypt_and_compress_folder(input_path, output_path, password)
    else:
        raise ValueError(f'No se puede comprimir el archivo o carpeta {input_path}')
    
    return True

def calculate_sha256_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Leer el archivo por bloques para archivos grandes
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


import zipfile
import shutil

def comprimir_carpeta(ruta_carpeta, volume_name):
    # Obtener el puerto o DeviceID donde está insertado el pendrive
    puerto = ""
    for port in serial.tools.list_ports.comports():
        if volume_name in port.description:
            puerto = port.device
            break

    # Comprimir la carpeta
    nombre_archivo_zip = ruta_carpeta + ".zip"
    with zipfile.ZipFile(nombre_archivo_zip, "w", zipfile.ZIP_DEFLATED) as archivo_zip:
        for raiz, directorios, archivos in os.walk(ruta_carpeta):
            for archivo in archivos:
                archivo_completo = os.path.join(raiz, archivo)
                archivo_relacionado = os.path.relpath(archivo_completo, ruta_carpeta)
                archivo_zip.write(archivo_completo, archivo_relacionado)

    # Copiar el archivo zip al pendrive (si existe) y si tiene suficiente espacio de memoria disponible
    if puerto != "" and shutil.disk_usage(puerto).free > os.path.getsize(nombre_archivo_zip):
        shutil.copy(nombre_archivo_zip, puerto)
    else:
        print("No hay espacio suficiente para copiar el archivo zip al pendrive")



    # Calcular el sha256 de la carpeta
    hash_sha256 = hashlib.sha256()
    with open(nombre_archivo_zip, "rb") as archivo_zip:
        for bloque in iter(lambda: archivo_zip.read(4096), b""):
            hash_sha256.update(bloque)

    # Mostrar el resultado por pantalla
    print(f"El sha256 de la carpeta {ruta_carpeta} es {hash_sha256.hexdigest()}")

    # Eliminar el archivo zip temporal
    os.remove(nombre_archivo_zip)



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



now = pyautogui.datetime.datetime.now()
# 10 minutos = 600 segundos
# 30 segundos = 30 segundos
# 20 capturas de pantalla




