# reportes.py
# Responsable: Darci Vanessa Londoño Ortiz (Control de calidad / Validaciones)
# Requisito: RF-14 (promedio de días + estadísticas) y exportar resultados
#
# Lee las PQRS de los 4 archivos y calcula las estadísticas.

import os
from datetime import datetime
CARPETA_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TIPOS = ["Peticion", "Queja", "Reclamo", "Sugerencia"]


def leer_todas():
    """Lee las PQRS de los 4 archivos y las devuelve como una lista de diccionarios."""
    todas = []
    for tipo in TIPOS:
        ruta = os.path.join(CARPETA_DATA, tipo + ".txt")
        if not os.path.exists(ruta):
            continue
        with open(ruta, "r", encoding="utf-8") as archivo:
            encabezado = archivo.readline().strip().split("|")
            for linea in archivo:
                valores = linea.rstrip("\n").split("|")
                if not linea.strip():
                    continue
                # Si a una línea le faltan campos, se completan con vacío
                valores = (valores + [""] * len(encabezado))[:len(encabezado)]
                todas.append(dict(zip(encabezado, valores)))
    return todas

DIAS_ALERTA = 5  # una PQRS está "próxima a vencer" si le quedan 5 días o menos


def convertir_fecha(texto):
    """Convierte '2026-09-04 12:37:03' (o '2026-09-04') en una fecha de Python."""
    texto = texto.strip()
    for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            pass
    return None


def promedio_dias_respuesta():
    """Promedio (número entero) de días reales que tomó responder:
    fecha de respuesta - fecha de radicación, solo en las PQRS solucionadas
    que tienen fecha de respuesta guardada.
    Devuelve (promedio, cantidad de PQRS usadas en el cálculo)."""
    dias = []
    for pqrs in leer_todas():
        if pqrs.get("estado_peticion") != "Solucionada":
            continue
        inicio = convertir_fecha(pqrs.get("fecha_radicacion", ""))
        fin = convertir_fecha(pqrs.get("fecha_respuesta", ""))
        if inicio and fin:
            dias.append((fin - inicio).days)
    if len(dias) == 0:
        return 0, 0
    return round(sum(dias) / len(dias)), len(dias)


def contar_por(campo):
    """Cuenta cuántas PQRS hay por cada valor de un campo (mascota, canal, campus, estado...)."""
    conteo = {}
    for pqrs in leer_todas():
        valor = pqrs[campo]
        conteo[valor] = conteo.get(valor, 0) + 1
    # Ordenamos de mayor a menor
    return dict(sorted(conteo.items(), key=lambda par: par[1], reverse=True))


def vencidas_y_por_vencer():
    """Revisa las PQRS que NO están solucionadas: cuántas ya vencieron y cuántas vencen pronto."""
    hoy = datetime.now()
    vencidas, por_vencer = 0, 0
    for pqrs in leer_todas():
        if pqrs["estado_peticion"] == "Solucionada":
            continue
        limite = convertir_fecha(pqrs["fecha_maxima_respuesta"])
        if limite is None:
            continue
        dias_restantes = (limite - hoy).days
        if dias_restantes < 0:
            vencidas += 1
        elif dias_restantes <= DIAS_ALERTA:
            por_vencer += 1
    return vencidas, por_vencer


def mas_antiguas(cantidad=5):
    """Las PQRS pendientes (no solucionadas) más antiguas."""
    pendientes = [p for p in leer_todas() if p["estado_peticion"] != "Solucionada"]
    pendientes.sort(key=lambda p: p["fecha_radicacion"])
    return pendientes[:cantidad]


def texto_promedio():
    """Texto de la estadística obligatoria (promedio de días de respuesta)."""
    promedio, cantidad = promedio_dias_respuesta()
    if cantidad == 0:
        return "Promedio de días de respuesta: aún no hay PQRS solucionadas con fecha de respuesta"
    return f"Promedio de días de respuesta: {promedio} días (calculado con {cantidad} PQRS solucionadas)"


def construir_reporte():
    """Arma el texto completo del reporte de estadísticas."""
    total = len(leer_todas())
    vencidas, por_vencer = vencidas_y_por_vencer()
    lineas = ["=" * 60, "ESTADÍSTICAS DE PQRS - BURBUJA PETS",
              "Generado: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "=" * 60,
              f"Total de PQRS registradas: {total}",
              texto_promedio(), ""]
    titulos = [("tipo_solicitud", "Por tipo de solicitud"), ("tipo_mascota", "Por tipo de mascota"),
               ("canal_recepcion", "Por canal de recepción"), ("campus_relacionado", "Por campus"),
               ("estado_peticion", "Por estado"), ("tipo_documento", "Por tipo de documento"),
               ("usuario_registro", "Carga operativa: PQRS registradas por cada usuario")]
    for campo, titulo in titulos:
        lineas.append(titulo + ":")
        for valor, cantidad in contar_por(campo).items():
            porcentaje = cantidad * 100 / total if total else 0
            lineas.append(f"   {valor:<45} {cantidad:>6}  ({porcentaje:.1f} %)")
        lineas.append("")
    # Estadística 5: cantidad y porcentaje (sobre el total de PQRS)
    pct_vencidas = vencidas * 100 / total if total else 0
    pct_por_vencer = por_vencer * 100 / total if total else 0
    lineas.append("Alerta de vencimiento (plazo de respuesta):")
    lineas.append(f"   PQRS vencidas (sin solucionar): {vencidas}  ({pct_vencidas:.1f} %)")
    lineas.append(f"   PQRS próximas a vencer (≤ {DIAS_ALERTA} días): {por_vencer}  ({pct_por_vencer:.1f} %)")
    lineas.append("")
    lineas.append("Las 5 PQRS pendientes más antiguas:")
    for p in mas_antiguas():
        lineas.append(f"   {p['tipo_solicitud']} #{p['id']} - {p['fecha_radicacion']} - {p['estado_peticion']}")
    return lineas


def mostrar_reporte():
    print("\n".join(construir_reporte()))


def exportar_reporte():
    """Guarda las estadísticas en data/reporte_estadisticas.txt y devuelve la ruta."""
    ruta = os.path.join(CARPETA_DATA, "reporte_estadisticas.txt")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(construir_reporte()) + "\n")
    return ruta


# Si se ejecuta este archivo solo (python reportes.py), muestra el reporte y lo exporta
if __name__ == "__main__":
    mostrar_reporte()
    print("\nReporte guardado en:", exportar_reporte())
