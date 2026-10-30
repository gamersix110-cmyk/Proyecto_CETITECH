
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from conexion import conectar
from estilo import aplicar_tema, FUENTE_TITULO


def formato_hora(valor):
    # MySQL entrega las horas como timedelta (por ejemplo 9:00:00).
    # Se convierte a HH:MM para que siempre tenga dos dígitos.
    if hasattr(valor, "total_seconds"):
        total = int(valor.total_seconds())
        return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"

    return str(valor)[:5]


def abrir_turnos(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Chatino's Pizza - Turnos")
    ventana.geometry("850x560")
    ventana.minsize(700, 450)
    aplicar_tema(ventana)

    seleccion_id = None

    #  TITULO 
    ttk.Label(
        ventana,
        text="Administración de turnos",
        font=FUENTE_TITULO
    ).pack(pady=(15, 10))

    ttk.Label(
        ventana,
        text="Escribe los días del turno y las horas en formato HH:MM."
    ).pack(pady=3)

    #  FORMULARIO 
    formulario = ttk.LabelFrame(
        ventana,
        text="Datos del turno",
        padding=15
    )
    formulario.pack(fill="x", padx=20, pady=10)

    ttk.Label(formulario, text="Días del turno:").grid(
        row=0, column=0, padx=5, pady=8, sticky="w"
    )

    entry_dias = ttk.Entry(formulario, width=30)
    entry_dias.grid(
        row=0, column=1, padx=5, pady=8, sticky="ew"
    )

    ttk.Label(formulario, text="Hora de entrada:").grid(
        row=1, column=0, padx=5, pady=8, sticky="w"
    )

    entry_entrada = ttk.Entry(formulario, width=30)
    entry_entrada.grid(
        row=1, column=1, padx=5, pady=8, sticky="ew"
    )

    ttk.Label(formulario, text="Hora de salida:").grid(
        row=2, column=0, padx=5, pady=8, sticky="w"
    )

    entry_salida = ttk.Entry(formulario, width=30)
    entry_salida.grid(
        row=2, column=1, padx=5, pady=8, sticky="ew"
    )

    formulario.columnconfigure(1, weight=1)

    #  TABLA 
    columnas = (
        "ID_Turno",
        "Dias",
        "HoraIn",
        "HoraSa"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=12
    )

    tabla.heading("ID_Turno", text="ID")
    tabla.heading("Dias", text="Días del turno")
    tabla.heading("HoraIn", text="Hora de entrada")
    tabla.heading("HoraSa", text="Hora de salida")

    tabla.column("ID_Turno", width=70, anchor="center")
    tabla.column("Dias", width=240, anchor="center")
    tabla.column("HoraIn", width=180, anchor="center")
    tabla.column("HoraSa", width=180, anchor="center")

    tabla.pack(fill="both", expand=True, padx=20, pady=10)

    #  CONSULTAR TURNOS 
    def mostrar_turnos():
        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = conectar()

        if conexion is None:
            messagebox.showerror(
                "Conexión",
                "No se pudo conectar con la base de datos.",
                parent=ventana
            )
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT ID_Turno, Dias, HoraIn, HoraSa
                FROM turno
                ORDER BY ID_Turno
            """)

            for fila in cursor.fetchall():
                tabla.insert(
                    "",
                    "end",
                    values=(
                        fila[0],
                        fila[1],
                        formato_hora(fila[2]),
                        formato_hora(fila[3])
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron consultar los turnos:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  VALIDAR DATOS 
    def obtener_datos():
        dias = entry_dias.get().strip()
        entrada = entry_entrada.get().strip()
        salida = entry_salida.get().strip()

        if not dias:
            messagebox.showwarning(
                "Días del turno",
                "Escribe los días correspondientes al turno.",
                parent=ventana
            )
            return None

        if len(dias) > 20:
            messagebox.showwarning(
                "Validación",
                "El campo de días admite hasta 20 caracteres.",
                parent=ventana
            )
            return None

        try:
            hora_entrada = datetime.strptime(
                entrada, "%H:%M"
            ).time()

        except ValueError:
            messagebox.showwarning(
                "Hora de entrada",
                "Escribe una hora válida, por ejemplo 09:00.",
                parent=ventana
            )
            return None

        try:
            hora_salida = datetime.strptime(
                salida, "%H:%M"
            ).time()

        except ValueError:
            messagebox.showwarning(
                "Hora de salida",
                "Escribe una hora válida, por ejemplo 17:00.",
                parent=ventana
            )
            return None

        if hora_entrada == hora_salida:
            messagebox.showwarning(
                "Horario incorrecto",
                "La entrada y la salida no pueden ser iguales.",
                parent=ventana
            )
            return None

        return (
            dias,
            hora_entrada.strftime("%H:%M:%S"),
            hora_salida.strftime("%H:%M:%S")
        )

    #  LIMPIAR 
    def limpiar():
        nonlocal seleccion_id
        seleccion_id = None

        entry_dias.delete(0, tk.END)
        entry_entrada.delete(0, tk.END)
        entry_salida.delete(0, tk.END)

        seleccion = tabla.selection()

        if seleccion:
            tabla.selection_remove(seleccion)

        entry_dias.focus_set()

    #  REGISTRAR 
    def crear_turno():
        datos = obtener_datos()

        if datos is None:
            return

        conexion = conectar()

        if conexion is None:
            messagebox.showerror(
                "Conexión",
                "No se pudo conectar con la base de datos.",
                parent=ventana
            )
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO turno (Dias, HoraIn, HoraSa)
                VALUES (%s, %s, %s)
            """, datos)

            conexion.commit()

            messagebox.showinfo(
                "Registro correcto",
                "El turno se registró correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_turnos()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el turno:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  SELECCIONAR FILA 
    def seleccionar_fila(event=None):
        nonlocal seleccion_id

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")

        if not valores:
            return

        seleccion_id = int(valores[0])

        entry_dias.delete(0, tk.END)
        entry_dias.insert(0, valores[1])

        entry_entrada.delete(0, tk.END)
        entry_entrada.insert(0, valores[2])

        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, valores[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    #  ACTUALIZAR 
    def actualizar_turno():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona un turno de la tabla.",
                parent=ventana
            )
            return

        datos = obtener_datos()

        if datos is None:
            return

        conexion = conectar()

        if conexion is None:
            messagebox.showerror(
                "Conexión",
                "No se pudo conectar con la base de datos.",
                parent=ventana
            )
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE turno
                SET Dias = %s,
                    HoraIn = %s,
                    HoraSa = %s
                WHERE ID_Turno = %s
            """, (*datos, seleccion_id))

            conexion.commit()

            messagebox.showinfo(
                "Actualización correcta",
                "El turno se actualizó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_turnos()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el turno:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  ELIMINAR 
    def eliminar_turno():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona un turno de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Deseas eliminar el turno seleccionado?\n\n"
            "Si está relacionado con empleados, horarios o "
            "asistencias, MySQL podría impedir su eliminación.",
            parent=ventana
        )

        if not confirmar:
            return

        conexion = conectar()

        if conexion is None:
            messagebox.showerror(
                "Conexión",
                "No se pudo conectar con la base de datos.",
                parent=ventana
            )
            return

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM turno
                WHERE ID_Turno = %s
            """, (seleccion_id,))

            conexion.commit()

            messagebox.showinfo(
                "Eliminación correcta",
                "El turno se eliminó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_turnos()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "No se pudo eliminar",
                "Comprueba si el turno está relacionado con "
                "otros registros.\n\n"
                f"Detalle: {error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  BOTONES 
    botones = ttk.Frame(ventana, padding=10)
    botones.pack()

    ttk.Button(
        botones,
        text="Registrar",
        command=crear_turno
    ).grid(row=0, column=0, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Actualizar",
        command=actualizar_turno
    ).grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Eliminar",
        command=eliminar_turno
    ).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Limpiar",
        command=limpiar
    ).grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Actualizar tabla",
        command=mostrar_turnos
    ).grid(row=0, column=4, padx=5, pady=5)

    mostrar_turnos()