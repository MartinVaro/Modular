# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:46:25 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Tkinter")

        self.create_main_section()

    def create_main_section(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.create_buttons_section(main_frame)
        self.create_table_section(main_frame)
        self.create_navigation_section(main_frame)
        

    def create_table_section(self, main_frame):
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        table = ttk.Treeview(table_frame, columns=("Evento", "Fecha", "Asistentes", "Hombres", "Mujeres"), show="headings")
        table.heading("Evento", text="Evento")
        table.heading("Fecha", text="Fecha")
        table.heading("Asistentes", text="Asistentes")
        table.heading("Hombres", text="Hombres")
        table.heading("Mujeres", text="Mujeres")

        # Personalizar el tamaño de cada columna
        table.column("Evento", width=200)
        table.column("Fecha", width=100)
        table.column("Asistentes", width=100)
        table.column("Hombres", width=100)
        table.column("Mujeres", width=100)

        table.pack()

        for i in range(10):
            table.insert("", "end", values=(f"Evento {i+1}", f"Fecha {i+1}", f"Lugar {i+1}", f"Exponentes {i+1}", f"Asistentes {i+1}", f"Hombres {i+1}", f"Mujeres {i+1}"))

    def create_navigation_section(self, main_frame):
        navigation_frame = ttk.Frame(main_frame)
        navigation_frame.pack(side=tk.TOP, fill=tk.X, padx=50, pady=10)

        first_page_button = ttk.Button(navigation_frame, text="<<")
        first_page_button.pack(side=tk.LEFT, padx=10)

        prev_page_button = ttk.Button(navigation_frame, text="<")
        prev_page_button.pack(side=tk.LEFT, padx=10)

        page_label = ttk.Label(navigation_frame, text="Página:")
        page_label.pack(side=tk.LEFT, padx=10)

        page_entry = ttk.Entry(navigation_frame, width=5)
        page_entry.pack(side=tk.LEFT, padx=10)

        next_page_button = ttk.Button(navigation_frame, text=">")
        next_page_button.pack(side=tk.LEFT, padx=10)

        last_page_button = ttk.Button(navigation_frame, text=">>")
        last_page_button.pack(side=tk.LEFT, padx=10)

    def create_buttons_section(self, main_frame):
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        add_button = ttk.Button(button_frame, text="Agregar")
        add_button.pack(pady=10)

        generate_button = ttk.Button(button_frame, text="Generar")
        generate_button.pack(pady=10)

        filter_button = ttk.Button(button_frame, text="Filtrar")
        filter_button.pack(pady=10)
        
        add_button2 = ttk.Button(button_frame, text="Agregar")
        add_button2.pack(pady=10)

        generate_button2 = ttk.Button(button_frame, text="Generar")
        generate_button2.pack(pady=10)

        filter_button2 = ttk.Button(button_frame, text="Filtrar")
        filter_button2.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()




