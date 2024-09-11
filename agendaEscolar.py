import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import tkinter.ttk as ttk
import tkinter.font as tkFont
import datetime
import json
import os

# Bandera para detectar cambios no guardados
cambios_no_guardados = False

# Crear la ventana principal
ventana = tk.Tk()
ventana.title('Agenda Escolar')
ventana.geometry('600x400')
font = tkFont.Font(family="Helvetica", size=12, weight="bold")
style = ttk.Style()
style.configure("hola.TFrame", background='CadetBlue3')

# Crear la barra de menú
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

menu_principal = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Menu", menu=menu_principal)

# Crear el submenú "Archivo"
menu_archivo = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Archivo", menu=menu_archivo)


menu_ver = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Ver", menu=menu_ver)

#Archivo
menu_archivo.add_command(label="Nuevo", command=lambda: nuevo_archivo())
menu_archivo.add_command(label="Guardar", command=lambda: guardar_datos())
menu_archivo.add_command(label="Cargar", command=lambda: cargar_datos())

#Ver
menu_ver.add_command(label="Todas", command=lambda: mostrar_tareas("todas"))
menu_ver.add_command(label="Día", command=lambda: mostrar_tareas("dia"))
menu_ver.add_command(label="Semana", command=lambda: mostrar_tareas("semana"))
menu_ver.add_command(label="Mes", command=lambda: mostrar_tareas("mes"))


menu_principal.add_command(label="Salir", command=ventana.quit)


# Configurar la cuadrícula para que los frames se expandan
ventana.grid_rowconfigure(0, weight=0)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1, uniform="group1")
ventana.grid_columnconfigure(1, weight=1, uniform="group1")

# Crear el Frame para la fecha y hora
frame_top = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1, style="hola.TFrame")
frame_top.grid(row=0, column=0, columnspan=2, sticky="ew")

# Agregar un Label para la fecha y hora en el frame_top
label_datetime = tk.Label(frame_top, text="", font=("Helvetica", 12, "bold"), bg="CadetBlue3")
label_datetime.pack()

def update_datetime():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_datetime.config(text=now)
    ventana.after(1000, update_datetime)

# Iniciar la actualización de la fecha y hora
update_datetime()

# Crear el Frame para la primera columna (Materias)
frame_left = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1, style="hola.TFrame")
frame_left.grid(row=1, column=0, sticky="nsew")

# Crear el Frame para la segunda columna (Lista de Tareas)
frame_right = ttk.Frame(ventana, padding="10", relief="sunken", borderwidth=1, style="hola.TFrame")
frame_right.grid(row=1, column=1, sticky="nsew")

# Agregar un Label y Listbox en la primera columna
label_materias = tk.Label(frame_left, text="Materias", font=font, bg="CadetBlue3")
label_materias.pack(pady=5, anchor="n")

lista_materias = tk.Listbox(frame_left, height=15)
lista_materias.pack(pady=5, fill="both", expand=True)



scrollbar = tk.Scrollbar(lista_materias, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Vincular la Listbox y la Scrollbar
lista_materias.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lista_materias.yview)



# Lista para almacenar las materias
materias = []

def abrir_ventana_agregar_materias():
    # Obtener posición de la ventana principal
    x = ventana.winfo_x()
    y = ventana.winfo_y()
    
    # Calcular la posición cercana (desplazar un poco desde la ventana principal)
    ventana_x = x + 100  # Desplazar 100 píxeles en horizontal
    ventana_y = y + 100  # Desplazar 100 píxeles en vertical

    ventana_materia = tk.Toplevel(ventana)
    ventana_materia.title("Agregar materia")
    ventana_materia.geometry(f"200x200+{ventana_x}+{ventana_y}")
    ventana_materia.resizable(width=0, height=0)

    label_nombre_materia = ttk.Label(ventana_materia, text="Nombre de la Materia:")
    label_nombre_materia.pack(padx=10, pady=5)

    entrada_nombre_materia = ttk.Entry(ventana_materia)
    entrada_nombre_materia.pack(padx=10, pady=5)

    entrada_nombre_materia.focus_set()

    def agregar_materia_desde_emergente():
        nombre_materia = entrada_nombre_materia.get()
        materias.append(nombre_materia)
        actualizar_listbox_materias()
        global cambios_no_guardados
        cambios_no_guardados = True
        ventana_materia.destroy()

    button_agregar = ttk.Button(ventana_materia, text="Agregar materia", command=agregar_materia_desde_emergente)
    button_agregar.pack(pady=10)

    # Función para manejar la tecla Enter
    def manejar_tecla(event):
      button_agregar.invoke() 

    # Vincular la tecla Enter al evento de la ventana
    ventana_materia.bind('<Return>', manejar_tecla)

def actualizar_listbox_materias():
    lista_materias.delete(0, tk.END)
    for materia in materias:
        lista_materias.insert(tk.END, materia)

button_agregar_materia = ttk.Button(frame_left, text="Agregar Materia", command=abrir_ventana_agregar_materias)
button_agregar_materia.pack(side="left", padx=5, pady=5)

def eliminar_materia():
    seleccion = lista_materias.curselection()
    if seleccion:
            materia_a_eliminar = materias[seleccion[0]]
            
            # Eliminar la materia de la lista de materias
            del materias[seleccion[0]]
            
            # Eliminar las tareas asociadas a la materia eliminada
            global tareas
            tareas = [tarea for tarea in tareas if tarea[2] != materia_a_eliminar]
            
            # Actualizar las listas en la interfaz
            actualizar_listbox_materias()
            actualizar_listbox_tarea()
            
            # Marcar que hay cambios no guardados
            global cambios_no_guardados
            cambios_no_guardados = True

button_eliminar_materia = ttk.Button(frame_left, text="Eliminar Materia", command=eliminar_materia)
button_eliminar_materia.pack(side="right", padx=5, pady=5)

# Filtro de tareas que se visualizan al seleccionar una materia
def materia_seleccionada(event):
    seleccion = lista_materias.curselection()
    if seleccion:
        index = seleccion[0]
        nombre_materia = lista_materias.get(index)
        lista_tareas.delete(0, tk.END)
        for tarea, fecha, materia in tareas:
          if nombre_materia == materia:
            lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})")

lista_materias.bind("<<ListboxSelect>>", materia_seleccionada)

def deseleccionar_materia(event):
    # Verifica si el clic fue fuera de la Listbox de materias
    if lista_materias.nearest(event.y) == -1:
        # Elimina la selección
        lista_materias.selection_clear(0, tk.END)

# Vincula el evento de clic a la ventana principal
ventana.bind("<Button-1>", deseleccionar_materia)





# Agregar un Label y Listbox en la segunda columna
label_tareas = tk.Label(frame_right, text="Tareas Pendientes", font=font, bg="CadetBlue3")
label_tareas.pack(pady=5, anchor="n")

lista_tareas = tk.Listbox(frame_right, height=15)
lista_tareas.pack(pady=5, fill="both", expand=True)


scrollbar = tk.Scrollbar(lista_tareas, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Vincular la Listbox y la Scrollbar
lista_tareas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lista_tareas.yview)


tareas = []

def abrir_ventana_agregar_tarea():
    # Obtener posición de la ventana principal
    x = ventana.winfo_x()
    y = ventana.winfo_y()
    
    # Calcular la posición cercana (desplazar un poco desde la ventana principal)
    ventana_x = x + 100  # Desplazar 100 píxeles en horizontal
    ventana_y = y + 100  # Desplazar 100 píxeles en vertical

    ventana_tarea = tk.Toplevel(ventana)
    ventana_tarea.title("Agregar Tarea")
    ventana_tarea.geometry(f"220x260+{ventana_x}+{ventana_y}")
    ventana_tarea.resizable(width=0, height=0)

    label_nombre_tarea = ttk.Label(ventana_tarea, text="Nombre de la Tarea:")
    label_nombre_tarea.pack(padx=10, pady=5)

    entrada_nombre_tarea = ttk.Entry(ventana_tarea)
    entrada_nombre_tarea.pack(padx=10, pady=5)
    entrada_nombre_tarea.focus_set()

    label_materia_correspondiente = ttk.Label(ventana_tarea, text="Materia a la que corresponde:")
    label_materia_correspondiente.pack(padx=10, pady=5)

    variable_menu_materias = tk.StringVar(ventana_tarea)
    menu_materias = ttk.Combobox(ventana_tarea, values=materias, state='readonly', width=21)
    menu_materias.set("Selecciona una materia")
    menu_materias.pack(padx=10, pady=5)

    label_fecha_limite = ttk.Label(ventana_tarea, text="Fecha Límite:")
    label_fecha_limite.pack(padx=10, pady=5)

    entrada_fecha_limite = DateEntry(ventana_tarea, date_pattern='yyyy-mm-dd')
    entrada_fecha_limite.pack(padx=10, pady=5)

    label_hora_limite = ttk.Label(ventana_tarea, text="Hora Límite (HH:MM):")
    label_hora_limite.pack(padx=10, pady=5)

    spinbox_hora = ttk.Spinbox(ventana_tarea, from_=0, to=23, width=5, format="%02.0f")
    spinbox_hora.pack(side="left", padx=(10, 2), pady=5)
    spinbox_hora.set(00)

    spinbox_minuto = ttk.Spinbox(ventana_tarea, from_=0, to=59, width=5, format="%02.0f")
    spinbox_minuto.pack(side="left", padx=(2, 10), pady=5)
    spinbox_minuto.set(00)

    def agregar_tarea_desde_emergente():
        nombre_tarea = entrada_nombre_tarea.get()
        fecha_limite = entrada_fecha_limite.get_date()
        hora_limite = int(spinbox_hora.get())
        minuto_limite = int(spinbox_minuto.get())
        materia_correspondiente = menu_materias.get()

        if nombre_tarea and fecha_limite and materia_correspondiente != "Selecciona una materia":
            fecha_hora_limite = datetime.datetime.combine(fecha_limite, datetime.time(hora_limite, minuto_limite))
            tareas.append((nombre_tarea, fecha_hora_limite, materia_correspondiente))
            tareas.sort(key=lambda x: x[1])
            actualizar_listbox_tarea()
            global cambios_no_guardados
            cambios_no_guardados = True
            ventana_tarea.destroy()

    button_agregar = ttk.Button(ventana_tarea, text="Agregar Tarea", command=agregar_tarea_desde_emergente)
    button_agregar.pack(pady=10)

    # Función para manejar la tecla Enter
    def manejar_tecla(event):
      button_agregar.invoke() 

    # Vincular la tecla Enter al evento de la ventana
    ventana_tarea.bind('<Return>', manejar_tecla)

def actualizar_listbox_tarea():
    lista_tareas.delete(0, tk.END)
    for tarea, fecha, materia in tareas:
        lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})")

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

def editar_materia(event):
    seleccion = lista_materias.curselection()
    if seleccion:
        index = seleccion[0]
        materia_a_editar = materias[index]
        
        x = ventana.winfo_x()
        y = ventana.winfo_y()
        
        # Calcular la posición cercana (desplazar un poco desde la ventana principal)
        ventana_x = x + 100  # Desplazar 100 píxeles en horizontal
        ventana_y = y + 100  # Desplazar 100 píxeles en vertical
        
        ventana_editar_materia = tk.Toplevel(ventana)
        ventana_editar_materia.title("Editar Materia")
        ventana_editar_materia.geometry(f"210x220+{ventana_x}+{ventana_y}")
        ventana_editar_materia.resizable(width=0, height=0)
        
        label_nombre_materia = ttk.Label(ventana_editar_materia, text="Editar nombre de la materia:")
        label_nombre_materia.pack(padx=10, pady=5)
        
        entrada_nombre_materia = ttk.Entry(ventana_editar_materia)
        entrada_nombre_materia.insert(0, materia_a_editar)
        entrada_nombre_materia.pack(padx=10, pady=5)
        
        def guardar_materia_editada():
            nuevo_nombre = entrada_nombre_materia.get()

            # Actualizar el nombre de la materia en la lista de materias
            materias[index] = nuevo_nombre
            
            # Actualizar las tareas que correspondían a la materia editada
            for i, (nombre_tarea, fecha_limite, materia_tarea) in enumerate(tareas):
                if materia_tarea == materia_a_editar:
                    # Cambiar la referencia de la materia en las tareas afectadas
                    tareas[i] = (nombre_tarea, fecha_limite, nuevo_nombre)
            
            # Actualizar las listas visuales
            actualizar_listbox_materias()
            actualizar_listbox_tarea()
            global cambios_no_guardados
            cambios_no_guardados = True
            ventana_editar_materia.destroy()
        
        button_guardar = ttk.Button(ventana_editar_materia, text="Guardar", command=guardar_materia_editada)
        button_guardar.pack(pady=10)

lista_materias.bind("<Double-Button-1>", editar_materia)


def editar_tarea(event):
    seleccion = lista_tareas.curselection()
    if seleccion:
        index_tarea = seleccion[0]
        tarea_a_editar = lista_tareas.get(index_tarea)
        
        # Buscar la tarea en la lista de tareas
        for i, (nombre_tarea, fecha, materia) in enumerate(tareas):
            if f"{nombre_tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})" == tarea_a_editar:
                index_tarea = i
                break
        

        # Obtener posición de la ventana principal
        x = ventana.winfo_x()
        y = ventana.winfo_y()
        
        # Calcular la posición cercana (desplazar un poco desde la ventana principal)
        ventana_x = x + 100  # Desplazar 100 píxeles en horizontal
        ventana_y = y + 100  # Desplazar 100 píxeles en vertical
        ventana_editar_tarea = tk.Toplevel(ventana)
        ventana_editar_tarea.title("Editar Tarea")
        ventana_editar_tarea.geometry(f"220x260+{ventana_x}+{ventana_y}")
        ventana_editar_tarea.resizable(width=0, height=0)
        
        nombre_tarea, fecha, materia = tareas[index_tarea]

        label_nombre_tarea = ttk.Label(ventana_editar_tarea, text="Editar nombre de la tarea:")
        label_nombre_tarea.pack(padx=10, pady=5)
        
        entrada_nombre_tarea = ttk.Entry(ventana_editar_tarea)
        entrada_nombre_tarea.insert(0, nombre_tarea)
        entrada_nombre_tarea.pack(padx=10, pady=5)
        
        label_materia_correspondiente = ttk.Label(ventana_editar_tarea, text="Materia a la que corresponde:")
        label_materia_correspondiente.pack(padx=10, pady=5)
        
        menu_materias = ttk.Combobox(ventana_editar_tarea, values=materias, state='readonly', width=21)
        menu_materias.set(materia)
        menu_materias.pack(padx=10, pady=5)
        
        label_fecha_limite = ttk.Label(ventana_editar_tarea, text="Editar fecha límite:")
        label_fecha_limite.pack(padx=10, pady=5)

        entrada_fecha_limite = DateEntry(ventana_editar_tarea, date_pattern='yyyy-mm-dd')
        entrada_fecha_limite.set_date(fecha)
        entrada_fecha_limite.pack(padx=10, pady=5)

        label_hora_limite = ttk.Label(ventana_editar_tarea, text="Editar hora límite (HH:MM):")
        label_hora_limite.pack(padx=10, pady=5)
        
        spinbox_hora = ttk.Spinbox(ventana_editar_tarea, from_=0, to=23, width=5, format="%02.0f")
        spinbox_hora.set(fecha.hour)
        spinbox_hora.pack(side="left", padx=(10, 2), pady=5)
        
        spinbox_minuto = ttk.Spinbox(ventana_editar_tarea, from_=0, to=59, width=5, format="%02.0f")
        spinbox_minuto.set(fecha.minute)
        spinbox_minuto.pack(side="left", padx=(2, 10), pady=5)
        
        def guardar_tarea_editada():
            nuevo_nombre = entrada_nombre_tarea.get()
            nueva_materia = menu_materias.get()
            nueva_fecha = entrada_fecha_limite.get_date()
            nueva_hora = int(spinbox_hora.get())
            nuevo_minuto = int(spinbox_minuto.get())
            
            nueva_fecha_hora = datetime.datetime.combine(nueva_fecha, datetime.time(nueva_hora, nuevo_minuto))
            
            tareas[index_tarea] = (nuevo_nombre, nueva_fecha_hora, nueva_materia)
            tareas.sort(key=lambda x: x[1])
            actualizar_listbox_tarea()
            global cambios_no_guardados
            cambios_no_guardados = True
            ventana_editar_tarea.destroy()
        
        button_guardar = ttk.Button(ventana_editar_tarea, text="Guardar", command=guardar_tarea_editada)
        button_guardar.pack(pady=10)

lista_tareas.bind("<Double-Button-1>", editar_tarea)




# Filtrar y mostrar las tareas según el filtro seleccionado
def mostrar_tareas(filtro):
    hoy = datetime.datetime.today()
    lista_tareas.delete(0, tk.END)
    
    if filtro == "todas":
        for tarea, fecha, materia in tareas:
            lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})")
    
    elif filtro == "dia":
        for tarea, fecha, materia in tareas:
            if fecha.date() == hoy.date():
                lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})")
    
    elif filtro == "semana":
        for tarea, fecha, materia in tareas:
            if hoy <= fecha <= hoy + datetime.timedelta(days=7):
                lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})")
    
    elif filtro == "mes":
        for tarea, fecha, materia in tareas:
            if hoy <= fecha <= hoy + datetime.timedelta(days=30):
                lista_tareas.insert(tk.END, f"{tarea} (Límite: {fecha.strftime('%Y-%m-%d %H:%M')})  ({materia})")

# Menú emergente con clic derecho para tener una vista general de las materias
menu_vistas = tk.Menu(ventana,tearoff=0)
menu_vistas.add_command(label="Ver todas las tareas", command= actualizar_listbox_tarea)

def mostrar_menu_vistas(event):
    # Posición del clic derecho
    x, y = event.x_root, event.y_root
    # Mostrar el menú en la posición del clic derecho
    menu_vistas.post(x, y)

lista_tareas.bind("<Button-3>", mostrar_menu_vistas)





# Funciones para manejo de archivos
def nuevo_archivo():
    global tareas, materias, cambios_no_guardados
    if cambios_no_guardados:
        respuesta = messagebox.askyesnocancel("Guardar cambios", "¿Deseas guardar los cambios antes de continuar?")
        if respuesta is None:
            return
        if respuesta:
            guardar_datos()

    tareas = []
    materias = []
    actualizar_listbox_tarea()
    actualizar_listbox_materias()
    cambios_no_guardados = False

def guardar_datos():
    archivo_guardado = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
    if archivo_guardado:
        datos = {"tareas": [(tarea, fecha.strftime("%Y-%m-%d %H:%M"), materia) for tarea, fecha, materia in tareas],
                 "materias": materias}
        with open(archivo_guardado, 'w') as f:
            json.dump(datos, f)
        global cambios_no_guardados
        cambios_no_guardados = False

def cargar_datos():
    global tareas, materias, cambios_no_guardados
    archivo_cargado = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
    if archivo_cargado:
        with open(archivo_cargado, 'r') as f:
            datos = json.load(f)
        tareas = [(tarea, datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M"), materia) for tarea, fecha, materia in datos["tareas"]]
        materias = datos["materias"]
        actualizar_listbox_tarea()
        actualizar_listbox_materias()
        cambios_no_guardados = False


def cerrar_programa():
    if cambios_no_guardados:
        respuesta = messagebox.askyesnocancel("Guardar cambios", "¿Deseas guardar los cambios antes de salir?")
        if respuesta is None:
            return
        if respuesta:
            guardar_datos()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar_programa)

# Iniciar el bucle de la aplicación
ventana.mainloop()
