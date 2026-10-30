import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chatinos_pizza"
        )
    except Error as error:
        print("Error al conectar con la base de datos:", error)
        return None