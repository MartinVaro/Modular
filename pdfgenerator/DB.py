# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 17:53:41 2023

@author: akava
"""
"""
import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('eventos.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear la tabla "eventos" con los atributos especificados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_evento TEXT NOT NULL,
        nombres_exponentes TEXT,
        lugar_evento TEXT,
        fecha_evento DATE NOT NULL,
        hora_evento TIME,
        asistentes_hombres INTEGER NOT NULL,
        asistentes_mujeres INTEGER NOT NULL
    )
''')

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
conn.close()
"""

import sqlite3

# Intentar conectar a la base de datos SQLite
try:
    conn = sqlite3.connect("eventos.db")
    cursor = conn.cursor()

    # Realizar una consulta SQL para obtener los registros de la tabla "eventos"
    cursor.execute("SELECT nombre_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos")

    # Obtener todos los registros
    eventos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conn.close()

    # Si llegamos aquí, la consulta se ejecutó con éxito
    print("Consulta exitosa.")

    # Puedes trabajar con los datos obtenidos en la variable "eventos"
except sqlite3.Error as e:
    # Si ocurre un error al conectar o ejecutar la consulta, se capturará aquí
    print("Error al ejecutar la consulta:", e)
