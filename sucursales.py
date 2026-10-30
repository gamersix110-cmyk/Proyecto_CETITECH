
import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar
from estilo import aplicar_tema, FUENTE_TITULO


def abrir_sucursales(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Chatino's Pizza - Sucursales")
    ventana.geometry("850x570")
    ventana.minsize(700, 450)
    aplicar_tema(ventana)

    seleccion_id = None

    #  TITULO 
    ttk.Label(
        ventana,
        text="Administración de sucursales",
        font=FUENTE_TITULO
    ).pack(pady=(15, 10))

    #  FORMULARIO 
    formulario = ttk.LabelFrame(
        ventana,
        text="Datos de la sucursal",
        padding=15
    )
    formulario.pack(fill="x", padx=20, pady=10)

    ttk.Label(formulario, text="Nombre:").grid(
        row=0, column=0, sticky="w", padx=5, pady=7
    )
    entry_nombre = ttk.Entry(formulario, width=35)
    entry_nombre.grid(
        row=0, column=1, sticky="ew", padx=5, pady=7
    )

    ttk.Label(formulario, text="Colonia:").grid(
        row=1, column=0, sticky="w", padx=5, pady=7
    )
    entry_colonia = ttk.Entry(formulario, width=35)
    entry_colonia.grid(
        row=1, column=1, sticky="ew", padx=5, pady=7
    )

    ttk.Label(formulario, text="Dirección:").grid(
        row=2, column=0, sticky="w", padx=5, pady=7
    )
    entry_direccion = ttk.Entry(formulario, width=35)
    entry_direccion.grid(
        row=2, column=1, sticky="ew", padx=5, pady=7
    )

    formulario.columnconfigure(1, weight=1)

    #  TABLA 
    columnas = (
        "ID_Sucursal",
        "Nombre",
        "Colonia",
        "Direccion"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=10
    )

    tabla.heading("ID_Sucursal", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Colonia", text="Colonia")
    tabla.heading("Direccion", text="Dirección")

    tabla.column("ID_Sucursal", width=60, anchor="center")
    tabla.column("Nombre", width=180)
    tabla.column("Colonia", width=160)
    tabla.column("Direccion", width=350)

    tabla.pack(
        fill="both", expand=True, padx=20, pady=10
    )

    #  CONSULTAR SUCURSALES 
    def mostrar_sucursales():
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
                SELECT ID_Sucursal, Nombre, Colonia, `Dirección`
                FROM sucursal
                ORDER BY ID_Sucursal
            """)

            for fila in cursor.fetchall():
                tabla.insert("", "end", values=fila)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron consultar las sucursales:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  VALIDAR FORMULARIO 
    def obtener_datos():
        nombre = entry_nombre.get().strip()
        colonia = entry_colonia.get().strip()
        direccion = entry_direccion.get().strip()

        if not nombre or not colonia or not direccion:
            messagebox.showwarning(
                "Campos incompletos",
                "Completa todos los campos.",
                parent=ventana
            )
            return None

        if len(nombre) > 50:
            messagebox.showwarning(
                "Validación",
                "El nombre admite hasta 50 caracteres.",
                parent=ventana
            )
            return None

        if len(colonia) > 50:
            messagebox.showwarning(
                "Validación",
                "La colonia admite hasta 50 caracteres.",
                parent=ventana
            )
            return None

        if len(direccion) > 100:
            messagebox.showwarning(
                "Validación",
                "La dirección admite hasta 100 caracteres.",
                parent=ventana
            )
            return None

        return nombre, colonia, direccion

    #  LIMPIAR FORMULARIO 
    def limpiar():
        nonlocal seleccion_id
        seleccion_id = None

        entry_nombre.delete(0, tk.END)
        entry_colonia.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)

        seleccion = tabla.selection()
        if seleccion:
            tabla.selection_remove(seleccion)

        entry_nombre.focus_set()

    #  REGISTRAR 
    def crear_sucursal():
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
                INSERT INTO sucursal
                    (Nombre, Colonia, `Dirección`)
                VALUES (%s, %s, %s)
            """, datos)

            conexion.commit()

            messagebox.showinfo(
                "Registro correcto",
                "La sucursal se registró correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_sucursales()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar la sucursal:\n{error}",
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

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])

        entry_colonia.delete(0, tk.END)
        entry_colonia.insert(0, valores[2])

        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, valores[3])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    #  ACTUALIZAR 
    def actualizar_sucursal():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona una sucursal de la tabla.",
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
                UPDATE sucursal
                SET Nombre = %s,
                    Colonia = %s,
                    `Dirección` = %s
                WHERE ID_Sucursal = %s
            """, (*datos, seleccion_id))

            conexion.commit()

            messagebox.showinfo(
                "Actualización correcta",
                "La sucursal se actualizó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_sucursales()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar la sucursal:\n{error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  ELIMINAR 
    def eliminar_sucursal():
        if seleccion_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Selecciona una sucursal de la tabla.",
                parent=ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar esta sucursal?\n\n"
            "Si tiene empleados asociados, MySQL podría "
            "impedir la eliminación.",
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
                DELETE FROM sucursal
                WHERE ID_Sucursal = %s
            """, (seleccion_id,))

            conexion.commit()

            messagebox.showinfo(
                "Eliminación correcta",
                "La sucursal se eliminó correctamente.",
                parent=ventana
            )

            limpiar()
            mostrar_sucursales()

        except Exception as error:
            conexion.rollback()

            messagebox.showerror(
                "No se pudo eliminar",
                "Puede que la sucursal tenga empleados asociados.\n\n"
                f"Detalle: {error}",
                parent=ventana
            )

        finally:
            conexion.close()

    #  BOTONES 
    panel_botones = ttk.Frame(ventana, padding=10)
    panel_botones.pack()

    ttk.Button(
        panel_botones,
        text="Registrar",
        command=crear_sucursal
    ).grid(row=0, column=0, padx=5, pady=5)

    ttk.Button(
        panel_botones,
        text="Actualizar",
        command=actualizar_sucursal
    ).grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(
        panel_botones,
        text="Eliminar",
        command=eliminar_sucursal
    ).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(
        panel_botones,
        text="Limpiar",
        command=limpiar
    ).grid(row=0, column=3, padx=5, pady=5)

    ttk.Button(
        panel_botones,
        text="Actualizar tabla",
        command=mostrar_sucursales
    ).grid(row=0, column=4, padx=5, pady=5)

    mostrar_sucursales()