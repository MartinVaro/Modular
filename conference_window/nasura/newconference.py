# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 17:40:42 2023

@author: akava
"""
import tkinter as tk
from tkinter import ttk
import sqlite3

class ConferenceWindow:
    def __init__(self, root, num_men, num_women):
        self.root = root
        self.root.title("Registro de Evento")
        self.root.resizable(False, False)
        #self.root.geometry("800x600")  # Tamaño de la ventana
      
        
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

        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=3, column=1, sticky="w", pady=10)




        self.time_label = tk.Label(input_frame, text="Hora de inicio (hh:mm):")
        self.time_label.grid(row=4, column=0, sticky="w", pady=10)

        self.time_entry = tk.Entry(input_frame)
        self.time_entry.grid(row=4, column=1, sticky="w", pady=10)
      

        # Botones para continuar y regresar en el Frame de los botones
        continue_button = ttk.Button(button_frame, text="Generar Reporte", width=15, command=self.save_to_database)
        continue_button.pack(padx=10, pady=10, anchor=tk.E)

        back_button = ttk.Button(button_frame, text="Regresar", width=15)
        back_button.pack(padx=10, pady=10, anchor=tk.E)

    def save_to_database(self):
        # Obtener los valores ingresados por el usuario
        evento = self.name_entry.get()
        exponente = self.speakers_entry.get()
        lugar = self.location_entry.get()
        fecha = self.date_entry.get()
        hora = self.time_entry.get()
    
        # Crear una conexión a la base de datos utilizando un administrador de contexto
        with sqlite3.connect("eventos.db") as conn:
            cursor = conn.cursor()
    
            # Ejecutar un comando SQL para insertar los datos en la tabla
            cursor.execute("INSERT INTO eventos (nombre_evento, nombres_exponentes, lugar_evento, fecha_evento, hora_evento, asistentes_hombres, asistentes_mujeres) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (evento, exponente, lugar, fecha, hora, self.num_men, self.num_women))  # Agrega valores para asistentes_hombres y asistentes_mujeres, puedes cambiar estos valores según tus necesidades
    
            # Confirmar la transacción (no es necesario para SELECT, pero sí para INSERT, UPDATE, DELETE)
            conn.commit()


        print("Evento registrado en la base de datos")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConferenceWindow(root, 25, 55)
    root.mainloop()