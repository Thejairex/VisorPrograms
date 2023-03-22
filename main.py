"""Importacion de modulos a utilizar"""
import tkinter as tk
from tkinter import ttk
import os
from pywinauto import Desktop
from windowsCapture import WindowCapture
import cv2 as cv
from PIL import ImageTk, Image
import threading
import pyautogui as bot
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Aplicacion(ttk.Frame):
    """

    Clase principal

    """
    def __init__(self, master=None):
        super().__init__(master)
        self.state_panel_control = False
        self.state_visor = False
        self.master = master

        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.widgets()

    def actualizar(self):
        """

        Renueva la lista de programas abiertos para ser insertados en la consola.

        """
        def filtro_nofuncional(windows):
            for x in windows:
                if x == 'Barra de tareas':
                    windows.remove(x)

                if x == '':
                    windows.remove(x)

                if 'Brave' in x:
                    windows.remove(x)
        windows_temp = Desktop(backend="uia").windows()
        self.txt_consola.config(state='normal')
        self.txt_consola.delete(1.0, 'end')
        self.txt_consola.insert(tk.END, "Estos son los programas que tenes abiertos: \n")
        self.btn_buscar.config(text = 'Actualizar')

        windows = [w.window_text() for w in windows_temp]
        filtro_nofuncional(windows)
        windows.append('Fullscreen')

        for window_text  in windows:
            self.txt_consola.insert(tk.END, f" • {window_text}\n")

        self.txt_consola.focus_set()
        self.cbb_window.config(values=windows)
        self.txt_consola.config(state='disabled')

    def visor(self):
        def ocultar():
            frm_visor.grid_forget()
            stop = True
            self.btn_visor.config(text = 'Iniciar', command=self.visor)
            self.state_visor = False
            self.frm_lista.grid(
                row = 0, column = 0, padx=(20, 10), pady=(20, 10), sticky="nsew"
                )
            
        def visualizar():
            programa = str(self.cbb_window.get())
            if programa != 'Fullscreen':
                wincap = WindowCapture(programa)
                while stop != True:
                    screenshot = wincap.get_screenshot()

                    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
                    screenshot = cv.resize(screenshot, (780, 400))
                    img_tk = ImageTk.PhotoImage(image=Image.fromarray(screenshot))

                    lbl_img.config(image=img_tk)
                    lbl_img.image = img_tk

            else:
                while stop != True:
                    frame = np.array(bot.screenshot())
                    # screenshot = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

                    screenshot = cv.resize(frame, (780, 400))
                    img_tk = ImageTk.PhotoImage(image=Image.fromarray(screenshot))

                    lbl_img.config(image=img_tk)
                    lbl_img.image = img_tk

        if not self.state_visor:
            #********* Control *********
            self.frm_lista.grid_forget()
            self.btn_visor.config(text = 'Apagar', command=ocultar)

            frm_visor = ttk.LabelFrame(self.master, text="Visor", padding=(20,10))
            frm_visor.grid(
                row = 0, column = 0, padx=(20, 10), pady=(10, 10), sticky="nsew"
            )

            frm_visor.columnconfigure(0, weight=1)
            frm_visor.rowconfigure(0, weight=1)

            lbl_img = ttk.Label(frm_visor)
            lbl_img.grid(
                row=0, column=0, padx=5, pady=10, sticky="nsew"
                )

            ttk.Button(frm_visor, text="Ocultar", command=ocultar).grid(
                row=1, column=0, padx=5, pady=10, sticky="nsew"
                )

            stop = False
            thread = threading.Thread(target=visualizar)
            thread.daemon = True
            thread.start()
            self.state_visor = True

    def widgets(self):
        """

        Diseño estetico de el programa con tkinter

        """
        def panel_control(event):
            if not self.state_panel_control:
                print('Se habri el panel de control')

                self.frm_panel_control.grid(
                    row = 0, column = 1, padx=(20, 10), pady=(20, 10), sticky="nsew"
                    )
                self.btn_visor = ttk.Button(self.frm_panel_control, text='Iniciar', command=self.visor)
                self.btn_visor.grid(
                    row=0, column=0, padx=5, pady=10, sticky="nsew"
                )

                self.state_panel_control = True

        self.frm_panel_control = ttk.LabelFrame(self.master, text='Panel', padding=(20,10))

        self.frm_lista = ttk.LabelFrame(self.master, text='Principal' ,padding=(20,10))
        self.frm_lista.grid(
            row = 0, column = 0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        self.btn_buscar = ttk.Button(self.frm_lista, text='Buscar', command=self.actualizar)
        self.btn_buscar.grid(
            row=0, column=0, padx=5, pady=10, sticky="nsew"
        )

        ttk.Label(self.frm_lista,text='Seleccionar programa:').grid(
            row=1, column=0, padx=5, pady=10, sticky="nsew"
            )

        self.cbb_window = ttk.Combobox(self.frm_lista, values=[], state='readonly')
        self.cbb_window.bind("<<ComboboxSelected>>", panel_control)
        self.cbb_window.grid(
            row=2, column=0, padx=5, pady=10, sticky="nsew"
            )

    #********** Textbox Consola ***********
        self.txt_consola = tk.Text(self.frm_lista, width=60, height=8, state='disabled')
        self.txt_consola.grid(
            row=3, column=0, padx=5, pady=10, sticky="nsew"
        )

        for row in range(10):
            self.txt_consola.grid_rowconfigure(row, weight=1)
        for col in range(50):
            self.txt_consola.grid_columnconfigure(col, weight=1)

        scrollbar_y = ttk.Scrollbar(
            self.frm_lista, orient="vertical", command=self.txt_consola.yview
            )
        scrollbar_y.grid(row=3, column=1, sticky="ns")
        self.txt_consola.config(yscrollcommand=scrollbar_y.set)


# •
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Capturadora")

    # Tema Azure descargado de 'https://github.com/rdbende/Azure-ttk-theme'
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = Aplicacion(root)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry(f"+{x_cordinate}+{y_cordinate-20}")

    root.mainloop()
