import os 
import tkinter as tk 
from tkinter import ttk
import datetime

ventana = tk.Tk()
ventana.title('Tareas')
ventana.geometry('600x400')
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)
menu_archivo = tk.Menu(barra_menu)

# Configurar la cuadrícula para que los frames se expandan
ventana.grid_rowconfigure(0, weight=0)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)

# Crear el Frame para la primera columna (Materias)
frame_left = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1)
frame_left.grid(row=1, column=0, sticky="nsew")

# Crear el Frame para la segunda columna (Lista de Tareas)
frame_right = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1)
frame_right.grid(row=1, column=1, sticky="nsew")

# Crear el Frame para la fecha y hora
frame_top = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1)
frame_top.grid(row=0, column=0, columnspan=2, sticky="ew")

# Agregar un Label para la fecha y hora en el frame_top
label_datetime = ttk.Label(frame_top, text="", font=("Helvetica", 12))
label_datetime.pack()

def update_datetime():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_datetime.config(text=now)
    ventana.after(1000, update_datetime)

# Iniciar la actualización de la fecha y hora
update_datetime()

# Agregar un Label y Listbox en la primera columna
label_materias = ttk.Label(frame_left, text="Materias")
label_materias.pack(pady=5, anchor="n")

listbox_materias = tk.Listbox(frame_left, height=15)
listbox_materias.pack(pady=5, fill="both", expand=True)

# Agregar botones de acción en la primera columna
button_agregar_materia = ttk.Button(frame_left, text="Agregar Materia")
button_agregar_materia.pack(side="left", padx=5, pady=5)

button_eliminar_materia = ttk.Button(frame_left, text="Eliminar Materia")
button_eliminar_materia.pack(side="right", padx=5, pady=5)

# Agregar un Label y Listbox en la segunda columna
label_tareas = ttk.Label(frame_right, text="Tareas Pendientes")
label_tareas.pack(pady=5, anchor="n")

listbox_tareas = tk.Listbox(frame_right, height=15)
listbox_tareas.pack(pady=5, fill="both", expand=True)


# Agregar botones de acción en la segunda columna
button_agregar_tarea = ttk.Button(frame_right, text="Agregar Tarea")
button_agregar_tarea.pack(side="left", padx=5, pady=5)

button_eliminar_tarea = ttk.Button(frame_right, text="Eliminar Tarea")
button_eliminar_tarea.pack(side="right", padx=5, pady=5)



# Opciones de archivo
barra_menu.add_cascade(label = 'Archivo', menu=menu_archivo)
submenu = tk.Menu(menu_archivo)
menu_archivo.add_cascade(label = 'Nuevo')
menu_archivo.add_cascade(label = 'Guardar')

# Opciones de Edición
menu_editar = tk.Menu(barra_menu)
barra_menu.add_cascade(label = 'Editar', menu=menu_editar)
submenu = tk.Menu(menu_editar)
menu_editar.add_cascade(label = 'Deshacer')
menu_editar.add_cascade(label = 'Rehacer')
menu_editar.add_cascade(label = 'Preferencias')

# Opciones de Visualizacion
menu_ver = tk.Menu(barra_menu)
barra_menu.add_cascade(label = 'Ver', menu=menu_ver)
submenu = tk.Menu(menu_ver)
menu_ver.add_cascade(label = 'Diario')
menu_ver.add_cascade(label = 'Semanal')
menu_ver.add_cascade(label = 'Mensual')


# Agregar tareas






ventana.mainloop()


