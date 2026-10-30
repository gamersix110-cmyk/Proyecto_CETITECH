
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


def a_minutos(valor):
    if hasattr(valor, "total_seconds"):
        return int(valor.total_seconds()) // 60

    horas, minutos = str(valor).split(":")[:2]
    return int(horas) * 60 + int(minutos)


def es_retardo(minutos_entrada, minutos_turno):
    diferencia = (minutos_entrada - minutos_turno) % 1440
    return 15 < diferencia <= 720


def abrir_asistencia(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Chatino's Pizza - Asistencia")
    ventana.geometry("850x570")
    ventana.minsize(750, 480)
    aplicar_tema(ventana)

    seleccion_id = None

    #  TITULO 
    ttk.Label(
        ventana,
        text="Control de asistencia",
        font=FUENTE_TITULO
    ).pack(pady=12)

    #  FORMULARIO 
    formulario = ttk.LabelFrame(
        ventana,
        text="Datos de asistencia",
        padding=12
    )
    formulario.pack(fill="x", padx=20, pady=8)

    ttk.Label(formulario, text="Turno:").grid(
        row=0, column=0, padx=5, pady=7, sticky="w"
    )

    combo_turno = ttk.Combobox(
        formulario, state="readonly", width=30
    )
    combo_turno.grid(
        row=0, column=1, padx=5, pady=7, sticky="ew"
    )

    ttk.Label(
        formulario, text="Hora de entrada (HH:MM):"
    ).grid(row=1, column=0, padx=5, pady=7, sticky="w")

    entry_entrada = ttk.Entry(formulario, width=32)
    entry_entrada.grid(
        row=1, column=1, padx=5, pady=7, sticky="ew"
    )

    ttk.Label(
        formulario, text="Hora de salida (HH:MM):"
    ).grid(row=2, column=0, padx=5, pady=7, sticky="w")

    entry_salida = ttk.Entry(formulario, width=32)
    entry_salida.grid(
        row=2, column=1, padx=5, pady=7, sticky="ew"
    )

    # El retardo se calcula solo: es de solo lectura
    texto_retardo = tk.StringVar(value="Falso")

    ttk.Label(formulario, text="Retardo:").grid(
        row=3, column=0, padx=5, pady=7, sticky="w"
    )

    ttk.Label(formulario, textvariable=texto_retardo).grid(
        row=3, column=1, padx=5, pady=7, sticky="w"
    )

    formulario.columnconfigure(1, weight=1)

    #  TABLA 
    columnas = (
        "ID_Asistencia",
        "HoraIn",
        "HoraSa",
        "ID_Turno",
        "Retardo"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=10
    )

    encabezados = {
        "ID_Asistencia": "ID",
        "HoraIn": "Entrada",
        "HoraSa": "Salida",
        "ID_Turno": "ID del turno",
        "Retardo": "Retardo"
    }

    for columna, titulo in encabezados.items():
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=140, anchor="center")

    tabla.pack(fill="both", expand=True, padx=20, pady=8)

    #  CARGAR TURNOS 
    turnos = {}
    horas_turno = {}

    def cargar_turnos():
        combo_turno.set("")
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
                ORDER BY Dias, HoraIn
            """)

            opciones = []

            for id_turno, dias, entrada, salida in cursor.fetchall():
                texto = (
                    f"{id_turno} - {dias} "
                    f"({formato_hora(entrada)} a {formato_hora(salida)})"
                )
                turnos[texto] = id_turno
                horas_turno[id_turno] = (
                    a_minutos(entrada),
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

    #  CONSULTAR ASISTENCIAS 
    def mostrar_asistencias():
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
                SELECT ID_Asistencia, HoraIn, HoraSa,
                       ID_Turno, Retardo
                FROM asistencia
                ORDER BY ID_Asistencia DESC
            """)

            for fila in cursor.fetchall():
                tabla.insert(
                    "",
                    "end",
                    values=(
                        fila[0],
                        formato_hora(fila[1]),
                        formato_hora(fila[2]),
                        fila[3],
                        "Verdadero" if fila[4] else "Falso"
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron consultar las asistencias:\n{error}",
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

        if not salida:
            messagebox.showwarning(
                "Hora de salida",
                "Escribe la hora de salida.",
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

        id_turno = turnos[combo_turno.get()]
        retardo = 1 if calcular_retardo() else 0

        return (
            hora_entrada.strftime("%H:%M:%S"),
            hora_salida.strftime("%H:%M:%S"),
            id_turno,
            retardo
        )

    #  LIMPIAR 
    def limpiar():
        nonlocal seleccion_id
        seleccion_id = None

        combo_turno.set("")
        entry_entrada.delete(0, tk.END)
        entry_salida.delete(0, tk.END)
        texto_retardo.set("Falso")

        seleccion = tabla.selection()
        if seleccion:
            tabla.selection_remove(seleccion)

    #  REGISTRAR 
    def registrar():
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
                INSERT INTO asistencia
                    (HoraIn, HoraSa, ID_Turno, Retardo)
                VALUES (%s, %s, %s, %s)
            """, datos)

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "La asistencia se registró correctamente.\n\n"
                "Importante: la tabla actual no guarda el ID "
                "del empleado ni la fecha de asistencia.",
                parent=ventana
            )

            limpiar()
            mostrar_asistencias()

        except Exception as error:
            conexion.rollback()
            messagebox.showerror(
                "Error",
                f"No se pudo registrar la asistencia:\n{error}",
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
        entry_entrada.insert(0, str(valores[1])[:5])

        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, str(valores[2])[:5])

        texto_retardo.set(valores[4])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    #  RETARDO AUTOMATICO 
    def calcular_retardo(event=None):
        retardo = False
        id_turno = turnos.get(combo_turno.get())

        if id_turno is not None:
            try:
                hora = datetime.strptime(
                    entry_entrada.get().strip(), "%H:%M"
                )
                retardo = es_retardo(
                    hora.hour * 60 + hora.minute,
                    horas_turno[id_turno][0]
                )
            except ValueError:
                pass

        texto_retardo.set("Verdadero" if retardo else "Falso")
        return retardo

    #  AUTOCOMPLETAR CON EL TURNO 
    def elegir_turno(event=None):
        id_turno = turnos.get(combo_turno.get())

        if id_turno is None:
            return

        _, entrada, salida = horas_turno[id_turno]

        entry_entrada.delete(0, tk.END)
        entry_entrada.insert(0, entrada)

        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, salida)

        calcular_retardo()

    combo_turno.bind("<<ComboboxSelected>>", elegir_turno)
    entry_entrada.bind("<KeyRelease>", calcular_retardo)

    #  ACTUALIZAR 
    def actualizar():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección",
                "Selecciona una asistencia de la tabla.",
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
                UPDATE asistencia
                SET HoraIn = %s,
                    HoraSa = %s,
                    ID_Turno = %s,
                    Retardo = %s
                WHERE ID_Asistencia = %s
            """, (*datos, seleccion_id))

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "La asistencia se actualizó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_asistencias()

        except Exception as error:
            conexion.rollback()
            messagebox.showerror(
                "Error",
                f"No se pudo actualizar la asistencia:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  ELIMINAR 
    def eliminar():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección",
                "Selecciona una asistencia de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Deseas eliminar esta asistencia?",
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
                DELETE FROM asistencia
                WHERE ID_Asistencia = %s
            """, (seleccion_id,))

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "La asistencia se eliminó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_asistencias()

        except Exception as error:
            conexion.rollback()
            messagebox.showerror(
                "Error",
                f"No se pudo eliminar la asistencia:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  BOTONES 
    botones = ttk.Frame(ventana, padding=8)
    botones.pack()

    ttk.Button(
        botones, text="Registrar", command=registrar
    ).grid(row=0, column=0, padx=4, pady=5)

    ttk.Button(
        botones, text="Actualizar", command=actualizar
    ).grid(row=0, column=1, padx=4, pady=5)

    ttk.Button(
        botones, text="Eliminar", command=eliminar
    ).grid(row=0, column=2, padx=4, pady=5)

    ttk.Button(
        botones, text="Limpiar", command=limpiar
    ).grid(row=0, column=3, padx=4, pady=5)

    ttk.Button(
        botones, text="Recargar", command=mostrar_asistencias
    ).grid(row=0, column=4, padx=4, pady=5)

    cargar_turnos()
    mostrar_asistencias()