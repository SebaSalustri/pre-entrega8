# Automatización de procesos ETL con Python y SQLite

## Descripción

Proyecto de automatización de un proceso ETL (Extract, Transform, Load) utilizando Python, Pandas y SQLite.

El objetivo es extraer datos desde un archivo CSV, realizar operaciones de limpieza y transformación, y almacenar los resultados en una base de datos local.

## Tecnologías utilizadas

- Python
- Pandas
- SQLite
- SQL

## Dataset

Se utiliza un archivo CSV con datos sintéticos de ventas de productos.

El dataset contiene las siguientes columnas:

- venta_id: identificador de la venta.
- producto: nombre del producto.
- cantidad: cantidad de unidades vendidas.
- precio_unitario: precio por unidad.

El archivo contiene 11 registros, incluyendo valores nulos y cantidades negativas para comprobar el funcionamiento del proceso de limpieza.

## Arquitectura del proceso ETL

El flujo de procesamiento se divide en tres etapas:

### 1. Extracción (Extract)

Se utiliza Pandas para leer el archivo `datos/ventas.csv` mediante la función read_csv.

### 2. Transformación (Transform)

Se realizan las siguientes operaciones:

- Eliminación de registros con valores nulos.
- Eliminación de cantidades y precios menores o iguales a cero.
- Cálculo del importe total de cada venta.
- Agrupación de los registros por producto.
- Cálculo de la cantidad total vendida y del importe acumulado.

### 3. Carga (Load)

Los datos transformados se almacenan en una base de datos SQLite denominada `ventas.db`.

Se crea automáticamente la tabla resumen_ventas y se insertan los resultados mediante consultas SQL parametrizadas.

Antes de insertar los nuevos resultados, se eliminan los registros anteriores de la tabla para evitar duplicaciones al ejecutar nuevamente el proceso.

## Capa de persistencia

Se utiliza SQLite como sistema de almacenamiento local.

La tabla de destino presenta el siguiente esquema:

| Columna | Tipo de dato | Restricción |
|---|---|---|
| producto | TEXT | PRIMARY KEY |
| cantidad_total | INTEGER | NOT NULL |
| ventas_totales | REAL | NOT NULL |

La base de datos conserva los resultados después de finalizar la ejecución del programa.

## Manejo de errores

El script utiliza bloques try, except y finally para controlar posibles errores durante el proceso ETL.

Se contemplan los siguientes casos:

- Archivo CSV no encontrado.
- Errores de conexión o ejecución en SQLite.
- Errores generales durante el procesamiento.

Se utiliza rollback para revertir cambios no confirmados en caso de errores durante la carga.

La conexión a la base de datos se cierra al finalizar el proceso.

## Estructura del proyecto

```text
etl-ventas-sqlite/
├── datos/
│   └── ventas.csv
├── etl_ventas.py
├── requirements.txt
├── .gitignore
└── README.md
```

El archivo ventas.db se genera automáticamente al ejecutar el script.

## Instalación

Instalar las dependencias desde la carpeta raíz del proyecto:

```bash
pip install -r requirements.txt
```

SQLite forma parte de la biblioteca estándar de Python, por lo que no requiere una instalación adicional.

## Ejecución

Ejecutar desde la carpeta raíz del repositorio:

```bash
python etl_ventas.py
```

El script realiza automáticamente las etapas de extracción, transformación y carga.

## Resultados obtenidos

### Procesamiento de registros

| Indicador | Resultado |
|---|---:|
| Registros extraídos | 11 |
| Registros válidos | 8 |
| Registros eliminados | 3 |
| Productos almacenados | 4 |

### Datos almacenados en SQLite

| Producto | Cantidad total | Ventas totales |
|---|---:|---:|
| Notebook | 3 | 1500.0 |
| Monitor | 3 | 450.0 |
| Teclado | 4 | 160.0 |
| Mouse | 7 | 140.0 |

Los resultados fueron verificados mediante una consulta SQL sobre la tabla resumen_ventas.

## Rendimiento

El tiempo total de ejecución se midió utilizando time.perf_counter() de Python.

| Operación | Tiempo de ejecución (segundos) |
|---|---:|
| Proceso ETL completo | 0.243034 |

El tiempo incluye la extracción, transformación, carga, verificación de los resultados y cierre de la conexión a SQLite.

Este resultado corresponde a una ejecución realizada en el equipo de desarrollo y puede variar según el hardware y las condiciones de ejecución.

## Control de versiones

Se utiliza un archivo .gitignore para excluir archivos temporales, entornos virtuales y la base de datos generada automáticamente.

Esto permite mantener un repositorio limpio y reproducible.

## Conclusión

La automatización de procesos ETL permite integrar tareas de extracción, limpieza, transformación y almacenamiento de datos en un único flujo de trabajo.

Python y Pandas facilitan el procesamiento de los datos, mientras que SQLite proporciona una capa de persistencia local sin necesidad de configurar un servidor de base de datos.

El proyecto demuestra cómo automatizar un proceso de datos reproducible, incorporando validaciones, manejo de errores y almacenamiento persistente.
