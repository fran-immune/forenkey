
# Importar el módulo tkinter
import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import time
import datetime
import py7zr
import pyWinhook, pythoncom, sys, logging
import pyautogui
import socket, cv2
import numpy as np
import pyautogui
#import root
from multiprocessing import Process, Queue

#crea directorios
screenshots_dir = os.path.join('C:\\users', os.getlogin(), '4rensics\\screenShotsCCR\\')
logs_dir = os.path.join('C:\\users', os.getlogin(), '4rensics\\logsCCR\\')
compress_dir= os.path.join('C:\\users', os.getlogin(), '4rensics\\compressCCR\\')
video_dir= os.path.join('C:\\users', os.getlogin(), '4rensics\\videoCCR\\')

#ruta = "F:/Cadena de custodia/Prueba"

#crea carpetas para guardar capturas de pantalla
def createFolder():
    try:
        os.mkdir('C:\\users\\%s\\4rensics\\screenShotsCCR' % os.getlogin())
        os.mkdir('C:\\users\\%s\\4rensics\\logsCCR' % os.getlogin())
        os.mkdir('C:\\users\\%s\\4rensics\\compressCCR' % os.getlogin())
        os.mkdir('C:\\users\\%s\\4rensics\\videoCCR' % os.getlogin())
    except OSError:
        pass
    else:
        print ("Successfully created the directories %s " % 'C:\\users\\%s\\screenShotsCCR' % os.getlogin())
    return


createFolder()

# Generar nombre para archivo log
log_filename = 'log_'+ pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt' 


# Ruta completa a archivo log
log_file = os.path.join(logs_dir, log_filename)


# captura eventos de teclado 
def OnKeyboardEvent(event):
    
    logging.basicConfig(filename=f'{log_file}', level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10,chr(event.Ascii))
    return True

# captura eventos de raton
def OnMouseEvent(event):
    #print('Click en ({}, {})'.format(event.Position[0], event.Position[1]))
    current_time = datetime.datetime.now()
    logging.basicConfig(filename=f'{log_file}', level=logging.DEBUG, format='%(message)s')
    log_message = f"Click en ({event.Position[0]}, {event.Position[1]}) en {current_time}"
    logging.log(10,log_message)
    
    return True

def keyandmouseLogger(queue):
    # crea un hook manager    
    hooks_manager = pyWinhook.HookManager()
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.MouseAllButtonsDown = OnMouseEvent
    hooks_manager.HookKeyboard()
    hooks_manager.HookMouse()
    pythoncom.PumpMessages()
    print("captura de raton y teclado  iniciado")
    return True

def screenshotdateAndTime(queue):
    i = 0
    fps = 5
    frame_array = []
    print("screenshotdateAndTime iniciado")
    screenshots_dir = os.path.join('C:\\users', os.getlogin(), 'screenShotsCCR')
    video_name = 'video_'+socket.gethostname()+'_'+pyautogui.datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.avi'
    ruta_completa_video = os.path.join(video_dir, video_name)
    video_out = cv2.VideoWriter(ruta_completa_video, 
                            cv2.VideoWriter_fourcc(*'MJPG'), 5, (1920,1080))
    print("La captura de pantalla ha iniciado")
    #nombre_video = socket.gethostname() + '_' + pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
    
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
        #video_out.release() # prueba para ver si se puede cerrar el video y abrirlo de nuevo


        print("imprime valor de la variable img a ver si es none")
        print("captura de pantalla añadida al video")

        i += 1
        time.sleep(5)
        return True

# Comprimir carpeta con capturas de pantalla, log y video
def compressFolder(url):
    print("Comprimiendo carpeta")
    # Generar nombre para archivo comprimido con nombre del host mas fecha y hora
    nombre_archivo = socket.gethostname() + '_' + pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.7z'
    ruta_completa = os.path.join(compress_dir, nombre_archivo)
    #print(ruta_completa)
    with py7zr.SevenZipFile(ruta_completa, 'w') as archive:
        archive.writeall(url, '4rensics')
    print("Carpeta comprimida")
    return ruta_completa

# Calcular hash 256 de archivo comprimido
def calculate_sha256_hash(url):
    print("Calculando hash")
    sha256_hash = hashlib.sha256()
    with open(url,"rb") as f:
        # Leer y actualizar hash en bloques de 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        print(sha256_hash.hexdigest())
        return sha256_hash.hexdigest()





# Crear una función para iniciar la aplicación
def start():
    global p1, p2
    print("La aplicación ha iniciado")


    try:
        p1.start()
        print("Iniciando proceso keyandmouseLogger")
        p2.start()
        print("Iniciando proceso screenshotdateAndTime")
        
    except Exception as e:
        print("Error iniciando procesos:", e)

# Crear una función para terminar la aplicación
def stop():
    global p1, p2
    if messagebox.askyesno("Terminar", "¿Seguro que quieres salir?"):
        

        
        print("La aplicación ha terminado")

        # termina proceso de captura de teclado y mouse
        if p1:
            p1.terminate()
        # termina proceso de captura de pantalla
        if p2:
            p2.terminate()

        # Esperar a que los procesos terminen
        p1.join()
        p2.join()
        print("La ruta de la carpeta comprimida es:")
        rutacomprimida =compressFolder(r"C:\Users\USER\4rensics\screenShotsCCR")
        print(rutacomprimida)
        hashcalculado = calculate_sha256_hash(rutacomprimida)
        print("El hash de la carpeta comprimida es:" + hashcalculado)
        showHashandRuta(hashcalculado,rutacomprimida)
        return


#agrega boton salir
def showHashandRuta(hashcalculado,ruta):


  # Crear el texto en la ventana principal
  hash_text = tk.Text(window)

  # Ubicar el texto en la ventana principal
  hash_text.pack(side="bottom")  

  # Insertar el texto con el hash
  hash_text.insert(tk.END, "El hash de la carpeta comprimida es: " + hashcalculado)
  hash_text.config(width=50, height=8, font=("Consolas", 12)  )
  hash_text.pack(side="top", pady=20) 
  hash_text.insert(tk.END, "\n\n")
  # Mostrar ruta de la carpeta que contiene el archivo comprimido
  hash_text.insert(tk.END, "la ruta de la carpeta comprimida es: " + ruta)


    # Crear botón de salir en la ventana principal
  exit_button = tk.Button(window, text="Salir", command=lambda: window.destroy())
  exit_button.pack(side="bottom")
  exit_button.pack(side="bottom", anchor="center", pady=(0, 20))
  return




if __name__ == "__main__":
    #p1 = Process(target=keyandmouseLogger)
    #p2 = Process(target=screenshotdateAndTime)

    # Crear la ventana principal de la interfaz
    window = tk.Tk()
    window.title("Cadena de custodia")
    window.geometry("600x500")

    queue = Queue()

    p1 = Process(target=keyandmouseLogger, args=(queue,))
    p2 = Process(target=screenshotdateAndTime, args=(queue,))

    # Crear un botón para iniciar la aplicación
    start_button = tk.Button(window, text="Iniciar", command=start)
    #sposicionar el botón en la ventana principal
    start_button.place(x=160, y=50)


    # Crear un botón para terminar la aplicación
    stop_button = tk.Button(window, text="Terminar", command=stop)
    #posicionar el botón en la ventana principal
    stop_button.place(x=290, y=50)
    #stop_button.pack()
    window.mainloop()

