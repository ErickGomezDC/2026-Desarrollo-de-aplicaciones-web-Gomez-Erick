import os
import mysql.connector


DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE", "sistema_referencial"),
    "port": int(os.getenv("MYSQL_PORT", "3306"))
}


def obtener_conexion():
    return mysql.connector.connect(**DB_CONFIG)