
import pandas as pd
import sqlite3
import time

# Inicio del proceso
inicio = time.perf_counter()

conexion = None

try:
    # ==========================
    # 1. EXTRACCION
    # ==========================

    print("Iniciando extraccion...")

    df = pd.read_csv("datos/ventas.csv")

    print(f"Registros extraidos: {len(df)}")

    # ==========================
    # 2. TRANSFORMACION
    # ==========================

    print("\nIniciando transformacion...")

    # Eliminar registros con valores nulos
    df_limpio = df.dropna(
        subset=["producto", "cantidad", "precio_unitario"]
    ).copy()

    # Eliminar cantidades y precios invalidos
    df_limpio = df_limpio[
        (df_limpio["cantidad"] > 0) &
        (df_limpio["precio_unitario"] > 0)
    ].copy()

    # Calcular importe total de cada venta
    df_limpio["importe_total"] = (
        df_limpio["cantidad"] *
        df_limpio["precio_unitario"]
    )

    # Agrupar ventas por producto
    resumen = df_limpio.groupby(
        "producto", as_index=False
    ).agg(
        cantidad_total=("cantidad", "sum"),
        ventas_totales=("importe_total", "sum")
    )

    resumen["cantidad_total"] = (
        resumen["cantidad_total"].astype(int)
    )

    print(f"Registros validos: {len(df_limpio)}")
    print(f"Registros eliminados: {len(df) - len(df_limpio)}")

    # ==========================
    # 3. CARGA
    # ==========================

    print("\nIniciando carga en SQLite...")

    conexion = sqlite3.connect("ventas.db")

    cursor = conexion.cursor()

    # Crear tabla de destino
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumen_ventas (
            producto TEXT PRIMARY KEY,
            cantidad_total INTEGER NOT NULL,
            ventas_totales REAL NOT NULL
        )
    """)

    # Eliminar resultados anteriores
    # para evitar duplicados al ejecutar nuevamente
    cursor.execute("DELETE FROM resumen_ventas")

    # Insertar datos transformados
    cursor.executemany("""
        INSERT INTO resumen_ventas (
            producto,
            cantidad_total,
            ventas_totales
        )
        VALUES (?, ?, ?)
    """, list(resumen.itertuples(index=False, name=None)))

    # Confirmar los cambios
    conexion.commit()

    # ==========================
    # 4. VERIFICACION
    # ==========================

    resultado = pd.read_sql_query("""
        SELECT *
        FROM resumen_ventas
        ORDER BY ventas_totales DESC
    """, conexion)

    print("\nDATOS GUARDADOS EN SQLITE")
    print(resultado.to_string(index=False))

    print("\nProceso ETL completado correctamente.")

except FileNotFoundError:
    print("Error: no se encontro el archivo ventas.csv.")

except sqlite3.Error as error:
    if conexion is not None:
        conexion.rollback()

    print(f"Error de SQLite: {error}")

except Exception as error:
    if conexion is not None:
        conexion.rollback()

    print(f"Error durante el proceso ETL: {error}")

finally:
    if conexion is not None:
        conexion.close()

    tiempo_total = time.perf_counter() - inicio

    print(f"\nTiempo total: {tiempo_total:.6f} segundos")
