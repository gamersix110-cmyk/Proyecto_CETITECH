import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar
from personal import abrir_personal
from sucursales import abrir_sucursales
from turnos import abrir_turnos
from horarios import abrir_horarios
from asistencia import abrir_asistencia
from pagos import abrir_pagos
from estilo import (
    aplicar_tema, FUENTE_TITULO_GRANDE, FUENTE_SUBTITULO,
    TURQUESA, GRIS_AZUL
)


def abrir_modulo(nombre):
    if nombre == "Personal":
        abrir_personal(ventana)

    elif nombre == "Sucursales":
        abrir_sucursales(ventana)

    elif nombre == "Turnos":
        abrir_turnos(ventana)

    elif nombre == "Horarios":
        abrir_horarios(ventana)

    elif nombre == "Asistencia":
        abrir_asistencia(ventana)

    elif nombre == "Pago al personal":
        abrir_pagos(ventana)

    else:
        messagebox.showinfo(
            "Chatino's Pizza",
            f"El módulo de {nombre} se implementará después."
        )


def comprobar_conexion():
    conexion = conectar()

    if conexion:
        conexion.close()
        messagebox.showinfo(
            "Conexión",
            "Conexión con Chatino's Pizza correcta."
        )

ventana = tk.Tk()
ventana.title("Chatino's Pizza - Sistema de Personal")
ventana.geometry("780x520")
ventana.minsize(660, 460)
aplicar_tema(ventana)

estilo = ttk.Style()
estilo.configure(
    "Titulo.TLabel",
    font = FUENTE_TITULO_GRANDE,
    foreground = TURQUESA
)
estilo.configure("Subtitulo.TLabel", font = FUENTE_SUBTITULO)
estilo.configure("Modulo.TButton", font = ("Arial", 12), padding = 12)

contenedor = ttk.Frame(ventana, padding=25)
contenedor.pack(fill = "both", expand = True)

ttk.Label(
    contenedor,
    text="CHATINO'S PIZZA",
    style="Titulo.TLabel"
).pack(pady=(15, 0))

tk.Frame(contenedor, bg = GRIS_AZUL, width = 180, height = 3).pack(pady = 8)

ttk.Label(
    contenedor,
    text="Sistema de administración de personal",
    style="Subtitulo.TLabel"
).pack(pady=(0, 25))

modulos = [
    ("Personal", "Personal"),
    ("Sucursales", "Sucursales"),
    ("Turnos", "Turnos"),
    ("Horarios", "Horarios"),
    ("Control de asistencia", "Asistencia"),
    ("Pago al personal", "Pago al personal")
]

panel = ttk.Frame(contenedor)
panel.pack(fill="x", padx=30)

for i, (texto, modulo) in enumerate(modulos):
    boton = ttk.Button(
        panel,
        text = texto,
        style = "Modulo.TButton",
        command = lambda m = modulo: abrir_modulo(m)
    )
    if i == len(modulos) - 1 and len(modulos) % 2 == 1:
        columna = 1
    else:
        columna = (i % 2) * 2

    boton.grid(
        row = i // 2,
        column = columna,
        columnspan = 2,
        sticky = "ew",
        padx = 8,
        pady = 8
    )

for columna in range(4):
    panel.columnconfigure(columna, weight = 1)

ttk.Button(
    contenedor,
    text = "Probar conexión con MySQL",
    command = comprobar_conexion
).pack(side = "bottom", pady = (10, 0))

ventana.mainloop()