# validaciones.py
# Responsable: Darci Vanessa Londoño Ortiz (Control de calidad / Validaciones)
# Requisitos: RF-04 (datos del solicitante) y RF-05 (información de la PQRS)
#
# Cada función recibe un texto y responde:
#   True  -> el dato está bien
#   False -> el dato está mal (el programa lo vuelve a pedir)

from datetime import datetime

# Listas de valores permitidos (las mismas que usan los archivos del profe)
TIPOS_DOCUMENTO = ["CC", "TI", "CE", "PP", "NIT"]
TIPOS_TELEFONO = ["Celular", "Fijo", "Corporativo", "Otro"]
TIPOS_SOLICITUD = ["Peticion", "Queja", "Reclamo", "Sugerencia"]
CANALES = ["Presencial", "Correo electrónico", "Página web", "Teléfono", "Redes sociales", "Otro"]
MASCOTAS = ["Perro", "Gato", "Otro"]
CAMPUS = [
    "Campus Medellín - Ciudad Universitaria",
    "Campus Medellín - Edificio San Ignacio",
    "Campus en el Área de la salud",
    "Campus Medellín - Casas Patrimoniales",
    "Campus Medellín - Antigua Escuela de Derecho",
    "Campus Medellín - Ciudadela Robledo",
    "Campus Medellín - Edificio Antioquia",
    "Campus Medellín - Edificio de Extensión",
    "Campus Medellín - Sede de Posgrado",
]


def validar_nombre(texto):
    """Nombre: de 3 a 100 caracteres; solo letras (con tildes y ñ), espacios, ' y -. Sin números."""
    texto = texto.strip()
    if len(texto) < 3 or len(texto) > 100:
        return False
    for letra in texto:
        # isalpha() es True para letras, incluidas á, é, í, ó, ú y ñ
        if not (letra.isalpha() or letra in " '-"):
            return False
    return True


def validar_documento(texto):
    """Número de documento: solo números, entre 3 y 15 dígitos."""
    texto = texto.strip()
    return texto.isdigit() and 3 <= len(texto) <= 15


def validar_telefono(texto):
    """Teléfono: exactamente 10 dígitos."""
    texto = texto.strip()
    return texto.isdigit() and len(texto) == 10


def validar_correo(texto):
    """Correo: máximo 254 caracteres, sin espacios, una sola @ y un dominio con punto (usuario@dominio.com)."""
    texto = texto.strip()
    if len(texto) > 254 or " " in texto or texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    if usuario == "" or "." not in dominio:
        return False
    # El dominio no puede empezar ni terminar en punto (ej: "correo." está mal)
    return not dominio.startswith(".") and not dominio.endswith(".")


def validar_direccion(texto):
    """Dirección: es opcional. Si se escribe, de 5 a 200 caracteres con letras, números y # - . / ,"""
    texto = texto.strip()
    if texto == "":
        return True  # vacía es válida: en el radicado aparecerá N/A
    if len(texto) < 5 or len(texto) > 200:
        return False
    for caracter in texto:
        if not (caracter.isalnum() or caracter in " #-./,"):
            return False
    return True


def validar_fecha(texto):
    """Fecha en formato AAAA-MM-DD (también acepta la hora). No puede ser una fecha futura."""
    texto = texto.strip()
    for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            fecha = datetime.strptime(texto, formato)
            return fecha <= datetime.now()
        except ValueError:
            pass  # no tenía ese formato: probamos con el siguiente
    return False


def validar_asunto(texto):
    """Asunto: de 5 a 150 caracteres."""
    texto = texto.strip()
    return 5 <= len(texto) <= 150


def validar_descripcion(texto):
    """Descripción: de 20 a 2000 caracteres; no puede estar vacía ni ser solo espacios."""
    texto = texto.strip()
    return 20 <= len(texto) <= 2000


def validar_opcion(texto, opciones):
    """Revisa que el usuario haya escogido un número de la lista (1, 2, 3...)."""
    texto = texto.strip()
    return texto.isdigit() and 1 <= int(texto) <= len(opciones)
