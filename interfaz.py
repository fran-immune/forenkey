
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
import shutil
from multiprocessing import Process, Queue
import shutil
import wmi
import logging

volume_serial = "76FBBFE3" #  número de serie USB

ROOT = 'C:\\users' #ruta raiz para crear directorios

user= os.getlogin()

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Obtener loggers
global keyboard_logger 
global mouse_logger

#funcion que recibe como parametro el SerialNumber de un USB y retorna el puerto donde está conectado
def get_USB_port(volume_serial):
  c = wmi.WMI()
  for disk in c.Win32_DiskDrive():
    for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
      for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
        if logical_disk.VolumeSerialNumber == volume_serial:
          port = logical_disk.DeviceID
          return port.split("\\")[-1]

#obtener puerto del USB
port = get_USB_port(volume_serial)
host = socket.gethostname()
ROOT_USB = os.path.join(port,'//')
print("el puerto del USB es " + port)

print("root_usb es " + ROOT_USB)

#directorios




# Generar nombre para archivo log
log_keyboard_file = 'log_keyboard'+ pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt' 
log_mouse_file = 'log_mouse'+ pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.txt' 


log_keyboard_ruta = os.path.join(ROOT_USB,"/4ensics/keyboardCCR/", log_keyboard_file)
log_mouse_ruta = os.path.join(ROOT_USB,"/4ensics/logs_mouseCCR/", log_mouse_file)  
print("laruta del log del mouse es: " + log_mouse_ruta)
compress_dir= os.path.join(ROOT_USB, '/4ensics/compressCCR/')
video_dir= os.path.join(ROOT_USB, '/4ensics/videoCCR/')
print("la ruta del video es: " + video_dir)

keyboard_logger = logging.getLogger('keyboard')
keyboard_logger.setLevel(logging.DEBUG)
keyboard_logger.addHandler(logging.FileHandler(log_keyboard_ruta, mode='w', encoding='utf-8'))

mouse_logger = logging.getLogger('mouse')
mouse_logger.setLevel(logging.DEBUG) 
mouse_logger.addHandler(logging.FileHandler(log_mouse_ruta))




#crea carpetas para guardar capturas de pantalla
def create_folder():
    try:
        os.mkdir('H:/4ensics/logs_mouseCCR')
        os.mkdir('H:/4ensics/videoCCR' )
        os.mkdir('H:/4ensics/keyboardCCR')
        os.mkdir('H:/4ensics/compressCCR')
        
        
    except OSError:
        pass
    else:
        print ("Successfully created the directories en el puerto USB")
    


create_folder()

print("el puerto del USB es " + port)



# captura eventos de teclado 
def onkeyboard_event(event):
    current_time = datetime.datetime.now()
    #chr(event.Ascii)
    log_messageK= f"{user} : {host} :{current_time} {event.Key} Ascii: {event.Ascii}  "
    keyboard_logger.log(10, log_messageK)
    return True



# captura eventos de raton
def onmouse_event(event):
    current_time = datetime.datetime.now()
    
    log_messageM = f"{user} : {host} : {current_time} Click en ({event.Position[0]}, {event.Position[1]})"
    mouse_logger.log(10, log_messageM)
    
    return True

def keyandmouse_logger(queue):
    # crea un hook manager    
    hooks_manager = pyWinhook.HookManager()
    hooks_manager.KeyDown = onkeyboard_event
    hooks_manager.MouseAllButtonsDown = onmouse_event
    hooks_manager.HookKeyboard()
    hooks_manager.HookMouse()
    pythoncom.PumpMessages()
    return True

def screenshot_date_and_time(queue):
    i = 0
    fps = 5
    frame_array = []
    print("screenshotdateAndTime iniciado")
    #screenshots_dir = os.path.join('C:\\users', os.getlogin(), '4rensics\\screenShotsCCR')
    video_name = 'video_'+host+'_'+pyautogui.datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.avi'
    ruta_completa_video = os.path.join(video_dir, video_name)

    #Configuración de VideoWriter
    video_out = cv2.VideoWriter(ruta_completa_video, cv2.VideoWriter_fourcc(*'MJPG'), fps, (1920,1080))
    print("La captura de pantalla ha iniciado")
    print("la ruta completa del video es: " + ruta_completa_video)
    
    while True:  # finalizar = False
        # Generar nombre para captura de pantalla con nombre del host mas fecha y hora
        nombre_screenshot = socket.gethostname() + '_' + pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.png'
       
        #ruta_completa = os.path.join(screenshots_dir, nombre_screenshot)
        ruta_completa = os.path.join('H:\\4ensics\\screenShotsCCR', nombre_screenshot)
        screenshot = pyautogui.screenshot()
        screenshot.save(ruta_completa)
        print("la ruta de la captura de pantalla es: " + ruta_completa)

        #agrega captura de pantalla al video, carga la imagen en Formato BGR
        img = cv2.imread(ruta_completa, cv2.IMREAD_UNCHANGED)
        frame_array.append(img)
        video_out.write(frame_array[i])
        
        print("imprime valor de la variable img a ver si es none")
        print("captura de pantalla añadida al video")

        i += 1
        time.sleep(5)
    #
    # 
    # 
    # video_out.release() # prueba para ver si se puede cerrar el video y abrirlo de nuevo
        

# Comprimir carpeta con capturas de pantalla, log y video
def compress_folder(url,password):
    print("Comprimiendo carpeta")
    print("la url de la carpeta a comprimir es: " + url)
    # Generar nombre para archivo comprimido con nombre del host mas fecha y hora
    nombre_archivo = socket.gethostname() + '_' + pyautogui.datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.7z'
    ruta_completa = os.path.join(compress_dir, nombre_archivo)
    print("la ruta de la carpeta comprimida es: " + ruta_completa)
    with py7zr.SevenZipFile(ruta_completa, 'w',password=password) as archive:
        archive.writeall(url, 'compressCCR')
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
    status_label.config(text="Capturas iniciadas") 
    start_button["state"] = "disabled"
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
        start_button["state"] = "normal"
        status_label.config(text="")
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
        rutacomprimida =compress_folder("H:/4ensics/videoCCR", "1234")
        
        print(rutacomprimida)
        hashcalculado = calculate_sha256_hash(rutacomprimida)
        print("El hash de la carpeta comprimida es:" + hashcalculado)
        
        showHashandRuta(hashcalculado,rutacomprimida)
        #encrypt_folder(rutacomprimida, "1234")

# Crear una función para mostrar el hash y la ruta de la carpeta comprimida
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


#main
if __name__ == "__main__":

    # Crear la ventana principal de la interfaz
    window = tk.Tk()
    window.title("Cadena de custodia")
    window.geometry("600x500")

    disk_usage = shutil.disk_usage(ROOT_USB)
    espacio_libre = disk_usage.free

    # Verificar que haya suficiente espacio libre en el USB
    if espacio_libre < 1024:
    
        lbl_error = tk.Label(window, text="No hay suficiente espacio libre")
        lbl_error.pack()
    
        btn_ok = tk.Button(window, text="OK", command=window.destroy)
        btn_ok.pack()
        sys.exit()
    
    #Indiador de estado
    status_label = tk.Label(window, text="")
    status_label.pack(side="bottom")

    queue = Queue()



    p1 = Process(target=keyandmouse_logger, args=(queue,))
    p2 = Process(target=screenshot_date_and_time, args=(queue,))

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

