# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:39:22 2023

@author: akava
"""

import tkinter as tk
from interface.interface import App  # Importa tu clase de la interfaz desde el módulo

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = App(root)  # Pasa la ventana principal como argumento
    app.run()





"""
import tkinter as tk
from load.photo_load_page import PhotoLoadPage


root = tk.Tk()
app = PhotoLoadPage(root)
root.mainloop()
"""
