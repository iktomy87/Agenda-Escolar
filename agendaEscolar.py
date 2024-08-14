import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import datetime
import json
import os

# Bandera para detectar cambios no guardados
cambios_no_guardados = False

# Crear la ventana principal
ventana = tk.Tk()
ventana.title('Tareas')
ventana.geometry('600x400')

# Crear la barra de menú
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)
menu_archivo = tk.Menu(barra_menu)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Nuevo", command=lambda: nuevo_archivo())
menu_archivo.add_command(label="Guardar", command=lambda: guardar_datos())
menu_archivo.add_command(label="Cargar", command=lambda: cargar_datos())
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=ventana.quit)

# Configurar la cuadrícula para que los frames se expandan
ventana.grid_rowconfigure(0, weight=0)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)

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

# Crear el Frame para la primera columna (Materias)
frame_left = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1)
frame_left.grid(row=1, column=0, sticky="nsew")

# Crear el Frame para la segunda columna (Lista de Tareas)
frame_right = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1)
frame_right.grid(row=1, column=1, sticky="nsew")

# Agregar un Label y Listbox en la primera columna
label_materias = ttk.Label(frame_left, text="Materias")
label_materias.pack(pady=5, anchor="n")

lista_materias = tk.Listbox(frame_left, height=15)
lista_materias.pack(pady=5, fill="both", expand=True)

# Lista para almacenar las materias
materias = []

def abrir_ventana_agregar_materias():
    ventana_materia = tk.Toplevel(ventana)
    ventana_materia.title("Agregar materia")
    ventana_materia.geometry("210x200")
    ventana_materia.resizable(width=0, height=0)

    label_nombre_materia = ttk.Label(ventana_materia, text="Nombre de la Materia:")
    label_nombre_materia.pack(padx=10, pady=5)

    entrada_nombre_materia = ttk.Entry(ventana_materia)
    entrada_nombre_materia.pack(padx=10, pady=5)

    def agregar_materia_desde_emergente():
        nombre_materia = entrada_nombre_materia.get()
        materias.append(nombre_materia)
        actualizar_listbox_materias()
        global cambios_no_guardados
        cambios_no_guardados = True
        ventana_materia.destroy()

    button_agregar = ttk.Button(ventana_materia, text="Agregar materia", command=agregar_materia_desde_emergente)
    button_agregar.pack(pady=10)

def actualizar_listbox_materias():
    lista_materias.delete(0, tk.END)
    for materia in materias:
        lista_materias.insert(tk.END, materia)

button_agregar_materia = ttk.Button(frame_left, text="Agregar Materia", command=abrir_ventana_agregar_materias)
button_agregar_materia.pack(side="left", padx=5, pady=5)

def eliminar_materia():
    seleccion = lista_materias.curselection()
    if seleccion:
        del materias[seleccion[0]]
        actualizar_listbox_materias()
        global cambios_no_guardados
        cambios_no_guardados = True

button_eliminar_materia = ttk.Button(frame_left, text="Eliminar Materia", command=eliminar_materia)
button_eliminar_materia.pack(side="right", padx=5, pady=5)

# Agregar un Label y Listbox en la segunda columna
label_tareas = ttk.Label(frame_right, text="Tareas Pendientes")
label_tareas.pack(pady=5, anchor="n")

lista_tareas = tk.Listbox(frame_right, height=15)
lista_tareas.pack(pady=5, fill="both", expand=True)

tareas = []

def abrir_ventana_agregar_tarea():
    ventana_tarea = tk.Toplevel(ventana)
    ventana_tarea.title("Agregar Tarea")
    ventana_tarea.geometry("210x200")
    ventana_tarea.resizable(width=0, height=0)

    label_nombre_tarea = ttk.Label(ventana_tarea, text="Nombre de la Tarea:")
    label_nombre_tarea.pack(padx=10, pady=5)

    entrada_nombre_tarea = ttk.Entry(ventana_tarea)
    entrada_nombre_tarea.pack(padx=10, pady=5)

    label_fecha_limite = ttk.Label(ventana_tarea, text="Fecha Límite:")
    label_fecha_limite.pack(padx=10, pady=5)

    entrada_fecha_limite = DateEntry(ventana_tarea, date_pattern='yyyy-mm-dd')
    entrada_fecha_limite.pack(padx=10, pady=5)

    label_hora_limite = ttk.Label(ventana_tarea, text="Hora Límite (HH:MM):")
    label_hora_limite.pack(padx=10, pady=5)

    spinbox_hora = ttk.Spinbox(ventana_tarea, from_=0, to=23, width=5, format="%02.0f")
    spinbox_hora.pack(side="left", padx=(10, 2), pady=5)

    spinbox_minuto = ttk.Spinbox(ventana_tarea, from_=0, to=59, width=5, format="%02.0f")
    spinbox_minuto.pack(side="left", padx=(2, 10), pady=5)

    def agregar_tarea_desde_emergente():
        nombre_tarea = entrada_nombre_tarea.get()
        fecha_limite = entrada_fecha_limite.get_date()
        hora_limite = int(spinbox_hora.get())
        minuto_limite = int(spinbox_minuto.get())
        
        if nombre_tarea and fecha_limite:
            fecha_hora_limite = datetime.datetime.combine(fecha_limite, datetime.time(hora_limite, minuto_limite))
            tareas.append((nombre_tarea, fecha_hora_limite))
            tareas.sort(key=lambda x: x[1])
            actualizar_listbox_tarea()
            global cambios_no_guardados
            cambios_no_guardados = True
            ventana_tarea.destroy()

    button_agregar = ttk.Button(ventana_tarea, text="Agregar Tarea", command=agregar_tarea_desde_emergente)
    button_agregar.pack(pady=10)

def actualizar_listbox_tarea():
    lista_tareas.delete(0, tk.END)
    for tarea, fecha in tareas:
        lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})")

button_agregar_tarea = ttk.Button(frame_right, text="Agregar Tarea", command=abrir_ventana_agregar_tarea)
button_agregar_tarea.pack(side="left", padx=5, pady=5)

def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        del tareas[seleccion[0]]
        actualizar_listbox_tarea()
        global cambios_no_guardados
        cambios_no_guardados = True

button_eliminar_tarea = ttk.Button(frame_right, text="Eliminar Tarea", command=eliminar_tarea)
button_eliminar_tarea.pack(side="right", padx=5, pady=5)

def guardar_datos():
    archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if archivo:
        datos = {"tareas": [(tarea, fecha.strftime('%Y-%m-%d %H:%M')) for tarea, fecha in tareas], "materias": materias}
        with open(archivo, "w") as file:
            json.dump(datos, file)
        global cambios_no_guardados
        cambios_no_guardados = False

def cargar_datos():
    archivo = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if archivo:
        with open(archivo, "r") as file:
            datos = json.load(file)
            global tareas, materias
            tareas = [(tarea, datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M')) for tarea, fecha in datos["tareas"]]
            materias = datos["materias"]
            actualizar_listbox_tarea()
            actualizar_listbox_materias()

def nuevo_archivo():
    global cambios_no_guardados
    if cambios_no_guardados:
        respuesta = messagebox.askyesnocancel("Guardar cambios", "Hay cambios sin guardar. ¿Deseas guardarlos antes de crear un nuevo archivo?")
        if respuesta is None:
            return
        elif respuesta:
            guardar_datos()
    global tareas, materias
    tareas = []
    materias = []
    actualizar_listbox_tarea()
    actualizar_listbox_materias()
    cambios_no_guardados = False

ventana.mainloop()
