# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 11:34:20 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
import customtkinter, tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
import sqlite3
from filemaker.file_maker import FileMaker
import re

class ConferenceWindow:
    def __init__(self, Gender, App, App_window, num_men, num_women):
        self.App = App
        self.App_window = App_window
        self.Gender = Gender
        self.root = customtkinter.CTkToplevel()
        self.root.title("Registro de Evento")
        self.root.resizable(False, False)
        self.nuevo_id = 0
        #self.root.geometry("800x600")  # Tamaño de la ventana

        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)        
        
        self.num_men = num_men
        self.num_women = num_women
        
        main_frame = customtkinter.CTkFrame(self.root, fg_color=("transparent"))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear un Frame para los labels y entrys
        input_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear un Frame para los botones
        button_frame = customtkinter.CTkFrame(main_frame, fg_color=("transparent"))
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        
        
        evento_image = customtkinter.CTkImage(Image.open("images/evento.png"), size=(26, 26))
        evento_label = customtkinter.CTkLabel(input_frame, font=('Calibri', 15), text="  Evento:", image=evento_image, compound=tk.LEFT)
        evento_label.grid(row=0, column=0, padx=10, pady=15, sticky=tk.W)
        self.evento_entry = customtkinter.CTkEntry(input_frame, font=('Calibri', 15), width=175)
        self.evento_entry.grid(row=0, column=1, padx=10, pady=15)
        
        exponentes_image = customtkinter.CTkImage(Image.open("images/exponente.png"), size=(26, 26))
        exponentes_label = customtkinter.CTkLabel(input_frame, font=('Calibri', 15), text="  Exponentes:", image=exponentes_image, compound=tk.LEFT)
        exponentes_label.grid(row=1, column=0, padx=10, pady=15, sticky=tk.W)
        self.exponentes_entry = customtkinter.CTkEntry(input_frame, font=('Calibri', 15), width=175)
        self.exponentes_entry.grid(row=1, column=1, padx=10, pady=15)

        # Etiqueta y entrada para la ubicación
        ubicacion_image = customtkinter.CTkImage(Image.open("images/ubicacion.png"), size=(26, 26))
        ubicacion_label = customtkinter.CTkLabel(input_frame, font=('Calibri', 15), text="  Ubicación:", image=ubicacion_image, compound=tk.LEFT)
        ubicacion_label.grid(row=2, column=0, padx=10, pady=15, sticky=tk.W)
        self.ubicacion_entry = customtkinter.CTkEntry(input_frame, font=('Calibri', 15), width=175)
        self.ubicacion_entry.grid(row=2, column=1, padx=10, pady=15)

        
        fecha_image = customtkinter.CTkImage(Image.open("images/fecha.png"), size=(26, 26))
        fecha_label = customtkinter.CTkLabel(input_frame, font=('Calibri', 15), text="  Fecha:", image=fecha_image, compound=tk.LEFT)
        fecha_label.grid(row=3, column=0, padx=10, pady=15, sticky=tk.W)
        self.date_cal =DateEntry(input_frame, font=('Calibri', 12), date_pattern="yy/MM/dd")
        self.date_cal.grid(row=3, column=1, sticky="w",  padx=10, pady=10)
        
        # Botones para Guardar y regresar en el Frame de los botones
        save_image = customtkinter.CTkImage(Image.open("images/guardar.png"), size=(26, 26))
        save_button = customtkinter.CTkButton(
            button_frame, 
            text="Guardar", 
            width=15, 
            image= save_image, 
            text_color= "black", 
            fg_color="transparent", 
            command=self.create_button_clicked)
        save_button.pack(padx=10, pady=10, anchor=tk.W)
        
        back_image = customtkinter.CTkImage(Image.open("images/volver.png"), size=(26, 26))
        back_button = customtkinter.CTkButton(
            button_frame, 
            text="Regresar",
            width=20,
            command=self.go_back,
            image=back_image,
            text_color="black",
            fg_color="transparent"
        )
        back_button.pack(padx=10, pady=10, anchor=tk.W)
        

        
    def create_button_clicked(self):
        
        evento =  self.evento_entry.get()
        exponentes = self.exponentes_entry.get()
        ubicacion = self.ubicacion_entry.get()
        fecha = self.date_cal.get_date() 
        hombres = self.num_men  
        mujeres = self.num_women  

        # Realizar validaciones
        if not evento or not exponentes or not ubicacion or not fecha or not hombres or not mujeres:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "Ningún campo puede quedar vacío.")
    
            return
    
        try:
            # Verificar que la fecha tenga un formato válido
            fecha_str = fecha.strftime('%Y-%m-%d')
            datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        except ValueError:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "El formato de fecha debe ser DD-MM-YY.")
            return
    
        try:
            # Verificar que los campos "Hombres" y "Mujeres" contengan números enteros mayores o iguales a 0
            hombres = int(hombres)
            mujeres = int(mujeres)
            if hombres < 0 or mujeres < 0:
                # Mostrar un mensaje de error
                tk.messagebox.showerror("Error", "Los campos 'Hombres' y 'Mujeres' deben ser números enteros no negativos.")
                return
        except ValueError:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "Los campos 'Hombres' y 'Mujeres' deben ser números enteros no negativos.")
            return
        
        try:
            # Validar que los campos evento y exponentes solo contengan letras del abecedario
            if not self.validar_texto(evento):
                # Mostrar un mensaje de error
                tk.messagebox.showerror("Error", "El campo 'Evento' solo debe contener letras del abecedario.")
                return
            
            if not self.validar_texto(exponentes):
                # Mostrar un mensaje de error
                tk.messagebox.showerror("Error", "El campo 'Exponentes' solo debe contener letras del abecedario.")
                return
            
        except ValueError:
            # Mostrar un mensaje de error
            tk.messagebox.showerror("Error", "Los campos 'Evento' y 'Exponentes' solo debe contener letras del abecedario.")


        try:
            # Conectar a la base de datos
            #conn = sqlite3.connect("database/eventos.db")
            conn = sqlite3.connect("database/eventos.db")

            cursor = conn.cursor()

            # Realizar la inserción de datos en la tabla "eventos"
            cursor.execute("INSERT INTO eventos (nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres) VALUES (?, ?, ?, ?, ?, ?)",
                           (evento, exponentes, ubicacion, fecha, hombres, mujeres))
            
            # Obtener el ID del elemento recién insertado
            self.nuevo_id = cursor.lastrowid
            
            # Confirmar la inserción y cerrar la conexión a la base de datos
            conn.commit()
            conn.close()

            # Mostrar un mensaje de éxito
            #messagebox.showinfo("Éxito", "Dato guardado correctamente en la base de datos.")
            self.show_confirmation_window()

        except sqlite3.Error as e:
            # Si ocurre un error al conectar o insertar datos, se capturará aquí
            print("Error al conectar a la base de datos o insertar datos:", e)

    def validar_texto(self, texto):
        # Patrón de expresión regular que permite letras, espacios y apóstrofes (si es necesario)
        patron = r'^[A-Za-z\s\'À-ÖØ-öø-ÿ]+$'
        if not re.match(patron, texto):
            return False
        return True
    
 
    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Gender.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
    
    
    def show_confirmation_window(self):
        self.root.destroy()
        self.confirmation_window = customtkinter.CTkToplevel()
        self.confirmation_window.title("EventAI")

        # message label
        exit_image = customtkinter.CTkImage(Image.open("images/exito.png"), size=(26, 26))
        message_label = customtkinter.CTkLabel(self.confirmation_window,  font=('Calibri', 15), image=exit_image, text="  Datos almacenados correctamente",  compound=tk.LEFT)
        message_label.pack(padx=20, pady=20)
    

        option_label = customtkinter.CTkLabel(self.confirmation_window, font=('Calibri', 15), text="Crear archivo:")
        option_label.pack(padx=20, pady=10)
    
        # Add buttons

        pdf_image = customtkinter.CTkImage(Image.open("images/pdf.png"), size=(26, 26))
        pdf_button = customtkinter.CTkButton(self.confirmation_window, image= pdf_image,  text_color= "black", text="  PDF", fg_color="transparent",  width=10)
        pdf_button.pack(pady=10)
        pdf_button.configure(command=lambda: FileMaker.create_pdf_report(self.nuevo_id))
        
        excel_image = customtkinter.CTkImage(Image.open("images/excel.png"), size=(26, 26))
        excel_button = customtkinter.CTkButton(self.confirmation_window, image=excel_image,  text_color= "black", text="  Excel", fg_color="transparent",  width=10)
        excel_button.pack(pady=10)
        excel_button.configure(command=lambda: FileMaker.create_excel_report(self.nuevo_id))
        
    
        # Add a button to return to the main menu
        home_image = customtkinter.CTkImage(Image.open("images/home.png"), size=(26, 26))
        home_button = customtkinter.CTkButton(
            self.confirmation_window, 
            image=home_image,  
            fg_color="transparent", 
            text_color= "black", 
            text="Home", width=10, 
            command=self.return_to_main_menu)
        home_button.pack(pady=10)
        
        label = customtkinter.CTkLabel(self.confirmation_window, text="")
        label.pack(pady=5)
    
        # Show the confirmation window
        self.confirmation_window.mainloop()
    
    def return_to_main_menu(self):
        # Restaura la ventana principal
        self.App.fill_data_from_database()
        self.App.show_page(0)
        self.App_window.deiconify()
        # Cierra la ventana de PhotoLoadPage
        self.confirmation_window.destroy()
        self.Gender.destroy()
    

    def on_closing(self):
        # Restaura la ventana principal
        self.App_window.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Gender.destroy()