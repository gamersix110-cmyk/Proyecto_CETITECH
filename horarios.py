
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from conexion import conectar
from estilo import aplicar_tema, FUENTE_TITULO


def formato_hora(valor):
    if hasattr(valor, "total_seconds"):
        total = int(valor.total_seconds())
        return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"

    return str(valor)[:5]


def abrir_horarios(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Chatino's Pizza - Horarios")
    ventana.geometry("850x540")
    ventana.minsize(750, 460)
    aplicar_tema(ventana)

    seleccion_id = None
    turnos = {}
    horas_turno = {}

    #  TITULO 
    ttk.Label(
        ventana,
        text="Administración de horarios",
        font=FUENTE_TITULO
    ).pack(pady=(15, 10))

    ttk.Label(
        ventana,
        text="Elige el turno y escribe las horas en formato HH:MM."
    ).pack(pady=3)

    #  FORMULARIO 
    formulario = ttk.LabelFrame(
        ventana,
        text="Datos del horario",
        padding=15
    )
    formulario.pack(fill="x", padx=20, pady=10)

    ttk.Label(formulario, text="Turno:").grid(
        row=0, column=0, padx=5, pady=8, sticky="w"
    )

    combo_turno = ttk.Combobox(
        formulario, state="readonly", width=30
    )
    combo_turno.grid(
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
        "ID_Horario",
        "HoraIn",
        "HoraSa",
        "ID_Turno"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=10
    )

    tabla.heading("ID_Horario", text="ID")
    tabla.heading("HoraIn", text="Hora de entrada")
    tabla.heading("HoraSa", text="Hora de salida")
    tabla.heading("ID_Turno", text="ID del turno")

    tabla.column("ID_Horario", width=70, anchor="center")
    tabla.column("HoraIn", width=200, anchor="center")
    tabla.column("HoraSa", width=200, anchor="center")
    tabla.column("ID_Turno", width=160, anchor="center")

    tabla.pack(fill="both", expand=True, padx=20, pady=10)

    #  CARGAR TURNOS 
    def cargar_turnos():
        turnos.clear()
        horas_turno.clear()

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

            opciones = []

            for id_turno, dias, entrada, salida in cursor.fetchall():
                texto = (
                    f"{id_turno} - {dias} "
                    f"({formato_hora(entrada)} a {formato_hora(salida)})"
                )
                turnos[texto] = id_turno
                horas_turno[id_turno] = (
                    formato_hora(entrada),
                    formato_hora(salida)
                )
                opciones.append(texto)

            combo_turno["values"] = opciones

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los turnos:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  CONSULTAR HORARIOS 
    def mostrar_horarios():
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
                SELECT ID_Horario, HoraIn, HoraSa, ID_Turno
                FROM horario
                ORDER BY ID_Horario
            """)

            for fila in cursor.fetchall():
                tabla.insert(
                    "",
                    "end",
                    values=(
                        fila[0],
                        formato_hora(fila[1]),
                        formato_hora(fila[2]),
                        fila[3]
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron consultar los horarios:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  VALIDAR DATOS 
    def obtener_datos():
        if combo_turno.get() not in turnos:
            messagebox.showwarning(
                "Turno",
                "Selecciona un turno.",
                parent=ventana
            )
            return None

        entrada = entry_entrada.get().strip()
        salida = entry_salida.get().strip()

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
            hora_entrada.strftime("%H:%M:%S"),
            hora_salida.strftime("%H:%M:%S"),
            turnos[combo_turno.get()]
        )

    #  LIMPIAR 
    def limpiar():
        nonlocal seleccion_id
        seleccion_id = None

        combo_turno.set("")
        entry_entrada.delete(0, tk.END)
        entry_salida.delete(0, tk.END)

        seleccion = tabla.selection()

        if seleccion:
            tabla.selection_remove(seleccion)

        entry_entrada.focus_set()

    #  REGISTRAR 
    def crear_horario():
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
                INSERT INTO horario (HoraIn, HoraSa, ID_Turno)
                VALUES (%s, %s, %s)
            """, datos)

            conexion.commit()

            messagebox.showinfo(
                "Registro correcto",
                "El horario se registró correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_horarios()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el horario:\n{error}",
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

        combo_turno.set("")

        for opcion, id_turno in turnos.items():
            if str(id_turno) == str(valores[3]):
                combo_turno.set(opcion)
                break

        entry_entrada.delete(0, tk.END)
        entry_entrada.insert(0, valores[1])

        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, valores[2])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    #  AUTOCOMPLETAR CON EL TURNO 
    def elegir_turno(event=None):
        id_turno = turnos.get(combo_turno.get())

        if id_turno is None:
            return

        entrada, salida = horas_turno[id_turno]

        entry_entrada.delete(0, tk.END)
        entry_entrada.insert(0, entrada)

        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, salida)

    combo_turno.bind("<<ComboboxSelected>>", elegir_turno)

    #  ACTUALIZAR 
    def actualizar_horario():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona un horario de la tabla.",
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
                UPDATE horario
                SET HoraIn = %s,
                    HoraSa = %s,
                    ID_Turno = %s
                WHERE ID_Horario = %s
            """, (*datos, seleccion_id))

            conexion.commit()

            messagebox.showinfo(
                "Actualización correcta",
                "El horario se actualizó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_horarios()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el horario:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  ELIMINAR 
    def eliminar_horario():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona un horario de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Deseas eliminar el horario seleccionado?\n\n"
            "Si está asignado a algún empleado, MySQL podría "
            "impedir su eliminación.",
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
                DELETE FROM horario
                WHERE ID_Horario = %s
            """, (seleccion_id,))

            conexion.commit()

            messagebox.showinfo(
                "Eliminación correcta",
                "El horario se eliminó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_horarios()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "No se pudo eliminar",
                "Puede que el horario esté asignado a empleados.\n\n"
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
        command=crear_horario
    ).grid(row=0, column=0, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Actualizar",
        command=actualizar_horario
    ).grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Eliminar",
        command=eliminar_horario
    ).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Limpiar",
        command=limpiar
    ).grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Actualizar tabla",
        command=mostrar_horarios
    ).grid(row=0, column=4, padx=5, pady=5)

    # Al desplegar la lista se recargan los turnos por si hay nuevos
    combo_turno.configure(postcommand=cargar_turnos)

    cargar_turnos()
    mostrar_horarios()
