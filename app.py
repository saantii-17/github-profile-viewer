from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk  # Corrección aquí
from io import BytesIO

# Función para obtener el perfil de GitHub
def get_github_profile():
    username = username_entry.get()
    if username:
        try:
            # Solicitud de información del perfil
            response = requests.get(f"https://api.github.com/users/{username}")
            data = response.json()

            if response.status_code == 200:
                # Actualizar información del perfil
                avatar_url = data['avatar_url']
                username_label.config(text=data['login'])
                bio_label.config(text=data['bio'] if data['bio'] else 'No bio available')

                # Descargar la imagen del avatar
                avatar_response = requests.get(avatar_url)
                img_data = avatar_response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((100, 100))
                avatar_img = ImageTk.PhotoImage(img)  # Corrección aquí
                avatar_label.config(image=avatar_img)
                avatar_label.image = avatar_img  # Evitar que la imagen sea eliminada por el recolector de basura

                # Obtener los repos públicos
                repos_response = requests.get(f"https://api.github.com/users/{username}/repos")
                repos_data = repos_response.json()
                repos_list.delete(0, END)  # Limpiar lista de repos anteriores
                for repo in repos_data:
                    repos_list.insert(END, repo['name'])

            else:
                messagebox.showerror("Error", "Usuario no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recuperar el perfil: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de usuario")

# Configuración de la ventana principal
root = Tk()  # Corrección aquí
root.title("GitHub Profile Viewer")
root.geometry("400x550")
root.config(bg="white")

# Icono ventana principal
icon = PhotoImage(file='icon.png')
root.iconphoto(True, icon)

# Título
title_label = Label(root, text="GitHub Profile Viewer", font=("Arial", 18), bg="white")
title_label.pack(pady=10)

# Avatar
avatar_label = Label(root, bg="white")
avatar_label.pack(pady=10)

# Nombre de usuario
username_label = Label(root, text="Username", font=("Arial", 14, "bold"), bg="white")
username_label.pack()

# Biografía
bio_label = Label(root, text="Bio", font=("Arial", 12), fg="gray", wraplength=300, bg="white")
bio_label.pack(pady=5)

# Repositorios
repos_frame = Frame(root, bg="white")
repos_frame.pack(pady=10)

repos_title_label = Label(repos_frame, text="Public Repositories:", font=("Arial", 12), bg="white")
repos_title_label.pack()

repos_list = Listbox(repos_frame, width=40, height=10)
repos_list.pack()

# Cuadro de entrada para el nombre de usuario
username_entry = Entry(root, width=25, font=("Arial", 12))
username_entry.pack(pady=10)

# Botón de búsqueda
search_button = Button(root, text="Search", command=get_github_profile, font=("Arial", 12), bg="#4CAF50", fg="white")
search_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()