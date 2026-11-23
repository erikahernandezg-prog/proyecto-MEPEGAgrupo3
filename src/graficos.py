import os
import pandas as pd
import matplotlib.pyplot as plt

# Ruta hacia la carpeta 'data' (funciona ejecutando desde la raíz o desde src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATA = os.path.join(BASE_DIR, "data")


def _cargar_datos_pqrs():
    """Lee los 4 archivos .txt de PQRS y los une en un solo DataFrame de pandas."""
    archivos = ["Peticion.txt", "Queja.txt", "Reclamo.txt", "Sugerencia.txt"]
    tablas = []

    for nombre in archivos:
        ruta = os.path.join(CARPETA_DATA, nombre)
        if os.path.exists(ruta) and os.path.getsize(ruta) > 0:
            # Lee cada archivo usando '|' como separador y tomando la primera fila como encabezado
            df_temp = pd.read_csv(ruta, sep="|", encoding="utf-8")
            tablas.append(df_temp)

    if not tablas:
        return pd.DataFrame()

    # Combina los 4 archivos en una sola tabla general
    return pd.concat(tablas, ignore_index=True)


def mostrar_graficos():
    """Genera y muestra los 4 gráficos estadísticos de PQRS (mascota, canal, campus y estado)."""
    df = _cargar_datos_pqrs()

    if df.empty:
        print("No hay datos disponibles en la carpeta 'data' para generar los gráficos.")
        return

    # Crear una ventana con 4 subgráficos (2 filas x 2 columnas)
    fig, ejes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("Estadísticas Generales de PQRS - Burbuja Pets", fontsize=15, fontweight="bold")

    # 1. Gráfico por Tipo de Mascota (Barras verticales)
    conteo_mascota = df["tipo_mascota"].value_counts()
    barras_mascota = ejes[0, 0].bar(
        conteo_mascota.index,
        conteo_mascota.values,
        color=["#4C72B0", "#DD8452", "#55A868"]
    )
    ejes[0, 0].set_title("PQRS por Tipo de Mascota")
    ejes[0, 0].set_xlabel("Tipo de mascota")
    ejes[0, 0].set_ylabel("Cantidad de PQRS")
    ejes[0, 0].bar_label(barras_mascota, padding=3)

    # 2. Gráfico por Estado de la Petición (Gráfico de torta / pastel)
    conteo_estado = df["estado_peticion"].value_counts()
    ejes[0, 1].pie(
        conteo_estado.values,
        labels=conteo_estado.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#64B5F6", "#FFD54F", "#81C784"]
    )
    ejes[0, 1].set_title("Distribución por Estado")

    # 3. Gráfico por Canal de Recepción (Barras verticales)
    conteo_canal = df["canal_recepcion"].value_counts()
    barras_canal = ejes[1, 0].bar(
        conteo_canal.index,
        conteo_canal.values,
        color="#5C6BC0"
    )
    ejes[1, 0].set_title("PQRS por Canal de Recepción")
    ejes[1, 0].set_xlabel("Canal")
    ejes[1, 0].set_ylabel("Cantidad de PQRS")
    ejes[1, 0].tick_params(axis="x", rotation=25)
    ejes[1, 0].bar_label(barras_canal, padding=3)

    # 4. Gráfico por Campus Relacionado (Barras horizontales para leer mejor los nombres largos)
    conteo_campus = df["campus_relacionado"].value_counts()
    # Acortar el prefijo 'Campus Medellín - ' para que el eje Y se vea limpio
    etiquetas_campus = [
        nombre.replace("Campus Medellín - ", "").replace("Campus en el ", "")
        for nombre in conteo_campus.index
    ]
    barras_campus = ejes[1, 1].barh(
        etiquetas_campus,
        conteo_campus.values,
        color="#26A69A"
    )
    ejes[1, 1].set_title("PQRS por Campus")
    ejes[1, 1].set_xlabel("Cantidad de PQRS")
    ejes[1, 1].invert_yaxis()  # Muestra el campus con más PQRS arriba
    ejes[1, 1].bar_label(barras_campus, padding=3)

    # Ajustar márgenes para que no se superpongan los textos y mostrar en pantalla
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


if __name__ == "__main__":
    # Bloque de prueba directa para verificar los gráficos
    mostrar_graficos()
