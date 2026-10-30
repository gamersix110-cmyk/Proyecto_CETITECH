
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
from conexion import conectar
from estilo import aplicar_tema, FUENTE_TITULO


def abrir_pagos(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Chatino's Pizza - Pagos")
    ventana.geometry("920x620")
    ventana.minsize(800, 540)
    aplicar_tema(ventana)

    seleccion_id = None
    empleados = {}

    #  TITULO 
    ttk.Label(
        ventana,
        text="Administración de pagos",
        font=FUENTE_TITULO
    ).pack(pady=12)

    #  FORMULARIO 
    formulario = ttk.LabelFrame(
        ventana, text="Datos del pago", padding=12
    )
    formulario.pack(fill="x", padx=20, pady=8)

    ttk.Label(formulario, text="Empleado:").grid(
        row=0, column=0, padx=5, pady=7, sticky="w"
    )

    combo_empleado = ttk.Combobox(
        formulario, state="readonly", width=35
    )
    combo_empleado.grid(
        row=0, column=1, padx=5, pady=7, sticky="ew"
    )

    ttk.Label(formulario, text="Salario ($):").grid(
        row=1, column=0, padx=5, pady=7, sticky="w"
    )

    entry_salario = ttk.Entry(formulario)
    entry_salario.grid(
        row=1, column=1, padx=5, pady=7, sticky="ew"
    )

    ttk.Label(formulario, text="Bono ($):").grid(
        row=2, column=0, padx=5, pady=7, sticky="w"
    )

    entry_bono = ttk.Entry(formulario)
    entry_bono.insert(0, "0.00")
    entry_bono.grid(
        row=2, column=1, padx=5, pady=7, sticky="ew"
    )

    ttk.Label(formulario, text="Descuento ($):").grid(
        row=3, column=0, padx=5, pady=7, sticky="w"
    )

    entry_descuento = ttk.Entry(formulario)
    entry_descuento.insert(0, "0.00")
    entry_descuento.grid(
        row=3, column=1, padx=5, pady=7, sticky="ew"
    )

    ttk.Label(formulario, text="Monto total ($):").grid(
        row=4, column=0, padx=5, pady=7, sticky="w"
    )

    etiqueta_monto = ttk.Label(
        formulario, text="$0.00",
        font=("Arial", 12, "bold")
    )
    etiqueta_monto.grid(
        row=4, column=1, padx=5, pady=7, sticky="w"
    )

    formulario.columnconfigure(1, weight=1)

    #  CALCULAR MONTO 
    def calcular_monto(event=None):
        try:
            salario = Decimal(entry_salario.get().strip())
            bono = Decimal(entry_bono.get().strip() or "0")
            descuento = Decimal(
                entry_descuento.get().strip() or "0"
            )

            importes = (salario, bono, descuento)

            if not all(x.is_finite() for x in importes):
                raise InvalidOperation

            if any(x < 0 for x in importes):
                etiqueta_monto.config(text="Importes inválidos")
                return

            monto = salario + bono - descuento

            if monto < 0:
                etiqueta_monto.config(text="Monto negativo")
                return

            etiqueta_monto.config(text=f"${monto:.2f}")

        except (InvalidOperation, ValueError):
            etiqueta_monto.config(text="Revisa los importes")

    entry_salario.bind("<KeyRelease>", calcular_monto)
    entry_bono.bind("<KeyRelease>", calcular_monto)
    entry_descuento.bind("<KeyRelease>", calcular_monto)

    #  CARGAR EMPLEADOS 
    def cargar_empleados():
        empleados.clear()

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
                    Salario
                FROM personal
                ORDER BY Nombre
            """)

            opciones = []

            for id_personal, nombre, apellidos, salario in cursor.fetchall():
                nombre_completo = (
                    f"{nombre or ''} {apellidos or ''}".strip()
                )

                texto = f"{id_personal} - {nombre_completo}"

                empleados[texto] = {
                    "id": id_personal,
                    "salario": salario
                }

                opciones.append(texto)

            combo_empleado["values"] = opciones

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los empleados:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    def seleccionar_empleado(event=None):
        empleado = empleados.get(combo_empleado.get())

        if empleado is not None:
            entry_salario.delete(0, tk.END)
            entry_salario.insert(
                0, str(empleado["salario"] or "0.00")
            )
            calcular_monto()

    combo_empleado.bind(
        "<<ComboboxSelected>>", seleccionar_empleado
    )

    #  TABLA 
    columnas = (
        "ID_Pago", "empleado", "Salario",
        "Bono", "Descuento", "Monto"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=12
    )

    encabezados = {
        "ID_Pago": "ID pago",
        "empleado": "Empleado",
        "Salario": "Salario",
        "Bono": "Bono",
        "Descuento": "Descuento",
        "Monto": "Monto total"
    }

    for columna, titulo in encabezados.items():
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=130, anchor="center")

    tabla.column("empleado", width=220)

    tabla.pack(
        fill="both", expand=True, padx=20, pady=8
    )

    #  CONSULTAR PAGOS 
    def mostrar_pagos():
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
                    p.ID_Pago,
                    p.ID_Personal,
                    CONCAT(
                        COALESCE(per.Nombre, ''),
                        ' ',
                        COALESCE(per.`ApePat/Mat`, '')
                    ) AS empleado,
                    p.Salario,
                    p.Bono,
                    p.Descuento,
                    p.Monto
                FROM pago AS p
                INNER JOIN personal AS per
                    ON p.ID_Personal = per.ID_Personal
                ORDER BY p.ID_Pago DESC
            """)

            for fila in cursor.fetchall():
                id_pago, id_personal, nombre, salario, bono, descuento, monto = fila

                tabla.insert(
                    "", "end",
                    values=(
                        id_pago,
                        f"{id_personal} - {nombre.strip()}",
                        salario,
                        bono,
                        descuento,
                        monto
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron consultar los pagos:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  OBTENER DATOS 
    def obtener_datos():
        texto_empleado = combo_empleado.get()

        if texto_empleado not in empleados:
            messagebox.showwarning(
                "Empleado",
                "Selecciona un empleado.",
                parent=ventana
            )
            return None

        try:
            salario = Decimal(entry_salario.get().strip())
            bono = Decimal(entry_bono.get().strip() or "0")
            descuento = Decimal(
                entry_descuento.get().strip() or "0"
            )

            importes = (salario, bono, descuento)

            if not all(x.is_finite() for x in importes):
                raise InvalidOperation

            if any(x < 0 for x in importes):
                raise ValueError

            if any(x.as_tuple().exponent < -2 for x in importes):
                raise InvalidOperation

            if any(x > Decimal("99999999.99") for x in importes):
                raise InvalidOperation

            monto = salario + bono - descuento

            if monto < 0:
                messagebox.showwarning(
                    "Monto inválido",
                    "El descuento no puede superar el salario más el bono.",
                    parent=ventana
                )
                return None

            if monto > Decimal("99999999.99"):
                raise InvalidOperation

            return (
                empleados[texto_empleado]["id"],
                monto,
                salario,
                bono,
                descuento
            )

        except (InvalidOperation, ValueError):
            messagebox.showwarning(
                "Importes inválidos",
                "Escribe cantidades no negativas, con máximo "
                "dos decimales. Ejemplo: 8500.00.",
                parent=ventana
            )
            return None

    #  LIMPIAR 
    def limpiar():
        nonlocal seleccion_id
        seleccion_id = None

        combo_empleado.set("")

        entry_salario.delete(0, tk.END)
        entry_bono.delete(0, tk.END)
        entry_descuento.delete(0, tk.END)

        entry_bono.insert(0, "0.00")
        entry_descuento.insert(0, "0.00")

        etiqueta_monto.config(text="$0.00")

        seleccion = tabla.selection()

        if seleccion:
            tabla.selection_remove(seleccion)

    #  REGISTRAR PAGO 
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
                INSERT INTO pago
                    (ID_Personal, Monto, Salario, Bono, Descuento)
                VALUES (%s, %s, %s, %s, %s)
            """, datos)

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "El pago se registró correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_pagos()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el pago:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  SELECCIONAR PAGO 
    def seleccionar_fila(event=None):
        nonlocal seleccion_id

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")

        if not valores:
            return

        seleccion_id = int(valores[0])

        # El empleado se muestra como "ID - Nombre".
        empleado_tabla = str(valores[1]).split(" - ", 1)[0]

        for texto, datos in empleados.items():
            if str(datos["id"]) == empleado_tabla:
                combo_empleado.set(texto)
                break

        entry_salario.delete(0, tk.END)
        entry_salario.insert(0, str(valores[2]))

        entry_bono.delete(0, tk.END)
        entry_bono.insert(0, str(valores[3]))

        entry_descuento.delete(0, tk.END)
        entry_descuento.insert(0, str(valores[4]))

        calcular_monto()

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    #  ACTUALIZAR PAGO 
    def actualizar():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección",
                "Selecciona un pago de la tabla.",
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
                UPDATE pago
                SET ID_Personal = %s,
                    Monto = %s,
                    Salario = %s,
                    Bono = %s,
                    Descuento = %s
                WHERE ID_Pago = %s
            """, (*datos, seleccion_id))

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "El pago se actualizó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_pagos()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el pago:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  ELIMINAR PAGO 
    def eliminar():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección",
                "Selecciona un pago de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Deseas eliminar el pago seleccionado?",
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

            cursor.execute(
                "DELETE FROM pago WHERE ID_Pago = %s",
                (seleccion_id,)
            )

            conexion.commit()

            messagebox.showinfo(
                "Correcto",
                "El pago se eliminó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_pagos()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el pago:\n{error}",
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
        botones, text="Recargar tabla", command=mostrar_pagos
    ).grid(row=0, column=4, padx=4, pady=5)

    cargar_empleados()
    mostrar_pagos()