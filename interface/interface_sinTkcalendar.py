# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:46:25 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from PIL import Image, ImageTk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Event AI")
        
        self.data = []  # Almacenar los datos de la tabla
        self.page_size = 10  # Tamaño de la página
        self.current_page = 0  # Página actual
        
        # Crear los elementos de la interfaz
        self.create_main_section()
        
        # Mostrar la primera página al inicio
        self.show_page(self.current_page)
        


    def create_main_section(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.create_buttons_section(main_frame)
        self.create_table_section(main_frame)
        self.create_navigation_section(main_frame)

    def create_table_section(self, main_frame):
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        self.table = ttk.Treeview(table_frame, columns=("ID", "Evento", "Fecha", "Asistentes", "Hombres", "Mujeres"), show="headings")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Evento", text="Evento", anchor="center")
        self.table.heading("Fecha", text="Fecha", anchor="center")
        self.table.heading("Asistentes", text="Asistentes",  anchor="center")
        self.table.heading("Hombres", text="Hombres", anchor="center")
        self.table.heading("Mujeres", text="Mujeres", anchor="center")
    
        # Personalizar el tamaño de cada columna
        self.table.column("ID", width=50, anchor="center")
        self.table.column("Evento", width=200, anchor="center")
        self.table.column("Fecha", width=100, anchor="center")
        self.table.column("Asistentes", width=100, anchor="center")
        self.table.column("Hombres", width=100, anchor="center")
        self.table.column("Mujeres", width=100, anchor="center")
    
        self.table.pack()
        self.fill_data_from_database()
 

    def create_navigation_section(self, main_frame):
        navigation_frame = ttk.Frame(main_frame)
        navigation_frame.pack(side=tk.TOP, fill=tk.X, padx=50, pady=10)
    
        first_page_button = ttk.Button(navigation_frame, text="<<", command=self.first_page)
        first_page_button.pack(side=tk.LEFT, padx=10)
    
        prev_page_button = ttk.Button(navigation_frame, text="<", command=self.prev_page)
        prev_page_button.pack(side=tk.LEFT, padx=10)
    
        self.page_label = ttk.Label(navigation_frame, text="Página:")
        self.page_label.pack(side=tk.LEFT, padx=10)
    
        self.page_entry = ttk.Entry(navigation_frame, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=10)
    
        next_page_button = ttk.Button(navigation_frame, text=">", command=self.next_page)
        next_page_button.pack(side=tk.LEFT, padx=10)
    
        last_page_button = ttk.Button(navigation_frame, text=">>", command=self.last_page)
        last_page_button.pack(side=tk.LEFT, padx=10)


    def create_buttons_section(self, main_frame):
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, padx=20, pady=10)
    
        add_button = ttk.Button(button_frame, text="Agregar")
        add_button.pack(pady=5)
    
        generate_button = ttk.Button(button_frame, text="Generar")
        generate_button.pack(pady=5)
    
        edit_button = ttk.Button(button_frame, text="Editar")
        edit_button.pack(pady=5)
        edit_button.config(command=self.edit_button_clicked)
    
        delete_button = ttk.Button(button_frame, text="Eliminar")
        delete_button.pack(pady=5)
        delete_button.config(command=self.delete_button_clicked)
    
        filter_button2 = ttk.Button(button_frame, text="Filtrar")
        filter_button2.pack(pady=5)
    
    
    
       
        # Cuadro para la selección de fechas de inicio
        date_frame = ttk.Frame(button_frame)
        date_frame.pack(pady=5)
        
        # Etiqueta para la fecha de inicio
        start_date_label = ttk.Label(date_frame, text="Fecha inicio:")
        start_date_label.grid(row=0, column=0, padx=0)
        
        # Etiqueta para el mes de fecha de inicio
        start_month_label = ttk.Label(date_frame, text="M:")
        start_month_label.grid(row=1, column=0, padx=0)
        
        # Cuadro de selección de mes de fecha de inicio
        self.start_month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, width=3)
        self.start_month_spinbox.grid(row=1, column=1, padx=0)
        
        # Etiqueta para el año de fecha de inicio
        start_year_label = ttk.Label(date_frame, text="A:")
        start_year_label.grid(row=1, column=2, padx=0)
        
        # Cuadro de selección de año de fecha de inicio
        self.start_year_spinbox = ttk.Spinbox(date_frame, from_=2000, to=2100, width=6)
        self.start_year_spinbox.grid(row=1, column=3, padx=5)
        
        # Etiqueta para la fecha de finalización
        end_date_label = ttk.Label(date_frame, text="Fecha final:")
        end_date_label.grid(row=2, column=0, padx=0)
        
        # Etiqueta para el mes de fecha de finalización
        end_month_label = ttk.Label(date_frame, text="M:")
        end_month_label.grid(row=3, column=0, padx=0)
        
        # Cuadro de selección de mes de fecha de finalización
        self.end_month_spinbox = ttk.Spinbox(date_frame, from_=1, to=12, width=3)
        self.end_month_spinbox.grid(row=3, column=1, padx=0)
        
        # Etiqueta para el año de fecha de finalización
        end_year_label = ttk.Label(date_frame, text="A:")
        end_year_label.grid(row=3, column=2, padx=0)
        
        # Cuadro de selección de año de fecha de finalización
        self.end_year_spinbox = ttk.Spinbox(date_frame, from_=2000, to=2100, width=6)
        self.end_year_spinbox.grid(row=3, column=3, padx=0)




    def show_page(self, page):
        # Calcula el índice de inicio y fin para la página actual
        start = page * self.page_size
        end = (page + 1) * self.page_size

        # Borra todos los elementos de la tabla
        for item in self.table.get_children():
            self.table.delete(item)

        # Llena la tabla con los datos de la página actual, calculando "Asistentes"
        for item in self.data[start:end]:
            id_evento, evento, fecha, hombres, mujeres = item[0], item[1], item[2], item[3], item[4]
            asistentes = hombres + mujeres  # Calcula la suma de asistentes
            self.table.insert("", "end", values=(id_evento, evento, fecha, asistentes, hombres, mujeres))

        # Actualiza la etiqueta de página actual
        self.page_label.config(text=f"Página: {page + 1}")
        # Actualiza la entrada de página
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, str(page + 1))

    def first_page(self):
        self.current_page = 0
        self.show_page(self.current_page)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def next_page(self):
        total_pages = (len(self.data) - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.show_page(self.current_page)

    def last_page(self):
        total_pages = (len(self.data) - 1) // self.page_size
        self.current_page = total_pages
        self.show_page(self.current_page)


    def fill_data_from_database(self):
        # Vaciar self.data antes de llenarlo con la información de la base de datos
        self.data = []

        # Intentar conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("eventos.db")
            cursor = conn.cursor()

            # Realizar una consulta SQL para obtener los registros de la tabla "eventos" para la página actual
            cursor.execute("SELECT id, nombre_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos")

            # Obtener los registros de la página actual
            eventos = cursor.fetchall()

            # Cerrar la conexión a la base de datos
            conn.close()

            # Llenar self.data con la información de eventos
            for evento in eventos:
                self.data.append(evento)
                
        except sqlite3.Error as e:
            # Si ocurre un error al conectar o ejecutar la consulta, se capturará aquí
            print("Error al conectar a la base de datos:", e)


    def edit_button_clicked(self):
        # Obtener la fila seleccionada de la tabla
        selected_item = self.table.selection()
        if selected_item:
            # Obtener los valores de la fila seleccionada
            selected_row = self.table.item(selected_item)
            values = selected_row['values']
            
            # Crear una ventana emergente para editar la información
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Editar Evento")
            self.edit_window.geometry("200x300")  # Establecer el tamaño de la ventana
    
            # Personalizar el estilo de la ventana emergente
            self.edit_window.configure(bg="white")  # Cambiar el fondo a blanco
    
            # Agregar un marco para un diseño más elegante
            frame = ttk.Frame(self.edit_window)
            frame.pack(expand=True, fill="both")
    
            evento_label = ttk.Label(frame, text="Evento:")
            evento_label.pack(pady=5)
            self.evento_id=values[0]
            self.evento_entry = ttk.Entry(frame)
            self.evento_entry.insert(0, values[1])  # Llenar con el valor actual
            self.evento_entry.pack(pady=5, fill="x")
    
            fecha_label = ttk.Label(frame, text="Fecha:")
            fecha_label.pack(pady=5)
            self.fecha_entry = ttk.Entry(frame)
            self.fecha_entry.insert(0, values[2])  # Llenar con el valor actual
            self.fecha_entry.pack(pady=5, fill="x")
    
            hombres_label = ttk.Label(frame, text="Hombres:")
            hombres_label.pack(pady=5)
            self.hombres_entry = ttk.Entry(frame)
            self.hombres_entry.insert(0, values[4])  # Llenar con el valor actual
            self.hombres_entry.pack(pady=5, fill="x")
    
            mujeres_label = ttk.Label(frame, text="Mujeres:")
            mujeres_label.pack(pady=5)
            self.mujeres_entry = ttk.Entry(frame)
            self.mujeres_entry.insert(0, values[5])  # Llenar con el valor actual
            self.mujeres_entry.pack(pady=5, fill="x")
    
            # Agregar un botón para guardar los cambios
            save_button = ttk.Button(frame, text="Guardar", command=self.save_changes)
            save_button.pack(pady=10)
    


    def save_changes(self):
        # Obtener los valores modificados
        evento_id = self.evento_id
        evento = self.evento_entry.get()
        fecha = self.fecha_entry.get()
        hombres = self.hombres_entry.get()
        mujeres = self.mujeres_entry.get()
        
        # Realizar validaciones
        if not evento or not fecha or not hombres or not mujeres:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "Ningún campo puede quedar vacío.")
            
            # Hacer que la ventana de edición parpadee
            self.flash_edit_window()
            return
        
        try:
            # Verificar que la fecha tenga un formato válido
            datetime.datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "El formato de fecha debe ser YYYY-MM-DD.")
            
            # Restablecer el valor en el campo de fecha a "YYYY-MM-DD"
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, "YYYY-MM-DD")
            
            # Hacer que la ventana de edición parpadee
            self.flash_edit_window()
            return
        
        try:
            # Verificar que los campos "Hombres" y "Mujeres" contengan números enteros mayores o iguales a 0
            hombres = int(hombres)
            mujeres = int(mujeres)
            if hombres < 0 or mujeres < 0:
                # Mostrar un mensaje de error
                tk.messagebox.showerror("Error", "Los campos 'Hombres' y 'Mujeres' deben ser números enteros no negativos.")
                
                # Hacer que la ventana de edición parpadee
                self.flash_edit_window()
                return
        except ValueError:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "Los campos 'Hombres' y 'Mujeres' deben ser números enteros no negativos.")
            
            # Hacer que la ventana de edición parpadee
            self.flash_edit_window()
            return
       
        
        # Actualizar la base de datos con los nuevos valores
        try:
            conn = sqlite3.connect("eventos.db")
            cursor = conn.cursor()
            
            # Construir y ejecutar la sentencia SQL UPDATE
            update_query = "UPDATE eventos SET nombre_evento = ?, fecha_evento = ?, asistentes_hombres = ?, asistentes_mujeres = ? WHERE id = ?"
            cursor.execute(update_query, (evento, fecha, hombres, mujeres, evento_id))
            
            # Confirmar los cambios en la base de datos
            conn.commit()
            
            # Cerrar la conexión a la base de datos
            conn.close()
        except sqlite3.Error as e:
            # Si ocurre un error al actualizar la base de datos, muestra un mensaje de error
            tk.messagebox.showerror("Error", "No se pudo actualizar la base de datos: " + str(e))
        
        
        self.fill_data_from_database()
        self.show_page(self.current_page)
        # Cerrar la ventana emergente de edición
        self.edit_window.destroy()
    
    
    def flash_edit_window(self):
        # Hacer que la ventana de edición parpadee
        self.edit_window.iconify()  # Ocultar la ventana de edición
        self.root.update()  # Forzar la actualización de la ventana principal
        self.root.after(500, self.edit_window.deiconify)  # Mostrar la ventana de edición después de 500 ms
    
    def delete_button_clicked(self):
        # Obtener la fila seleccionada de la tabla
        selected_item = self.table.selection()
        if selected_item:
            # Obtener los valores de la fila seleccionada
            selected_row = self.table.item(selected_item)
            values = selected_row['values']
            
            # Crear una ventana emergente para confirmar la eliminación
            self.delete_window = tk.Toplevel(self.root)
            self.delete_window.title("Eliminar Evento")
            self.delete_window.geometry("200x300")  # Establecer el tamaño de la ventana
    
            # Personalizar el estilo de la ventana emergente
            self.delete_window.configure(bg="white")  # Cambiar el fondo a blanco
    
            # Agregar un marco para un diseño más elegante
            frame = ttk.Frame(self.delete_window)
            frame.pack(expand=True, fill="both")
            
            self.evento_id=values[0]
            evento_label = ttk.Label(frame, text="Evento:")
            evento_label.pack(pady=5)
            evento_value_label = ttk.Label(frame, text=values[1])
            evento_value_label.pack(pady=5)
    
            fecha_label = ttk.Label(frame, text="Fecha:")
            fecha_label.pack(pady=5)
            fecha_value_label = ttk.Label(frame, text=values[2])
            fecha_value_label.pack(pady=5)
    
            hombres_label = ttk.Label(frame, text="Hombres:")
            hombres_label.pack(pady=5)
            hombres_value_label = ttk.Label(frame, text=values[4])
            hombres_value_label.pack(pady=5)
    
            mujeres_label = ttk.Label(frame, text="Mujeres:")
            mujeres_label.pack(pady=5)
            mujeres_value_label = ttk.Label(frame, text=values[5])
            mujeres_value_label.pack(pady=5)
    
            # Agregar un botón para confirmar la eliminación
            delete_button = ttk.Button(frame, text="Eliminar", command=self.confirm_delete)
            delete_button.pack(pady=10)

    
    def confirm_delete(self):

        evento_id = self.evento_id

        # Eliminar el evento de la base de datos
        try:
            conn = sqlite3.connect("eventos.db")
            cursor = conn.cursor()

            # Construir y ejecutar la sentencia SQL DELETE
            delete_query = "DELETE FROM eventos WHERE id = ?"
            cursor.execute(delete_query, (evento_id,))

            # Confirmar los cambios en la base de datos
            conn.commit()

            # Cerrar la conexión a la base de datos
            conn.close()
        except sqlite3.Error as e:
            # Si ocurre un error al eliminar de la base de datos, muestra un mensaje de error
            tk.messagebox.showerror("Error", "No se pudo eliminar el evento: " + str(e))

        # Recargar los datos de la base de datos y mostrar la página actual
        self.fill_data_from_database()
        self.show_page(self.current_page)

        # Cerrar la ventana emergente de eliminación
        self.delete_window.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


