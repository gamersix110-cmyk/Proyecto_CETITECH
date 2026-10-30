from tkinter import ttk

AZUL_OSCURO = "#0D223B"   # fondo de las ventanas
GRIS_AZUL = "#8E9AD6"     # encabezados, bordes y botones activos
TURQUESA = "#7EBFC2"      # titulos, botones y marcos
BLANCO = "#FFFFFF"
FONDO_CAMPO = "#F4F8F9"   # entradas y tablas

FAMILIA_TITULO = "Georgia"
FUENTE_TITULO = (FAMILIA_TITULO, 18, "bold")
FUENTE_TITULO_GRANDE = (FAMILIA_TITULO, 38, "bold")
FUENTE_SUBTITULO = (FAMILIA_TITULO, 13, "italic")


def aplicar_tema(ventana):
    """Aplica la paleta de colores a una ventana y a sus widgets ttk."""
    ventana.configure(bg=AZUL_OSCURO)

    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")

    estilo.configure(
        ".",
        background=AZUL_OSCURO,
        foreground=BLANCO,
        fieldbackground=FONDO_CAMPO,
        bordercolor=GRIS_AZUL,
        lightcolor=GRIS_AZUL,
        darkcolor=GRIS_AZUL
    )

    # Marcos
    estilo.configure(
        "TLabelframe",
        background=AZUL_OSCURO,
        bordercolor=TURQUESA,
        lightcolor=TURQUESA,
        darkcolor=TURQUESA
    )
    estilo.configure(
        "TLabelframe.Label",
        background=AZUL_OSCURO,
        foreground=TURQUESA,
        font=(FAMILIA_TITULO, 11, "bold")
    )

    # Botones
    estilo.configure(
        "TButton",
        background=TURQUESA,
        foreground=AZUL_OSCURO,
        bordercolor=TURQUESA,
        lightcolor=TURQUESA,
        darkcolor=TURQUESA,
        focuscolor=GRIS_AZUL,
        padding=(12, 6),
        relief="flat"
    )
    estilo.map(
        "TButton",
        background=[("pressed", GRIS_AZUL), ("active", GRIS_AZUL)],
        foreground=[("pressed", BLANCO), ("active", BLANCO)],
        bordercolor=[("pressed", GRIS_AZUL), ("active", GRIS_AZUL)],
        lightcolor=[("pressed", GRIS_AZUL), ("active", GRIS_AZUL)],
        darkcolor=[("pressed", GRIS_AZUL), ("active", GRIS_AZUL)]
    )

    # Campos de texto
    estilo.configure(
        "TEntry",
        fieldbackground=FONDO_CAMPO,
        foreground=AZUL_OSCURO,
        insertcolor=AZUL_OSCURO,
        bordercolor=GRIS_AZUL
    )
    estilo.map("TEntry", bordercolor=[("focus", TURQUESA)])

    # Listas desplegables
    estilo.configure(
        "TCombobox",
        fieldbackground=FONDO_CAMPO,
        background=TURQUESA,
        foreground=AZUL_OSCURO,
        arrowcolor=AZUL_OSCURO,
        bordercolor=GRIS_AZUL
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", FONDO_CAMPO)],
        foreground=[("readonly", AZUL_OSCURO)],
        background=[("active", TURQUESA), ("pressed", TURQUESA)],
        selectbackground=[("readonly", FONDO_CAMPO)],
        selectforeground=[("readonly", AZUL_OSCURO)],
        bordercolor=[("focus", TURQUESA)]
    )
    ventana.option_add("*TCombobox*Listbox.background", FONDO_CAMPO)
    ventana.option_add("*TCombobox*Listbox.foreground", AZUL_OSCURO)
    ventana.option_add("*TCombobox*Listbox.selectBackground", GRIS_AZUL)
    ventana.option_add("*TCombobox*Listbox.selectForeground", BLANCO)

    estilo.configure(
        "TCheckbutton",
        background=AZUL_OSCURO,
        foreground=BLANCO,
        indicatorbackground=FONDO_CAMPO,
        indicatorforeground=AZUL_OSCURO
    )
    estilo.map(
        "TCheckbutton",
        background=[("active", AZUL_OSCURO)],
        indicatorcolor=[("selected", TURQUESA)]
    )

    # Tablas
    estilo.configure(
        "Treeview",
        background=FONDO_CAMPO,
        fieldbackground=FONDO_CAMPO,
        foreground=AZUL_OSCURO,
        bordercolor=GRIS_AZUL,
        rowheight=24
    )
    estilo.map(
        "Treeview",
        background=[("selected", GRIS_AZUL)],
        foreground=[("selected", BLANCO)]
    )
    estilo.configure(
        "Treeview.Heading",
        background=GRIS_AZUL,
        foreground=BLANCO,
        bordercolor=AZUL_OSCURO,
        relief="flat",
        padding=(4, 5)
    )
    estilo.map(
        "Treeview.Heading",
        background=[("active", TURQUESA)],
        foreground=[("active", AZUL_OSCURO)]
    )
