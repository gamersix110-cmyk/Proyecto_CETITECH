Chatino's Pizza – Sistema de Administración de Personal
Descripción del proyecto

El sistema de administración de personal de Chatino's Pizza es una aplicación de escritorio desarrollada en Python, diseñada para facilitar la gestión y organización de la información del personal de la empresa.

Su objetivo es centralizar la administración de empleados, sucursales, turnos, horarios, asistencias y pagos mediante una interfaz gráfica sencilla e intuitiva, conectada a una base de datos MySQL.

La aplicación permite registrar, consultar, actualizar y eliminar información de los diferentes módulos, facilitando el control de los datos administrativos del personal.

Tecnologías utilizadas
Python: lenguaje de programación utilizado para desarrollar la aplicación.
Tkinter: biblioteca utilizada para crear la interfaz gráfica.
MySQL: sistema de gestión de bases de datos utilizado para almacenar la información.
MySQL Connector: herramienta que permite establecer la conexión entre Python y MySQL.
Funcionalidades principales

El sistema está compuesto por los siguientes módulos:

1. Administración de personal

Permite registrar y administrar la información de los empleados, incluyendo:

Nombre y apellidos.
Edad.
Teléfono.
Colonia y dirección.
Salario.
Sucursal asignada.
Horario y turno correspondientes.
2. Administración de sucursales

Permite gestionar la información de las diferentes sucursales de Chatino's Pizza:

Nombre de la sucursal.
Colonia.
Dirección.
3. Administración de turnos

Permite administrar los turnos de trabajo, considerando los días y las horas de entrada y salida.

4. Administración de horarios

Permite registrar y modificar horarios laborales, relacionándolos con los turnos correspondientes.

5. Control de asistencia

Permite registrar las horas de entrada y salida del personal, relacionarlas con un turno y calcular automáticamente si existe un retardo de acuerdo con la hora de entrada establecida.

Nota: En la versión actual, el registro de asistencia no almacena el identificador del empleado ni la fecha de asistencia.

6. Administración de pagos

Permite registrar y consultar los pagos del personal. Incluye:

Salario.
Bonos.
Descuentos.
Cálculo automático del monto total.

El monto se obtiene mediante la siguiente operación:

Monto total = Salario + Bono - Descuento

Estructura del proyecto

El proyecto está organizado en diferentes archivos de Python, cada uno encargado de una función específica.

Archivo	Descripción
main.py	Archivo principal. Inicia la aplicación y muestra el menú de módulos.
conexion.py	Contiene la función encargada de establecer la conexión con MySQL.
estilo.py	Define los colores, fuentes y estilos de la interfaz gráfica.
personal.py	Administra la información de los empleados.
sucursales.py	Administra los registros de las sucursales.
turnos.py	Gestiona los turnos laborales.
horarios.py	Administra los horarios de trabajo.
asistencia.py	Controla los registros de asistencia y retardos.
pagos.py	Gestiona los pagos, bonos y descuentos del personal.
Base de datos

El sistema utiliza MySQL y se conecta a una base de datos llamada:

chatinos_pizza

La aplicación trabaja con las siguientes tablas:

personal
sucursal
turno
horario
asistencia
pago

Estas tablas permiten organizar la información y establecer relaciones entre los diferentes elementos del sistema.

Requisitos para ejecutar el proyecto

Antes de iniciar la aplicación, es necesario contar con:

Python instalado.
MySQL Server instalado y funcionando.
La base de datos chatinos_pizza creada.
Las tablas necesarias configuradas en MySQL.
Los archivos del proyecto dentro de una misma carpeta.

También se debe instalar el conector de MySQL para Python.

Instalación
1. Instalar la dependencia

Abrir una terminal y ejecutar:

pip install mysql-connector-python
2. Configurar la conexión

Abrir el archivo conexion.py y verificar los datos de conexión:

return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatinos_pizza"
)

Es necesario ajustar el usuario y la contraseña de acuerdo con la configuración del servidor MySQL.

3. Preparar la base de datos

Crear la base de datos chatinos_pizza en MySQL e importar o ejecutar las instrucciones SQL necesarias para crear las tablas que utiliza el sistema.

4. Ejecutar la aplicación

Desde la terminal, ingresar a la carpeta del proyecto y ejecutar:

python main.py

Al iniciar, aparecerá la ventana principal de Chatino's Pizza, desde donde se podrá acceder a los diferentes módulos.

Interfaz gráfica

La aplicación cuenta con una interfaz gráfica desarrollada con Tkinter. Se utiliza una paleta de colores basada en azul oscuro, turquesa, gris azulado y blanco.

El diseño busca mantener una presentación uniforme en todos los módulos, facilitando la navegación y el uso del sistema.

Consideraciones
Es necesario mantener activo el servidor MySQL para utilizar las funciones que consultan o modifican información.
Los datos se almacenan en la base de datos y no únicamente en la interfaz gráfica.
El sistema cuenta con validaciones para evitar el registro de información incompleta o incorrecta.
Las operaciones de modificación y eliminación requieren seleccionar previamente un registro.
Las credenciales de conexión deben configurarse de acuerdo con el entorno donde se ejecute el programa.
Autoría y propósito

Proyecto: Chatino's Pizza – Sistema de Administración de Personal.

Propósito: Desarrollar una herramienta informática que facilite la administración de los recursos humanos de la empresa, centralizando la información del personal y sus procesos administrativos en una sola aplicación.
