
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
from conexion import conectar
from estilo import aplicar_tema, FUENTE_TITULO


def formato_hora(valor):
    # MySQL entrega las horas como timedelta (por ejemplo 9:00:00).
    # Se convierte a HH:MM para que siempre tenga dos dígitos.
    if hasattr(valor, "total_seconds"):
        total = int(valor.total_seconds())
        return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"

    return str(valor)[:5]


def abrir_personal(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Chatino's Pizza - Personal")
    ventana.geometry("1040x640")
    ventana.minsize(900, 560)
    aplicar_tema(ventana)

    seleccion_id = None
    sucursales = {}
    horarios = {}
    turnos = {}

    #  TITULO 
    ttk.Label(
        ventana,
        text="Administración de personal",
        font=FUENTE_TITULO
    ).pack(pady=(12, 5))

    #  FORMULARIO 
    formulario = ttk.LabelFrame(
        ventana,
        text="Datos del empleado",
        padding=12
    )
    formulario.pack(fill="x", padx=15, pady=8)

    campos = [
        ("Nombre", "nombre"),
        ("Apellidos", "apellidos"),
        ("Edad", "edad"),
        ("Teléfono", "telefono"),
        ("Colonia", "colonia"),
        ("Dirección", "direccion"),
        ("Salario", "salario")
    ]

    entradas = {}

    for i, (etiqueta, clave) in enumerate(campos):
        fila = i // 4
        columna = (i % 4) * 2

        ttk.Label(
            formulario, text=etiqueta + ":"
        ).grid(
            row=fila, column=columna,
            padx=5, pady=6, sticky="w"
        )

        entrada = ttk.Entry(formulario, width=20)
        entrada.grid(
            row=fila, column=columna + 1,
            padx=5, pady=6, sticky="ew"
        )

        entradas[clave] = entrada

    #  LISTAS DESPLEGABLES 
    ttk.Label(formulario, text="Sucursal:").grid(
        row=2, column=0, padx=5, pady=6, sticky="w"
    )

    combo_sucursal = ttk.Combobox(
        formulario, state="readonly", width=18
    )
    combo_sucursal.grid(
        row=2, column=1, padx=5, pady=6, sticky="ew"
    )

    ttk.Label(formulario, text="Horario:").grid(
        row=2, column=2, padx=5, pady=6, sticky="w"
    )

    combo_horario = ttk.Combobox(
        formulario, state="readonly", width=18
    )
    combo_horario.grid(
        row=2, column=3, padx=5, pady=6, sticky="ew"
    )

    ttk.Label(formulario, text="Turno:").grid(
        row=3, column=0, padx=5, pady=6, sticky="w"
    )

    combo_turno = ttk.Combobox(
        formulario, state="readonly", width=18
    )
    combo_turno.grid(
        row=3, column=1, padx=5, pady=6, sticky="ew"
    )

    for columna in (1, 3, 5, 7):
        formulario.columnconfigure(columna, weight=1)

    #  TABLA 
    columnas = (
        "ID_Personal",
        "Nombre",
        "Apellidos",
        "Edad",
        "Telefono",
        "Colonia",
        "Direccion",
        "Salario",
        "Sucursal",
        "Horario",
        "Turno"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=12
    )

    encabezados = {
        "ID_Personal": "ID",
        "Nombre": "Nombre",
        "Apellidos": "Apellidos",
        "Edad": "Edad",
        "Telefono": "Teléfono",
        "Colonia": "Colonia",
        "Direccion": "Dirección",
        "Salario": "Salario",
        "Sucursal": "ID sucursal",
        "Horario": "ID horario",
        "Turno": "ID turno"
    }

    anchos = {
        "ID_Personal": 50,
        "Nombre": 110,
        "Apellidos": 120,
        "Edad": 45,
        "Telefono": 100,
        "Colonia": 100,
        "Direccion": 140,
        "Salario": 85,
        "Sucursal": 80,
        "Horario": 80,
        "Turno": 70
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(
            columna,
            width=anchos[columna],
            anchor="center"
        )

    tabla.pack(
        fill="both", expand=True, padx=15, pady=8
    )

    #  CARGAR SUCURSALES, HORARIOS Y TURNOS 
    def cargar_listas():
        nonlocal sucursales, horarios, turnos

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

            # Sucursales
            cursor.execute("""
                SELECT ID_Sucursal, Nombre
                FROM sucursal
                ORDER BY ID_Sucursal
            """)

            sucursales = {}

            for id_sucursal, nombre in cursor.fetchall():
                etiqueta = f"{id_sucursal} - {nombre}"
                sucursales[etiqueta] = id_sucursal

            combo_sucursal["values"] = list(sucursales.keys())

            # Horarios
            cursor.execute("""
                SELECT ID_Horario, HoraIn, HoraSa, ID_Turno
                FROM horario
                ORDER BY ID_Horario
            """)

            horarios = {}

            for id_horario, entrada, salida, id_turno in cursor.fetchall():
                etiqueta = (
                    f"{id_horario} - "
                    f"{formato_hora(entrada)} a {formato_hora(salida)} "
                    f"(Turno {id_turno})"
                )
                horarios[etiqueta] = id_horario

            combo_horario["values"] = list(horarios.keys())

            # Turnos
            cursor.execute("""
                SELECT ID_Turno, Dias, HoraIn, HoraSa
                FROM turno
                ORDER BY ID_Turno
            """)

            turnos = {}

            for id_turno, dias, entrada, salida in cursor.fetchall():
                etiqueta = (
                    f"{id_turno} - {dias} "
                    f"({formato_hora(entrada)} a {formato_hora(salida)})"
                )
                turnos[etiqueta] = id_turno

            combo_turno["values"] = list(turnos.keys())

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las listas:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    # Al desplegar la lista de horarios se recargan por si hay nuevos
    combo_horario.configure(postcommand=cargar_listas)

    #  MOSTRAR PERSONAL 
    def mostrar_personal():
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
                SELECT
                    ID_Personal,
                    Nombre,
                    `ApePat/Mat`,
                    Edad,
                    `Teléfono`,
                    Colonia,
                    `Dirección`,
                    Salario,
                    ID_Sucursal,
                    ID_Horario,
                    ID_Turno
                FROM personal
                ORDER BY ID_Personal
            """)

            for fila in cursor.fetchall():
                tabla.insert("", "end", values=fila)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo consultar el personal:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  VALIDAR DATOS 
    def obtener_datos():
        datos = {
            clave: entradas[clave].get().strip()
            for clave in entradas
        }

        if not datos["nombre"] or not datos["apellidos"]:
            messagebox.showwarning(
                "Validación",
                "Escribe el nombre y los apellidos del empleado.",
                parent=ventana
            )
            return None

        if len(datos["nombre"]) > 50 or len(datos["apellidos"]) > 50:
            messagebox.showwarning(
                "Validación",
                "El nombre y los apellidos admiten hasta 50 caracteres.",
                parent=ventana
            )
            return None

        if not datos["edad"].isdigit() or int(datos["edad"]) <= 0:
            messagebox.showwarning(
                "Edad",
                "Escribe una edad válida mayor que cero.",
                parent=ventana
            )
            return None

        telefono = datos["telefono"]

        if not telefono.isdigit() or len(telefono) > 10:
            messagebox.showwarning(
                "Teléfono",
                "Escribe un teléfono de hasta 10 dígitos, sin espacios "
                "ni símbolos.",
                parent=ventana
            )
            return None

        if not datos["colonia"] or len(datos["colonia"]) > 50:
            messagebox.showwarning(
                "Colonia",
                "Escribe una colonia de hasta 50 caracteres.",
                parent=ventana
            )
            return None

        if not datos["direccion"] or len(datos["direccion"]) > 50:
            messagebox.showwarning(
                "Dirección",
                "Escribe una dirección de hasta 50 caracteres.",
                parent=ventana
            )
            return None

        try:
            salario = Decimal(datos["salario"])

            if not salario.is_finite() or salario < 0:
                raise InvalidOperation

            if salario.as_tuple().exponent < -2:
                raise InvalidOperation

            if salario > Decimal("99999999.99"):
                raise InvalidOperation

        except (InvalidOperation, ValueError):
            messagebox.showwarning(
                "Salario",
                "Escribe un salario válido, no negativo y con máximo "
                "dos decimales. Ejemplo: 8500.00.",
                parent=ventana
            )
            return None

        if combo_sucursal.get() not in sucursales:
            messagebox.showwarning(
                "Sucursal",
                "Selecciona una sucursal.",
                parent=ventana
            )
            return None

        if combo_horario.get() not in horarios:
            messagebox.showwarning(
                "Horario",
                "Selecciona un horario.",
                parent=ventana
            )
            return None

        if combo_turno.get() not in turnos:
            messagebox.showwarning(
                "Turno",
                "Selecciona un turno.",
                parent=ventana
            )
            return None

        return (
            datos["nombre"],
            datos["apellidos"],
            int(datos["edad"]),
            int(telefono),
            datos["colonia"],
            datos["direccion"],
            salario,
            sucursales[combo_sucursal.get()],
            horarios[combo_horario.get()],
            turnos[combo_turno.get()]
        )

    #  LIMPIAR 
    def limpiar():
        nonlocal seleccion_id
        seleccion_id = None

        for entrada in entradas.values():
            entrada.delete(0, tk.END)

        combo_sucursal.set("")
        combo_horario.set("")
        combo_turno.set("")

        seleccion = tabla.selection()

        if seleccion:
            tabla.selection_remove(seleccion)

    #  REGISTRAR 
    def crear_personal():
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
                INSERT INTO personal (
                    Nombre,
                    `ApePat/Mat`,
                    Edad,
                    `Teléfono`,
                    Colonia,
                    `Dirección`,
                    Salario,
                    ID_Sucursal,
                    ID_Horario,
                    ID_Turno
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, datos)

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "El empleado se registró correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_personal()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar al empleado:\n{error}",
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

        claves = (
            "nombre",
            "apellidos",
            "edad",
            "telefono",
            "colonia",
            "direccion",
            "salario"
        )

        # Los campos de texto se copian desde la tabla.
        for indice, clave in enumerate(claves, start=1):
            entradas[clave].delete(0, tk.END)
            entradas[clave].insert(
                0,
                str(valores[indice] if valores[indice] is not None else "")
            )

        # Sucursal: posición 8
        for etiqueta, id_sucursal in sucursales.items():
            if str(id_sucursal) == str(valores[8]):
                combo_sucursal.set(etiqueta)
                break

        # Horario: posición 9
        for etiqueta, id_horario in horarios.items():
            if str(id_horario) == str(valores[9]):
                combo_horario.set(etiqueta)
                break

        # Turno: posición 10
        for etiqueta, id_turno in turnos.items():
            if str(id_turno) == str(valores[10]):
                combo_turno.set(etiqueta)
                break

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    #  ACTUALIZAR 
    def actualizar_personal():
        if seleccion_id is None:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un empleado de la tabla.",
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
                UPDATE personal
                SET
                    Nombre = %s,
                    `ApePat/Mat` = %s,
                    Edad = %s,
                    `Teléfono` = %s,
                    Colonia = %s,
                    `Dirección` = %s,
                    Salario = %s,
                    ID_Sucursal = %s,
                    ID_Horario = %s,
                    ID_Turno = %s
                WHERE ID_Personal = %s
            """, (*datos, seleccion_id))

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "El empleado se actualizó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_personal()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar al empleado:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  ELIMINAR 
    def eliminar_personal():
        if seleccion_id is None:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un empleado de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este empleado?\n\n"
            "Si tiene pagos u otros registros relacionados, "
            "MySQL podría impedir la eliminación.",
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
                DELETE FROM personal
                WHERE ID_Personal = %s
            """, (seleccion_id,))

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "El empleado se eliminó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_personal()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                "No se pudo eliminar al empleado. "
                "Puede tener pagos u otros registros asociados.\n\n"
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
        command=crear_personal
    ).grid(row=0, column=0, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Actualizar",
        command=actualizar_personal
    ).grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Eliminar",
        command=eliminar_personal
    ).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Limpiar",
        command=limpiar
    ).grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(
        botones,
        text="Actualizar tabla",
        command=mostrar_personal
    ).grid(row=0, column=4, padx=5, pady=5)

    cargar_listas()
    mostrar_personal()