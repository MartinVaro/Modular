# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:39:22 2023

@author: akava
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter
from interface.interface import App 
import sqlite3

try:
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('database/eventos.db')

    # Crear un cursor para ejecutar comandos SQL
    cursor = conn.cursor()

    # Crear la tabla "eventos"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_evento TEXT NOT NULL,
            nombres_exponentes TEXT,
            lugar_evento TEXT,
            fecha_evento DATE NOT NULL,
            asistentes_hombres INTEGER NOT NULL,
            asistentes_mujeres INTEGER NOT NULL
        )
    ''')

    # Guardar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión
    conn.close()

    if __name__ == "__main__":
        root = customtkinter.CTk()
        root.resizable(False, False)
        app = App(root)  
        app.run()

except sqlite3.Error as e:
    # Muestra una alerta en caso de error
    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

