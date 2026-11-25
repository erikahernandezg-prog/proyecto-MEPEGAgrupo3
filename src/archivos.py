#archivos.py: Backend de lectura y escritura de las PQRS (Burbuja Pets).
#Responsable: Yanidis Yoela Arrieta Requeme

# Etete archivo maneja los 4 archivos planos (Peticion.txt, Queja.txt, Reclamo.txt, Sugerencia.txt)
# guardados en la carpeta data. Cada línea es una PQRS; los campos van separados por "|".


from pathlib import Path
from datetime import datetime

# Carpeta data, calculada de forma robusta sin importar desde dónde se ejecute
RUTA_DATA = Path(__file__).resolve().parent.parent / "data"

# Los 4 tipos válidos
TIPOS = ["Peticion", "Queja", "Reclamo", "Sugerencia"]

# Orden de los 19 campos de cada línea
# (los 18 del profe + "fecha_respuesta", que se llena al pasar a Solucionada)
CAMPOS = [
    "id", "nombre_completo", "tipo_documento", "numero_documento", "tipo_telefono",
    "telefono_contacto", "correo_electronico", "direccion", "tipo_solicitud",
    "fecha_radicacion", "canal_recepcion", "asunto_titulo", "descripcion_detallada",
    "tipo_mascota", "campus_relacionado", "fecha_maxima_respuesta", "estado_peticion",
    "usuario_registro", "fecha_respuesta",
]

# Flujo único permitido de estados
FLUJO_ESTADOS = ["Registrada", "En proceso", "Solucionada"]


class c_archivos:
    """Clase organizada y reutilizable que encapsula el acceso sencillo a los archivos planos."""

    @staticmethod
    def ruta_archivo(tipo):
        """Devuelve la ruta (Path) válida del archivo de un tipo; lanza error si el tipo no existe."""
        if tipo not in TIPOS:
            raise ValueError(f"Tipo inválido: {tipo!r}. Debe ser uno de {TIPOS}")
        return RUTA_DATA / f"{tipo}.txt"

    @staticmethod
    def _linea_a_registro(linea):
        """Convierte una línea limpia del archivo en un diccionario ordenado campo -> valor."""
        partes = linea.rstrip("\r\n").split("|")
        # Si faltan columnas se completan con vacío; si sobran se ignoran
        partes = (partes + [""] * len(CAMPOS))[:len(CAMPOS)]
        return dict(zip(CAMPOS, partes))

    @staticmethod
    def _registro_a_linea(datos):
        """Convierte un diccionario (o lista) en una línea de texto con los campos en orden."""
        if isinstance(datos, dict):
            valores = [datos.get(campo, "") for campo in CAMPOS]
        else:
            valores = list(datos)
        # Se quitan saltos de línea y barras internas para no romper la estructura del archivo
        return "|".join(str(v).replace("|", "/").replace("\n", " ").replace("\r", " ").strip()
                        for v in valores)

    @classmethod
    def leer(cls, tipo):
        """Lee todas las PQRS del archivo (saltando el encabezado) y devuelve una lista de diccionarios."""
        ruta = cls.ruta_archivo(tipo)
        if not ruta.exists():
            return []
        with open(ruta, "r", encoding="utf-8-sig") as f:
            lineas = f.readlines()[1:]  # la primera línea es el encabezado, no una PQRS
        # Comprensión de listas: una PQRS por cada línea no vacía
        return [cls._linea_a_registro(l) for l in lineas if l.strip()]

    @classmethod
    def siguiente_id(cls, tipo):
        """Devuelve el próximo ID consecutivo del archivo (último ID + 1, o 1 si está vacío)."""
        ids = [int(r["id"]) for r in cls.leer(tipo) if r["id"].strip().isdigit()]
        return max(ids) + 1 if ids else 1

    @classmethod
    def guardar(cls, tipo, datos):
        """Agrega la PQRS al final del archivo y devuelve el ID con el que quedó guardada."""
        ruta = cls.ruta_archivo(tipo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        # Si el archivo no existe o está vacío, se crea con su encabezado
        if not ruta.exists() or ruta.stat().st_size == 0:
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write("|".join(CAMPOS) + "\n")

        # Se asegura de que la última línea termine en salto para no pegar dos registros
        with open(ruta, "rb") as f:
            contenido = f.read()
        if not contenido.endswith(b"\n"):
            with open(ruta, "ab") as f:
                f.write(b"\n")

        # Si la PQRS no trae ID, se le asigna el siguiente consecutivo
        if isinstance(datos, dict):
            datos = dict(datos)
            if not str(datos.get("id", "")).strip():
                datos["id"] = cls.siguiente_id(tipo)
            id_guardado = datos["id"]
        else:
            id_guardado = datos[0]

        with open(ruta, "a", encoding="utf-8", newline="\n") as f:
            f.write(cls._registro_a_linea(datos) + "\n")
        return int(id_guardado)

    @classmethod
    def actualizar_estado(cls, tipo, id_pqrs, nuevo):
        """Cambia el estado de una PQRS respetando el flujo; True si cambió, False si no se permite."""
        if nuevo not in FLUJO_ESTADOS:
            return False
        ruta = cls.ruta_archivo(tipo)
        if not ruta.exists():
            return False

        with open(ruta, "r", encoding="utf-8-sig") as f:
            lineas = f.read().splitlines()

        cambiado = False
        for i in range(1, len(lineas)):  # desde 1 para saltar el encabezado
            if not lineas[i].strip():
                continue
            registro = cls._linea_a_registro(lineas[i])
            if registro["id"] == str(id_pqrs):
                actual = registro["estado_peticion"]
                # Solo se permite avanzar exactamente un paso en el flujo
                if actual in FLUJO_ESTADOS and \
                        FLUJO_ESTADOS.index(nuevo) == FLUJO_ESTADOS.index(actual) + 1:
                    registro["estado_peticion"] = nuevo
                    # Al solucionar, se guarda la fecha y hora de respuesta
                    if nuevo == "Solucionada":
                        registro["fecha_respuesta"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    lineas[i] = cls._registro_a_linea(registro)
                    cambiado = True
                break

        if cambiado:
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lineas) + "\n")
        return cambiado


    @classmethod
    def asegurar_columna_respuesta(cls):
        """Si un archivo todavía tiene el encabezado viejo de 18 campos, le agrega la columna
        fecha_respuesta (vacía) a todas las líneas. Solo se hace una vez por archivo."""
        for tipo in TIPOS:
            ruta = cls.ruta_archivo(tipo)
            if not ruta.exists():
                continue
            with open(ruta, "r", encoding="utf-8-sig") as f:
                lineas = f.read().splitlines()
            if not lineas or "fecha_respuesta" in lineas[0]:
                continue
            nuevas = ["|".join(CAMPOS)]
            for linea in lineas[1:]:
                if linea.strip():
                    nuevas.append(cls._registro_a_linea(cls._linea_a_registro(linea)))
            with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(nuevas) + "\n")


# ---- Funciones con los nombres acordados por el grupo (las que usa main.py) ----
def obtener_siguiente_id(tipo):
    """Devuelve el siguiente número de ID de ese archivo."""
    return c_archivos.siguiente_id(tipo)


def guardar_pqrs(tipo, datos):
    """Guarda la PQRS al final del archivo y devuelve su ID."""
    return c_archivos.guardar(tipo, datos)


def leer_pqrs(tipo):
    """Devuelve una lista con todas las PQRS de ese archivo (cada una es un diccionario)."""
    return c_archivos.leer(tipo)


def actualizar_estado(tipo, id, nuevo):
    """True si el estado cambió, False si el cambio no está permitido."""
    return c_archivos.actualizar_estado(tipo, id, nuevo)


def preparar_archivos():
    """Deja los 4 archivos con la columna fecha_respuesta (se llama al iniciar el programa)."""
    c_archivos.asegurar_columna_respuesta()
