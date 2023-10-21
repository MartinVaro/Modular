# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:46:25 2023

@author: akava
"""

import customtkinter
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from filemaker.file_maker import FileMaker
from tkcalendar import DateEntry
import openpyxl
from tkinter import filedialog
from load.photo_load_page import PhotoLoadPage
from PIL import Image
import re

class App:
    def __init__(self, root):
        
        customtkinter.set_default_color_theme("dark-blue")
        
        self.root = root
        self.root.title("Event AI")
        self.data = []  # Almacenar los datos de la tabla
        self.page_size = 10  # Tamaño de la página
        self.current_page = 0  # Página actual
        self.total_pages = 0
        
        # Crear los elementos de la interfaz
        self.create_main_section()
        
        # Mostrar la primera página al inicio
        self.show_page(self.current_page)
        

    def create_main_section(self):
        main_frame = customtkinter.CTkFrame(self.root, fg_color=("transparent"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.create_buttons_section(main_frame)
        self.create_table_section(main_frame)
        self.create_navigation_section(main_frame)

    def create_table_section(self, main_frame):
        table_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 12,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        
            
        self.table = ttk.Treeview(table_frame, style="mystyle.Treeview", columns=("ID",  "Evento", "Fecha", "Asistentes", "Hombres", "Mujeres"), show="headings")
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
        navigation_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        navigation_frame.pack(side=tk.TOP, fill=tk.X, padx=50, pady=10)
    
        first_image = customtkinter.CTkImage(Image.open("images/primera.png"), size=(26, 26))
        first_page_button = customtkinter.CTkButton(navigation_frame, command=self.first_page, image=first_image, text="", fg_color="transparent",width=80)
        first_page_button.pack(side=tk.LEFT, padx=5)
    
        prev_image = customtkinter.CTkImage(Image.open("images/atras.png"), size=(26, 26))
        prev_page_button = customtkinter.CTkButton(navigation_frame, command=self.prev_page, image=prev_image, text="", fg_color="transparent",width=80)
        prev_page_button.pack(side=tk.LEFT, padx=5)
    
        self.page_label = customtkinter.CTkLabel(navigation_frame, text="Página:")
        self.page_label.pack(side=tk.LEFT, padx=5)
    
        self.page_entry = customtkinter.CTkEntry(navigation_frame, font=('Calibri', 15,'bold'), width=40)
        self.page_entry.configure(justify="center")
        self.page_entry.pack(side=tk.LEFT, padx=5)
    
        next_image = customtkinter.CTkImage(Image.open("images/siguiente.png"), size=(26, 26))
        next_page_button = customtkinter.CTkButton(navigation_frame, command=self.next_page, image=next_image, text="", fg_color="transparent", width=80)
        next_page_button.pack(side=tk.LEFT, padx=5)
    
        last_image = customtkinter.CTkImage(Image.open("images/ultima.png"), size=(26, 26))
        last_page_button = customtkinter.CTkButton(navigation_frame, command=self.last_page, image=last_image, text="", fg_color="transparent", width=80)
        last_page_button.pack(side=tk.LEFT, padx=5)

        go_to_image = customtkinter.CTkImage(Image.open("images/seleccionar.png"), size=(26, 26))
        go_to_button = customtkinter.CTkButton(navigation_frame, command=self.go_to_page, image=go_to_image, text="", fg_color="transparent", width=80)
        go_to_button.pack(side=tk.LEFT, padx=5)


    def create_buttons_section(self, main_frame):
       
        buttons_section_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        buttons_section_frame.pack(side=tk.RIGHT)
        # Crear y colocar los botones en la cuadrícula
        
        add_image = customtkinter.CTkImage(Image.open("images/nuevo.png"), size=(26, 26))
        add_button = customtkinter.CTkButton(buttons_section_frame, image=add_image,  text_color= "black", text="Añadir ", fg_color="transparent", width=150)
        add_button.grid(row=0, column=0, padx=10, pady=10)
        add_button.configure(command=self.open_photo_load_page)

        recharge_image = customtkinter.CTkImage(Image.open("images/recargar.png"), size=(26, 26))
        recharge_button = customtkinter.CTkButton(buttons_section_frame, image= recharge_image,  text_color= "black", text="Recargar", fg_color="transparent", width=150)
        recharge_button.grid(row=0, column=1, padx=10, pady=10)
        recharge_button.configure(command=self.recharge_button_clicked)

        edit_image = customtkinter.CTkImage(Image.open("images/editar.png"), size=(26, 26))
        edit_button = customtkinter.CTkButton(buttons_section_frame, image=edit_image,  text_color= "black", text="Editar ", fg_color="transparent", width=150)
        edit_button.grid(row=2, column=0, padx=10, pady=10)
        edit_button.configure(command=self.edit_button_clicked)

        pdf_image = customtkinter.CTkImage(Image.open("images/pdf.png"), size=(26, 26))
        pdf_button = customtkinter.CTkButton(buttons_section_frame, image= pdf_image, text_color= "black", text="PDF   ", fg_color="transparent", width=150)
        pdf_button.grid(row=1, column=0, padx=10, pady=10)
        pdf_button.configure(command=self.pdf_button_clicked)
        
        excel_image = customtkinter.CTkImage(Image.open("images/excel.png"), size=(26, 26))
        excel_button = customtkinter.CTkButton(buttons_section_frame, image=excel_image, text_color= "black", text="  Excel     ", fg_color="transparent", width=150)
        excel_button.grid(row=1, column=1, padx=10, pady=10)
        excel_button.configure(command=self.excel_button_clicked)

        delete_image = customtkinter.CTkImage(Image.open("images/borrar.png"), size=(26, 26))
        delete_button = customtkinter.CTkButton(buttons_section_frame, image= delete_image,  text_color= "black", text="  Eliminar", fg_color="transparent", width=150)
        delete_button.grid(row=2, column=1, padx=10, pady=10)
        delete_button.configure(command=self.delete_button_clicked)

        filter_image = customtkinter.CTkImage(Image.open("images/filtrar.png"), size=(26, 26))
        filter_button = customtkinter.CTkButton(buttons_section_frame, image= filter_image,  text_color= "black", text="Filtrar", fg_color="transparent", width=150)
        filter_button.grid(row=3, column=0, padx=10, pady=10)
        filter_button.configure(command=self.filter_button_clicked)

        clean_image = customtkinter.CTkImage(Image.open("images/limpiar.png"), size=(26, 26))
        clean_button = customtkinter.CTkButton(buttons_section_frame, image= clean_image,  text_color= "black", text="  Limpiar ", fg_color="transparent", width=150)
        clean_button.grid(row=3, column=1, padx=10, pady=10)
        clean_button.configure(command=self.clear_button_clicked)

        # Crear un calendario de fecha de inicio
        start_date_label = customtkinter.CTkLabel(buttons_section_frame, font=('Calibri', 15,'bold') , text="Fecha inicio:")
        start_date_label.grid(row=4, column=0, padx=10, pady=10)
        self.start_cal = DateEntry(buttons_section_frame, width=8, font=('Calibri', 12), date_pattern="yy/MM/dd")
        self.start_cal.grid(row=5, column=0, padx=10, pady=10)

        # Crear un calendario de fecha de finalización
        end_date_label = customtkinter.CTkLabel(buttons_section_frame, font=('Calibri', 15,'bold') , text="Fecha final:")
        end_date_label.grid(row=4, column=1, padx=40, pady=10)
        self.end_cal = DateEntry(buttons_section_frame, width=8, font=('Calibri', 12), date_pattern="yy/MM/dd")
        self.end_cal.grid(row=5, column=1, padx=40, pady=10)
        
    def show_page(self, page):
        # Calcula el índice de inicio y fin para la página actual
        start = page * self.page_size
        end = (page + 1) * self.page_size
        self.total_pages = ((len(self.data) - 1) / self.page_size)+1

        # Borra todos los elementos de la tabla
        for item in self.table.get_children():
            self.table.delete(item)

        # Llena la tabla con los datos de la página actual, calculando "Asistentes"
        for index, item in enumerate(self.data[start:end]):
            id_evento, evento, fecha, hombres, mujeres = item[0], item[1], item[4], item[5], item[6]
            
            tag = "even" if index % 2 == 0 else "odd"
            
            asistentes = hombres + mujeres  # Calcula la suma de asistentes
            self.table.insert("", "end", values=(id_evento, evento, fecha, asistentes, hombres, mujeres), tags=(tag,))
        
        self.table.tag_configure('odd', background='#FAFAFA')
        self.table.tag_configure('even', background='#EEEEEE')

        # Actualiza la etiqueta de página actual
        self.page_label.configure(text=f"Página: {page + 1}")
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
        self.total_pages = (len(self.data) - 1) // self.page_size
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.show_page(self.current_page)

    def last_page(self):
        self.total_pages = (len(self.data) - 1) // self.page_size
        self.current_page = self.total_pages
        self.show_page(self.current_page)


    def fill_data_from_database(self):
        # Vaciar self.data antes de llenarlo con la información de la base de datos
        self.data = []

        # Intentar conectar a la base de datos SQLite
        try:
            conn = sqlite3.connect("database/eventos.db")
            cursor = conn.cursor()

            # Realizar una consulta SQL para obtener los registros de la tabla "eventos" para la página actual
            cursor.execute("SELECT id, nombre_evento,  nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos")
           
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
            evento_id = values[0]
            
            try:
                # Conectar a la base de datos y obtener información del evento por su ID
                conn = sqlite3.connect("database/eventos.db")
                cursor = conn.cursor()
    
                # Realizar una consulta para obtener información del evento por su ID
                query =" SELECT nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos WHERE id = ?"
                cursor.execute(query, (evento_id,))
                event_data = cursor.fetchone()
    
                # Cerrar la conexión a la base de datos
                conn.close()
    
 
                # Desempaquetar los datos del evento
                conference_name, speakers_names, location, date, num_men, num_women = event_data
                
                # Crear una ventana emergente para editar la información
                self.edit_window = customtkinter.CTkToplevel(self.root)
                self.edit_window.title("Editar Evento")
                self.edit_window.geometry("325x400")  # Establecer el tamaño de la ventana
                self.edit_window.resizable(False, False)
                
                
                # Personalizar el estilo de la ventana emergente
                self.edit_window.configure()  # Cambiar el fondo a blanco
                
                frame = customtkinter.CTkFrame(self.edit_window, fg_color="transparent")
                frame.pack(expand=True, fill="both")
        
                # Etiqueta y entrada para el nombre del evento
                evento_image = customtkinter.CTkImage(Image.open("images/evento.png"), size=(26, 26))
                evento_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Evento:", image=evento_image, compound=tk.LEFT)
                evento_label.grid(row=0, column=0, padx=10, pady=15, sticky=tk.W)
                self.evento_entry = customtkinter.CTkEntry(frame, font=('Calibri', 15), width=175)
                self.evento_entry.insert(0, conference_name)  # Llenar con el valor actual
                self.evento_entry.grid(row=0, column=1, padx=10, pady=15)
    
           
                # Etiqueta y entrada para el nombre de los exponentes
                exponentes_image = customtkinter.CTkImage(Image.open("images/exponente.png"), size=(26, 26))
                exponentes_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Exponentes:", image=exponentes_image, compound=tk.LEFT)
                exponentes_label.grid(row=1, column=0, padx=10, pady=15, sticky=tk.W)
                self.exponentes_entry = customtkinter.CTkEntry(frame, font=('Calibri', 15), width=175)
                self.exponentes_entry.insert(0, speakers_names)  # Llenar con el valor actual
                self.exponentes_entry.grid(row=1, column=1, padx=10, pady=15)
    
    
                # Etiqueta y entrada para la ubicación
                ubicacion_image = customtkinter.CTkImage(Image.open("images/ubicacion.png"), size=(26, 26))
                ubicacion_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Ubicación:", image=ubicacion_image, compound=tk.LEFT)
                ubicacion_label.grid(row=2, column=0, padx=10, pady=15, sticky=tk.W)
                self.ubicacion_entry = customtkinter.CTkEntry(frame, font=('Calibri', 15), width=175)
                self.ubicacion_entry.insert(0, location)  # Llenar con el valor actual
                self.ubicacion_entry.grid(row=2, column=1, padx=10, pady=15)
                
                # Etiqueta y entrada para la fecha
                fecha_image = customtkinter.CTkImage(Image.open("images/fecha.png"), size=(26, 26))
                fecha_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Fecha:", image=fecha_image, compound=tk.LEFT)
                fecha_label.grid(row=3, column=0, padx=10, pady=15, sticky=tk.W)
                self.fecha_entry = customtkinter.CTkEntry(frame, font=('Calibri', 15), width=175)
                self.fecha_entry.insert(0, date)  # Llenar con el valor actual
                self.fecha_entry.grid(row=3, column=1, padx=10, pady=15)
    
                # Etiqueta y entrada para la cantidad de hombres
                hombres_image = customtkinter.CTkImage(Image.open("images/hombre.png"), size=(26, 26))
                hombres_label = customtkinter.CTkLabel(frame, font=('Calibri', 15 ), text="  Hombres:", image=hombres_image, compound=tk.LEFT)
                hombres_label.grid(row=4, column=0, padx=10, pady=15, sticky=tk.W)
                self.hombres_entry = customtkinter.CTkEntry(frame, font=('Calibri', 15), width=175)
                self.hombres_entry.insert(0, num_men)  # Llenar con el valor actual
                self.hombres_entry.grid(row=4, column=1, padx=10, pady=15)
    
                # Etiqueta y entrada para la cantidad de mujeres
                mujeres_image = customtkinter.CTkImage(Image.open("images/mujer.png"), size=(26, 26))
                mujeres_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Mujeres:", image=mujeres_image, compound=tk.LEFT)
                mujeres_label.grid(row=5, column=0, padx=10, pady=15, sticky=tk.W)
                self.mujeres_entry = customtkinter.CTkEntry(frame, font=('Calibri', 15), width=175)
                self.mujeres_entry.insert(0, num_women)  # Llenar con el valor actual
                self.mujeres_entry.grid(row=5, column=1, padx=10, pady=15)

        
                # Agregar un botón para guardar los cambios
                save_image = customtkinter.CTkImage(Image.open("images/guardar.png"), size=(26, 26))
                save_button = customtkinter.CTkButton(frame, text="Guardar", width=175, image= save_image, text_color= "black", fg_color="transparent", command=lambda: self.save_changes(evento_id))
                save_button.grid(row=6, column=1, padx=0, pady=0)
              
            except sqlite3.Error as e:
                # Si ocurre un error al conectar o insertar datos, se capturará aquí
                print("Error al conectar a la base de datos o insertar datos:", e)
  
    
  
    def save_changes(self, evento_id):
        # Obtener los valores modificados
        evento_id = evento_id
        evento = self.evento_entry.get()
        exponentes = self.exponentes_entry.get()  
        ubicacion = self.ubicacion_entry.get()  
        fecha = self.fecha_entry.get()
        hombres = self.hombres_entry.get()
        mujeres = self.mujeres_entry.get()
        

        # Realizar validaciones
        if not evento or not exponentes or not ubicacion or not fecha or not hombres or not mujeres:
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
        
        try:
            # Validar que los campos evento y exponentes solo contengan letras del abecedario
            if not self.validar_texto(evento):
                # Mostrar un mensaje de error
                tk.messagebox.showerror("Error", "El campo 'Evento' solo debe contener letras del abecedario.")
                # Hacer que la ventana de edición parpadee
                self.flash_edit_window()
                return
            
            if not self.validar_texto(exponentes):
                # Mostrar un mensaje de error
                tk.messagebox.showerror("Error", "El campo 'Exponentes' solo debe contener letras del abecedario.")
                # Hacer que la ventana de edición parpadee
                self.flash_edit_window()
                return
            
        except ValueError:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "Los campos 'Evento' y 'Exponentes' solo debe contener letras del abecedario.")

        # Actualizar la base de datos con los nuevos valores
        try:
            conn = sqlite3.connect("database/eventos.db")
            cursor = conn.cursor()
            
            # Construir y ejecutar la sentencia SQL UPDATE
            update_query = "UPDATE eventos SET nombre_evento = ?, nombres_exponentes = ?, lugar_evento = ?, fecha_evento = ?, asistentes_hombres = ?, asistentes_mujeres = ? WHERE id = ?"
            cursor.execute(update_query, (evento, exponentes, ubicacion, fecha, hombres, mujeres, evento_id))
            
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



    def validar_texto(self, texto):
        # Patrón de expresión regular que permite letras, espacios y apóstrofes (si es necesario)
        patron = r'^[A-Za-z\s\'À-ÖØ-öø-ÿ]+$'
        if not re.match(patron, texto):
            return False
        return True


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
            self.delete_window = customtkinter.CTkToplevel(self.root)
            self.delete_window.title("Eliminar Evento")
            self.delete_window.geometry("325x300")  # Establecer el tamaño de la ventana
            self.delete_window.resizable(False, False)
    
            # Personalizar el estilo de la ventana emergente
            self.delete_window.configure()  # Cambiar el fondo a blanco
    
            # Agregar un marco para un diseño más elegante
            frame = customtkinter.CTkFrame(self.delete_window, fg_color="transparent")
            frame.pack(expand=True, fill="both")
            
            self.evento_id=values[0]
            evento_image = customtkinter.CTkImage(Image.open("images/evento.png"), size=(26, 26))
            evento_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Evento:", image=evento_image, compound=tk.LEFT)
            evento_label.grid(row=0, column=0, padx=10, pady=15, sticky=tk.W)
            evento_value_label = customtkinter.CTkLabel(frame, text=values[1], font=('Calibri', 15), width=175, fg_color="white", corner_radius= 8)
            evento_value_label.grid(row=0, column=1, padx=10, pady=15)
    
            fecha_image = customtkinter.CTkImage(Image.open("images/fecha.png"), size=(26, 26))
            fecha_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Fecha:", image=fecha_image, compound=tk.LEFT)
            fecha_label.grid(row=3, column=0, padx=10, pady=15, sticky=tk.W)
            fecha_value_label = customtkinter.CTkLabel(frame, text=values[2], font=('Calibri', 15), width=175, fg_color="white", corner_radius= 8)
            fecha_value_label.grid(row=3, column=1, padx=10, pady=15)
    
            hombres_image = customtkinter.CTkImage(Image.open("images/hombre.png"), size=(26, 26))
            hombres_label = customtkinter.CTkLabel(frame, font=('Calibri', 15 ), text="  Hombres:", image=hombres_image, compound=tk.LEFT)
            hombres_label.grid(row=4, column=0, padx=10, pady=15, sticky=tk.W)
            hombres_value_label = customtkinter.CTkLabel(frame, text=values[4], font=('Calibri', 15), width=175, fg_color="white", corner_radius= 8)
            hombres_value_label.grid(row=4, column=1, padx=10, pady=15)
            
            mujeres_image = customtkinter.CTkImage(Image.open("images/mujer.png"), size=(26, 26))
            mujeres_label = customtkinter.CTkLabel(frame, font=('Calibri', 15), text="  Mujeres:", image=mujeres_image, compound=tk.LEFT)
            mujeres_label.grid(row=5, column=0, padx=10, pady=15, sticky=tk.W)
            mujeres_value_label = customtkinter.CTkLabel(frame, text=values[5], font=('Calibri', 15), width=175, fg_color="white", corner_radius= 8)
            mujeres_value_label.grid(row=5, column=1, padx=10, pady=15)
    
            # Agregar un botón para confirmar la eliminación
            delete_image = customtkinter.CTkImage(Image.open("images/borrar.png"), size=(26, 26))
            delete_button = customtkinter.CTkButton(frame, image= delete_image,  text_color= "black", text="Eliminar", fg_color="transparent", command=self.confirm_delete)
            delete_button.grid(row=6, column=1, padx=0, pady=0)

    def confirm_delete(self):

        evento_id = self.evento_id

        # Eliminar el evento de la base de datos
        try:
            conn = sqlite3.connect("database/eventos.db")
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

    def filter_button_clicked(self):
        # Obtener las fechas de inicio y finalización
        start_date = self.start_cal.get_date()
        end_date = self.end_cal.get_date()


        # Realizar la consulta SQL para obtener los registros en el rango de fechas
        try:
            conn = sqlite3.connect("database/eventos.db")
            cursor = conn.cursor()

            # Consulta SQL para obtener los registros entre las fechas dadas
            query = "SELECT id, nombre_evento,  nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos WHERE fecha_evento BETWEEN ? AND ? ORDER BY fecha_evento"
            cursor.execute(query, (start_date, end_date))

            # Obtener los registros resultantes
            eventos_filtrados = cursor.fetchall()

            # Cerrar la conexión a la base de datos
            conn.close()
            
            self.data= []

            # Llenar self.data con la información de eventos
            for evento in eventos_filtrados:
                self.data.append(evento)

            # Actualizar la tabla con los resultados filtrados
            self.show_page(self.current_page)

        except sqlite3.Error as e:
            # Si ocurre un error al conectar o ejecutar la consulta, se capturará aquí
            print("Error al conectar a la base de datos o ejecutar la consulta:", e)

    def clear_button_clicked(self):
        # Restablecer las fechas a sus valores originales
        self.start_cal.set_date(None)  # Reemplaza 'None' con la fecha inicial predeterminada si la tienes
        self.end_cal.set_date(None)  # Reemplaza 'None' con la fecha final predeterminada si la tienes
        
        self.fill_data_from_database()
        self.show_page(self.current_page)

    def recharge_button_clicked(self):
        # Restablecer las fechas a sus valores originales
        self.fill_data_from_database()
        self.show_page(self.current_page)


    def go_to_page(self):
        try:
            page = int(self.page_entry.get()) - 1  # Restamos 1 porque las páginas se cuentan desde 1
            if 0 <= page < self.total_pages:  # Asegurarse de que la página esté en el rango válido
                self.show_page(page)
            else:
                tk.messagebox.showerror("Error", "Número de página fuera de rango")
        except ValueError:
            tk.messagebox.showerror("Error", "Ingrese un número de página válido")

    def excel_button_clicked(self):
        # Preguntar al usuario la ubicación y nombre del archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile="EventAI")
        
        if file_path:
            try:
                # Crear un nuevo libro de trabajo de Excel
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                
                # Configurar los encabezados
                headers = ["Evento", "Fecha", "Asistentes", "Hombres", "Mujeres"]
                sheet.append(headers)
                
                # Agregar datos de la tabla a la hoja de Excel
                for row_data in self.data:
                    evento, fecha, hombres, mujeres = row_data[1], row_data[4], row_data[5], row_data[6]
                    asistentes = hombres + mujeres
                    row = [evento, fecha, asistentes, hombres, mujeres]
                    sheet.append(row)
                
                # Guardar el archivo de Excel en la ubicación proporcionada
                workbook.save(file_path)
                
                tk.messagebox.showinfo("Excel Exportado", f"Los datos se han exportado a '{file_path}'")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error al exportar a Excel: {str(e)}")

    def pdf_button_clicked(self):
        selected_item = self.table.selection()
        if selected_item:
            # Obtener los valores de la fila seleccionada
            selected_row = self.table.item(selected_item)
            values = selected_row['values']
            id = values[0]
            FileMaker.create_pdf_report(id)

    def open_photo_load_page(self):
        # Cuando se presione el botón "Agregar", crea una instancia de PhotoLoadPage
        self.root.iconify()
        photo_load_page = PhotoLoadPage(self, self.root) 
    

    def run(self):
        self.root.mainloop()



        """

        pdf_image = customtkinter.CTkImage(Image.open("images/pdf.png"), size=(26, 26))
        pdf_button = customtkinter.CTkButton(buttons_section_frame, image= pdf_image, text="  PDF", fg_color="transparent",  width=10)
        pdf_button.grid(row=0, column=1, padx=25, sticky=tk.W)
        pdf_button.configure(command=self.pdf_button_clicked)
        
        excel_image = customtkinter.CTkImage(Image.open("images/excel.png"), size=(26, 26))
        excel_button = customtkinter.CTkButton(buttons_section_frame, image=excel_image, text="  Excel", fg_color="transparent",  width=10)
        excel_button.grid(row=0, column=1, padx=75)
        excel_button.configure(command=self.excel_button_clicked)ç
"""