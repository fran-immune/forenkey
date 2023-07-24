
# Importar el módulo tkinter
import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import time


#crea directorios
screenshots_dir = os.path.join('C:\\users', os.getlogin(), '4rensics\\screenShotsCCR\\')
logs_dir = os.path.join('C:\\users', os.getlogin(), '4rensics\\logsCCR\\')
compress_dir= os.path.join('C:\\users', os.getlogin(), '4rensics\\compressCCR\\')
video_dir= os.path.join('C:\\users', os.getlogin(), '4rensics\\videoCCR\\')

ruta = "F:/Cadena de custodia/Prueba"

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
# Crear la ventana principal
window = tk.Tk()
window.title("Cadena de custodia")
window.geometry("600x500")

# Crear una función para iniciar la aplicación
def start():
    print("La aplicación ha iniciado")

# Crear una función para terminar la aplicación
def stop():
    if messagebox.askyesno("Terminar", "¿Seguro que quieres salir?"):
        showHash2()
        print("La aplicación ha terminado")
        # esperar a que se cierre el popup de showHash antes de cerrar la ventana
       # window.after(6000, window.destroy)
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

#agrega boton salir
def showHash2():

  # Eliminar creación de popup
  #popup = tk.Toplevel(window) 
  
  # Crear el texto en la ventana principal
  hash_text = tk.Text(window)

  # Ubicar el texto en la ventana principal
  hash_text.pack(side="bottom")  

  # Insertar el texto con el hash
  hash_text.insert(tk.END, "El hash de la carpeta comprimida es: " + hashcalculado)
  hash_text.config(width=50, height=5, font=("Consolas", 12)  )
  hash_text.pack(side="top", pady=20) 
  hash_text.insert(tk.END, "\n\n")
  # Mostrar ruta de la carpeta que contiene el archivo comprimido
  hash_text.insert(tk.END, "la ruta de la carpeta comprimida es: " + ruta)


    # Crear botón de salir en la ventana principal
  exit_button = tk.Button(window, text="Salir", command=lambda: window.destroy())
  exit_button.pack(side="bottom")
  exit_button.pack(side="bottom", anchor="center", pady=(0, 20))

  
    




#popup = tk.Toplevel(window) yes
#popup.geometry("400x200+200+200") yes
#hash_text = tk.Text(popup) yes
#hash_text.pack(side="bottom") yes
#hash_text.insert(tk.END, "El hash de la carpeta comprimida es: " + hashcalculado)
# Iniciar el bucle principal de la ventana
window.mainloop()

