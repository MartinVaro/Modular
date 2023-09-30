# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 11:34:20 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from filemaker.file_maker import FileMaker

class ConferenceWindow:
    def __init__(self, Gender, App, num_men, num_women):
        self.App = App
        self.Gender = Gender
        self.root = tk.Toplevel()
        self.root.title("Registro de Evento")
        self.root.resizable(False, False)
        self.nuevo_id = 0
        #self.root.geometry("800x600")  # Tamaño de la ventana

        # Configurar el evento de cierre de la ventana secundaria
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)        
        
        self.num_men = num_men
        self.num_women = num_women
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear un Frame para los labels y entrys
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear un Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        
        self.name_label = tk.Label(input_frame, text="Evento o conferencia:")
        self.name_label.grid(row=0, column=0, sticky="w", pady=10)
        self.name_entry = tk.Entry(input_frame, width=50)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=10)

        self.speakers_label = tk.Label(input_frame, text="Nombre del exponente:")
        self.speakers_label.grid(row=1, column=0, sticky="w", pady=10)
        self.speakers_entry = tk.Entry(input_frame, width=50)
        self.speakers_entry.grid(row=1, column=1, sticky="w", pady=10)

        self.location_label = tk.Label(input_frame, text="Localización del evento:")
        self.location_label.grid(row=2, column=0, sticky="w", pady=10)
        self.location_entry = tk.Entry(input_frame, width=50)
        self.location_entry.grid(row=2, column=1, sticky="w", pady=10)

        self.date_label = tk.Label(input_frame, text="Fecha del evento:")
        self.date_label.grid(row=3, column=0, sticky="w", pady=10)

        self.date_cal =DateEntry(input_frame, date_pattern="yy/MM/dd")
        self.date_cal.grid(row=3, column=1, sticky="w", pady=10)
        
        # Botones para Guardar y regresar en el Frame de los botones
        save_button = ttk.Button(button_frame, text="Guardar", command=self.create_button_clicked, width=15)
        save_button.pack(padx=10, pady=10, anchor=tk.E)
        
        back_button = ttk.Button(button_frame, text="Regresar", command=self.go_back, width=15)
        back_button.pack(padx=10, pady=10, anchor=tk.E)
 
        
    def create_button_clicked(self):
        
        conference_name = self.name_entry.get()
        speakers_names = self.speakers_entry.get()
        location = self.location_entry.get()
        date = self.date_cal.get_date() 
        asistentes_hombres = self.num_men  
        asistentes_mujeres = self.num_women  

        missing_fields = []
    
        if not conference_name:
            missing_fields.append("Nombre del evento o conferencia")
        if not speakers_names:
            missing_fields.append("Nombre del exponente")
        if not location:
            missing_fields.append("Localización del evento")
        if not date:
            missing_fields.append("Fecha del evento")
        
        if missing_fields:
            # Mostrar un mensaje de error si hay campos obligatorios vacíos
            messagebox.showerror("Campos Faltantes", f"Los siguientes campos son obligatorios:\n\n{', '.join(missing_fields)}")
        else:
            try:
                # Conectar a la base de datos
                #conn = sqlite3.connect("database/eventos.db")
                conn = sqlite3.connect("database/eventos.db")
    
                cursor = conn.cursor()
    
                # Realizar la inserción de datos en la tabla "eventos"
                cursor.execute("INSERT INTO eventos (nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, asistentes_hombres, asistentes_mujeres) VALUES (?, ?, ?, ?, ?, ?)",
                               (conference_name, speakers_names, location, date, asistentes_hombres, asistentes_mujeres))
                
                
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
 
    def go_back(self):
        # Hacer que la ventana anterior vuelva a ser visible
        self.Gender.deiconify()
        # Cerrar la ventana actual
        self.root.destroy()
    
    
    def show_confirmation_window(self):
        self.root.destroy()
        self.confirmation_window = tk.Toplevel()
        self.confirmation_window.title("EventAI")

    
        # Add a message label
        message_label = ttk.Label(self.confirmation_window, text="Datos almacenados correctamente.")
        message_label.pack(padx=20, pady=20)
    
        # Add a label for the buttons
        option_label = ttk.Label(self.confirmation_window, text="Crear archivo:")
        option_label.pack(padx=20, pady=10)
    
        # Add buttons
       
        pdf_button = ttk.Button(self.confirmation_window, text="PDF", command=lambda: FileMaker.create_pdf_report(self.nuevo_id))
        pdf_button.pack(pady=10)
        
        excel_button = ttk.Button(self.confirmation_window, text="Excel", command=lambda: FileMaker.create_excel_report(self.nuevo_id))
        excel_button.pack(pady=10)
    
        tk.Label(self.confirmation_window, text="").pack()
    
        # Add a button to return to the main menu
        return_to_main_menu_button = ttk.Button(self.confirmation_window, text="Menú principal", command=self.return_to_main_menu)
        return_to_main_menu_button.pack(pady=10)
    
        # Show the confirmation window
        self.confirmation_window.mainloop()
    
    def return_to_main_menu(self):
        # Restaura la ventana principal
        self.App.deiconify()
        # Cierra la ventana de PhotoLoadPage
        self.confirmation_window.destroy()
        self.Gender.destroy()
    

    def on_closing(self):
        # Restaura la ventana principal
        self.App.deiconify()
        
        # Cierra la ventana de PhotoLoadPage
        self.root.destroy()
        self.Gender.destroy()