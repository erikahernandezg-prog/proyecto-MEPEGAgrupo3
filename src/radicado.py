# radicado.py: Generador del comprobante (radicado) de cada PQRS (Burbuja Pets).
# Responsable: Yanidis Yoela Arrieta Requeme 
# Descripción: Crea un .txt con marco ASCII (+ - |) donde CADA línea mide exactamente 120 caracteres.
No incluye la descripción detallada; si no hay dirección escribe "N/A".


from pathlib import Path

ANCHO = 120                 
INTERIOR = ANCHO - 4        
CARPETA_RADICADOS = Path(__file__).resolve().parent.parent / "data" / "radicados"


class c_radicado:
    """Clase ordenada y precisa que construye el comprobante ASCII de una PQRS."""

    @staticmethod
    def _borde():
        """Línea horizontal del marco: + y 118 guiones + (120 en total)."""
        return "+" + "-" * (ANCHO - 2) + "+"

    @staticmethod
    def _linea(texto="", centrado=False):
        """Línea de contenido ajustada (recortada o rellenada) a exactamente 120 caracteres."""
        texto = str(texto)[:INTERIOR]
        cuerpo = texto.center(INTERIOR) if centrado else texto.ljust(INTERIOR)
        return "| " + cuerpo + " |"

    @classmethod
    def _campo_doble(cls, et1, val1, et2, val2):
        """Dos pares etiqueta: valor en una misma línea, cada uno en media columna."""
        mitad = INTERIOR // 2
        izq = f"{et1}: {val1}"[:mitad - 2].ljust(mitad)
        der = f"{et2}: {val2}"[:INTERIOR - mitad]
        return cls._linea(izq + der)

    @classmethod
    def construir(cls, datos):
        """Arma el texto completo del radicado a partir del diccionario de la PQRS."""
        d = {k: str(v).strip() for k, v in datos.items()}
        direccion = d.get("direccion", "") or "N/A"   # campo opcional
        id_fmt = d.get("id", "").zfill(6)             # ID formateado con ceros a la izquierda

        filas = [
            cls._borde(),
            cls._linea("UNIVERSIDAD DE ANTIOQUIA - BURBUJA PETS", centrado=True),
            cls._linea("COMPROBANTE DE RADICADO DE PQRS", centrado=True),
            cls._borde(),
            cls._linea("DATOS DEL RADICADO", centrado=True),
            cls._borde(),
            cls._campo_doble("Radicado No.", id_fmt, "Fecha/hora de radicación", d.get("fecha_radicacion", "")),
            cls._campo_doble("Estado inicial", d.get("estado_peticion", "") or "Registrada",
                             "Fecha máxima de respuesta", d.get("fecha_maxima_respuesta", "")),
            cls._linea(f"Registrado por: {d.get('usuario_registro', '')}"),
            cls._borde(),
            cls._linea("DATOS DEL SOLICITANTE", centrado=True),
            cls._borde(),
            cls._linea(f"Nombre completo: {d.get('nombre_completo', '')}"),
            cls._campo_doble("Documento", f"{d.get('tipo_documento', '')} {d.get('numero_documento', '')}",
                             "Teléfono", f"{d.get('telefono_contacto', '')} ({d.get('tipo_telefono', '')})"),
            cls._linea(f"Correo electrónico: {d.get('correo_electronico', '')}"),
            cls._linea(f"Dirección: {direccion}"),
            cls._borde(),
            cls._linea("CLASIFICACIÓN", centrado=True),
            cls._borde(),
            cls._campo_doble("Tipo de solicitud", d.get("tipo_solicitud", ""),
                             "Canal de recepción", d.get("canal_recepcion", "")),
            cls._campo_doble("Tipo de mascota", d.get("tipo_mascota", ""),
                             "Campus", d.get("campus_relacionado", "")),
            cls._borde(),
            cls._linea("RESUMEN", centrado=True),
            cls._borde(),
            cls._linea(f"Asunto: {d.get('asunto_titulo', '')}"),
            cls._borde(),
        ]
        return "\n".join(filas) + "\n"

    @classmethod
    def generar(cls, datos):
        """Crea el .txt del radicado (ej. Peticion_16.txt) y devuelve su ruta como texto."""
        CARPETA_RADICADOS.mkdir(parents=True, exist_ok=True)
        nombre = f"{datos['tipo_solicitud']}_{datos['id']}.txt"
        ruta = CARPETA_RADICADOS / nombre
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            f.write(cls.construir(datos))
        return str(ruta)


# ---- Función con el nombre acordado por el grupo (la que usa main.py) ----
def generar_radicado(datos):
    """Crea el .txt del radicado y devuelve el nombre/ruta del archivo."""
    return c_radicado.generar(datos)


def texto_radicado(datos):
    """Devuelve el radicado como texto (sirve para mostrarlo en pantalla al consultar)."""
    return c_radicado.construir(datos)
