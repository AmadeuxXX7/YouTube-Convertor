import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from pytube import YouTube
import os
import shutil

root = tk.Tk()

root.title("Convertidor de Youtube a MP3 y MP4")

root.resizable(False, False)

icono = tk.PhotoImage(file="imgs/logo2.png")
root.iconphoto(True, icono)

root.geometry("700x550")

Logo = PhotoImage(file="imgs/logo.png")

Label(root, image=Logo).pack()

title = ("Helvetica", 16)
font = ("Helvetica", 13)

Titulo = Label(root, text="CONVERTIDOR DE YOUTUBE A MP3 & MP4", font=title)
Titulo.pack()

urlLabel = Label(root, text="Link:", font=font)
urlLabel.place(x=250, y=350)

urlEntry = Entry(root)
urlEntry.place(x=300, y=350)

save_path = ""

def get_video_title(url):
    try:
        video = YouTube(url)
        return video.title
    except Exception as e:
        print("Error al obtener el título del video:", str(e))
        return "video"

def browse_save_location():
    global save_path
    url = urlEntry.get()
    if not is_valid_youtube_url(url):
        show_error_message("URL no válida. Ingrese una URL de YouTube válida.")
        return
    video_title = get_video_title(url)
    initial_file = video_title + format.get()  # Nombre predeterminado basado en el título del video
    save_path = filedialog.asksaveasfilename(defaultextension=format.get(), filetypes=[(f"Archivos {format.get()}", f"*{format.get()}")], initialfile=initial_file)
    Convertir()

def Convertir():
    url = urlEntry.get()
    if not is_valid_youtube_url(url):
        show_error_message("URL no válida. Ingrese una URL de YouTube válida.")
        return
    video = YouTube(url)
    print('Title:', video.title)
    stream = None
    
    if format.get() == ".mp3":
        stream = video.streams.filter(only_audio=True).first()
    elif format.get() == ".mp4":
        stream = video.streams.filter(progressive=True, file_extension="mp4").first()
    
    if stream and save_path:
        print(f'Descargando como {format.get()}....')
        output_filename = os.path.splitext(os.path.basename(save_path))[0] + format.get()
        stream.download(filename=output_filename)
        shutil.move(output_filename, save_path)  # Mover el archivo a la ubicación seleccionada
        print('¡Listo!')
        urlEntry.delete(0, END)  # Borrar el contenido del Entry

formatLabel = Label(root, text="Selecciona el formato:", font=font)
formatLabel.place(x=260, y=395)

format = StringVar()
format.set(".mp3")

mp3rb = Radiobutton(root, text="MP3", variable=format, value=".mp3")
mp3rb.place(x=249, y=420)

mp4rb = Radiobutton(root, text="MP4", variable=format, value=".mp4")
mp4rb.place(x=249, y=450)

button = Button(root, text="Convertir", command=browse_save_location)
button.place(x=320, y=490)

def is_valid_youtube_url(url):
    import re
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=\w+"
    return bool(re.match(pattern, url))

def show_error_message(message):
    result = messagebox.showerror("Error", message)
    # Si el usuario hace clic en "OK", borra el contenido del Entry
    if result == "ok":
        urlEntry.delete(0, END)

root.mainloop()
