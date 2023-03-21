"""Importacion de modulos a utilizar"""
import tkinter as tk
from tkinter import ttk
import os
from pywinauto import Desktop


os.chdir(os.path.dirname(os.path.abspath(__file__)))



class Aplicacion(ttk.Frame):
    """

    Clase principal

    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.widgets()

    def actualizar(self):
        """

        Renueva la lista de programas abiertos para ser insertados en la consola.

        """
        windows = Desktop(backend="uia").windows()
        self.txt_consola.config(state='normal')
        self.txt_consola.insert(tk.END, "Estos son los programas que tenes abiertos: \n")
        self.btn_buscar.config(text='Actualizar')
        for window_text  in [w.window_text() for w in windows]:
            self.txt_consola.insert(tk.END, f" • {window_text}\n")

        self.txt_consola.config(state='disabled')

    def widgets(self):
        """

        Diseño estetico de el programa con tkinter

        """
        self.frm_lista = ttk.LabelFrame(self.master, text='Visor' ,padding=(20,10))
        self.frm_lista.grid(
            row = 0, column = 0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        self.btn_buscar = ttk.Button(self.frm_lista, text='Buscar', command=self.actualizar)
        self.btn_buscar.grid(
            row=0, column=0, padx=5, pady=10, sticky="nsew"
        )


        self.txt_consola = tk.Text(self.frm_lista, width=60, height=8, state='disabled')
        self.txt_consola.grid(
            row=1, column=0, padx=5, pady=10, sticky="nsew"
        )

        for row in range(10):
            self.txt_consola.grid_rowconfigure(row, weight=1)
        for col in range(50):
            self.txt_consola.grid_columnconfigure(col, weight=1)

        scrollbar_y = ttk.Scrollbar(
            self.frm_lista, orient="vertical", command=self.txt_consola.yview
            )
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        self.txt_consola.config(yscrollcommand=scrollbar_y.set)


# •
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Capturadora")
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = Aplicacion(root)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry(f"+{x_cordinate}+{y_cordinate-20}")

    root.mainloop()
