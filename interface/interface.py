# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:46:25 2023

@author: akava
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
import tkinter as tk
#import tkcalendar as tkcal
from tkcalendar import DateEntry
import openpyxl
from tkinter import filedialog
from load.photo_load_page import PhotoLoadPage

"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from tkinter import filedialog, messagebox
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import matplotlib.pyplot as plt

"""

class App:
    def __init__(self, root):
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

        go_to_button = ttk.Button(navigation_frame, text="Ir a Página", command=self.go_to_page)
        go_to_button.pack(side=tk.LEFT, padx=10)


    def create_buttons_section(self, main_frame):
       
        buttons_section_frame = ttk.Frame(main_frame)
        buttons_section_frame.pack(side=tk.RIGHT)

        # Crear y colocar los botones en la cuadrícula
        add_button = ttk.Button(buttons_section_frame, text="Agregar")
        add_button.grid(row=0, column=0, padx=10, pady=10)
        add_button.grid_configure(columnspan=2)
        add_button.grid_configure(sticky="ew")
        add_button.config(command=self.open_photo_load_page)

        edit_button = ttk.Button(buttons_section_frame, text="Editar")
        edit_button.grid(row=2, column=0, padx=10, pady=10)
        edit_button.config(command=self.edit_button_clicked)

        pdf_button = ttk.Button(buttons_section_frame, text="PDF")
        pdf_button.grid(row=1, column=0, padx=10, pady=10)
        #pdf_button.config(command=self.pdf_button_clicked)
        

        excel_button = ttk.Button(buttons_section_frame, text="Excel")
        excel_button.grid(row=1, column=1, padx=5, pady=10)
        excel_button.config(command=self.excel_button_clicked)

        delete_button = ttk.Button(buttons_section_frame, text="Eliminar")
        delete_button.grid(row=2, column=1, padx=5, pady=10)
        delete_button.config(command=self.delete_button_clicked)

        filter_button = ttk.Button(buttons_section_frame, text="Filtrar")
        filter_button.grid(row=3, column=0, padx=10, pady=10)
        filter_button.config(command=self.filter_button_clicked)

        clean_button = ttk.Button(buttons_section_frame, text="Limpiar")
        clean_button.grid(row=3, column=1, padx=5, pady=10)
        clean_button.config(command=self.clear_button_clicked)

        # Crear un calendario de fecha de inicio
        start_date_label = ttk.Label(buttons_section_frame, text="Fecha inicio:")
        start_date_label.grid(row=4, column=0, padx=5, pady=10)
        self.start_cal = DateEntry(buttons_section_frame, width=8, date_pattern="dd/MM/yy")
        self.start_cal.grid(row=5, column=0, padx=5, pady=10)

        # Crear un calendario de fecha de finalización
        end_date_label = ttk.Label(buttons_section_frame, text="Fecha final:")
        end_date_label.grid(row=4, column=1, padx=5, pady=10)
        self.end_cal = DateEntry(buttons_section_frame, width=8, date_pattern="dd/MM/yy")
        self.end_cal.grid(row=5, column=1, padx=5, pady=10)
        
    def show_page(self, page):
        # Calcula el índice de inicio y fin para la página actual
        start = page * self.page_size
        end = (page + 1) * self.page_size
        self.total_pages = ((len(self.data) - 1) / self.page_size)+1

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
            conn = sqlite3.connect("database/eventos.db")
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
            query = "SELECT id, nombre_evento, fecha_evento, asistentes_hombres, asistentes_mujeres FROM eventos WHERE fecha_evento BETWEEN ? AND ? ORDER BY fecha_evento"
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
                    evento, fecha, hombres, mujeres = row_data[1], row_data[2], row_data[3], row_data[4]
                    asistentes = hombres + mujeres
                    row = [evento, fecha, asistentes, hombres, mujeres]
                    sheet.append(row)
                
                # Guardar el archivo de Excel en la ubicación proporcionada
                workbook.save(file_path)
                
                tk.messagebox.showinfo("Excel Exportado", f"Los datos se han exportado a '{file_path}'")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error al exportar a Excel: {str(e)}")


    def open_photo_load_page(self):
        # Cuando se presione el botón "Agregar", crea una instancia de PhotoLoadPage
        self.root.iconify()
        photo_load_page = PhotoLoadPage(self.root) 
    
       

    def run(self):
        self.root.mainloop()

"""

    def generate_pdf(self, selected_row):
        try:
            # Crear un archivo PDF con ReportLab
            pdf_file = "evento.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
    
            # Extraer los valores de la fila seleccionada
            id_evento, evento, fecha, asistentes, hombres, mujeres = selected_row
    
            # Escribir la información en el PDF
            c.drawString(100, 750, "ID del Evento: " + str(id_evento))
            c.drawString(100, 730, "Evento: " + evento)
            c.drawString(100, 710, "Fecha: " + fecha)
            c.drawString(100, 690, "Asistentes: " + str(asistentes))
            c.drawString(100, 670, "Hombres: " + str(hombres))
            c.drawString(100, 650, "Mujeres: " + str(mujeres))
    
            # Guardar y cerrar el archivo PDF
            c.save()
    
            messagebox.showinfo("PDF Generado", f"El archivo PDF '{pdf_file}' se ha generado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")
    
    # Luego, en tu función de botón PDF, llama a esta función con la fila seleccionada:
    def pdf_button_clicked(self):
        selected_item = self.table.selection()
        if selected_item:
            selected_row = self.table.item(selected_item)['values']
            self.generate_pdf(selected_row)
        else:
            messagebox.showwarning("Advertencia", "Selecciona una fila antes de generar el PDF.")


    def generate_pdf_from_data(self, selected_row):
        try:
            
            # Extraer los valores de la fila seleccionada
            id_evento, evento, fecha, asistentes, hombres, mujeres = selected_row
            
            # Crear un archivo PDF con ReportLab
            pdf_file =evento.replace(" ", "_").lower() + ".pdf"
            doc = SimpleDocTemplate(pdf_file, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=54, bottomMargin=54)
    
            # Crear un objeto Story para el contenido del PDF
            story = []
    
            # Estilos de texto
            styles = getSampleStyleSheet()
            title_style = styles["Title"]
            normal_style = styles["Normal"]
    
            # Agregar el título
            title = "Informe de Evento"
            story.append(Paragraph(title, title_style))
    
            # Agregar información del evento
            event_info = [
                ["Evento:", conference_name],
                ["Exponente:", speakers_names],
                ["Lugar del evento:", location],
                ["Total de asistentes:", str(num_men + num_women)],
                ["Fecha del evento:", date],
                ["Hora de inicio:", time],
            ]
    
            # Crear una tabla para mostrar la información del evento
            event_table = Table(event_info, colWidths=[150, 200])
            event_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente negrita para la primera fila
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 12),  # Fuente tamaño 12 para las otras celdas
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación a la izquierda
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical al centro
            ]))
    
            # Agregar la tabla al Story
            story.append(event_table)
    
            # Crear una gráfica de pastel con Matplotlib
            data = [num_men, num_women]
            labels = ["Hombres", "Mujeres"]
            colors = ['#4C8FD6', '#FF8EB0']
    
            plt.figure(figsize=(6, 6))  # Aumentar el tamaño de la gráfica
            wedges, texts, autotexts = plt.pie(data, labels=labels, colors=colors, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * sum(data) / 100, p))
            plt.title('Distribución de Asistentes', fontsize=14, fontweight='bold')
    
            for autotext in autotexts:
                autotext.set_fontsize(12)  # Tamaño de fuente para los porcentajes
                autotext.set_color('white')  # Color de fuente en blanco
    
            # Guardar la gráfica en un objeto BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
    
            # Crear la imagen a partir del contenido del objeto BytesIO
            pie_chart_image = Image(buffer, width=350, height=350)
    
            # Agregar la imagen al Story
            story.append(pie_chart_image)
    
            # Construir el PDF
            doc.build(story)
    
            messagebox.showinfo("PDF Generado", f"El archivo PDF '{pdf_file}' se ha generado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    
"""



"""

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
"""



