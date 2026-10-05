import os
import psycopg2


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DB", "sistema_referencial"),
    "port": int(os.getenv("POSTGRES_PORT", "5432"))
}


def obtener_conexion():
    return psycopg2.connect(**DB_CONFIG)