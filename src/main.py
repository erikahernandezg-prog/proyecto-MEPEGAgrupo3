# main.py
# Menú principal de Burbuja Pets. Une todos los módulos.

from datetime import datetime, timedelta

import login
import validaciones
import archivos
import radicado
import reportes
import graficos

DIAS_RESPUESTA = 15

# Valores permitidos (los mismos de los archivos del profe).
TIPOS_SOLICITUD = ["Peticion", "Queja", "Reclamo", "Sugerencia"]
TIPOS_DOCUMENTO = ["CC", "TI", "CE", "PP", "NIT"]
TIPOS_TELEFONO = ["Celular", "Fijo", "Corporativo", "Otro"]
CANALES = ["Presencial", "Correo electrónico", "Página web",
           "Teléfono", "Redes sociales", "Otro"]
TIPOS_MASCOTA = ["Perro", "Gato", "Otro"]
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


def pedir_opcion(lista, mensaje):
    """Muestra una lista numerada y devuelve el valor elegido."""
    print(mensaje)
    for i, valor in enumerate(lista, start=1):
        print(f"  {i}. {valor}")
    while True:
        entrada = input("Elige una opción: ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= len(lista):
            return lista[int(entrada) - 1]
        print("Opción inválida. Intenta de nuevo.")


def pedir_dato(mensaje, funcion_validadora):
    """Pide un dato hasta que la función de validación devuelva True."""
    while True:
        valor = input(mensaje).strip()
        if funcion_validadora(valor):
            return valor
        print("Dato inválido. Intenta de nuevo.")


def registrar_pqrs(usuario_registro):
    """Pide los datos, valida, guarda la PQRS y genera el radicado."""
    print("\n--- REGISTRAR PQRS ---")
    datos = {}

    datos["nombre_completo"] = pedir_dato(
        "Nombre completo: ", validaciones.validar_nombre)
    datos["tipo_documento"] = pedir_opcion(
        TIPOS_DOCUMENTO, "Tipo de documento:")
    datos["numero_documento"] = pedir_dato(
        "Número de documento: ", validaciones.validar_documento)
    datos["tipo_telefono"] = pedir_opcion(
        TIPOS_TELEFONO, "Tipo de teléfono:")
    datos["telefono_contacto"] = pedir_dato(
        "Teléfono (10 dígitos): ", validaciones.validar_telefono)
    datos["correo_electronico"] = pedir_dato(
        "Correo electrónico: ", validaciones.validar_correo)
    datos["direccion"] = pedir_dato(
        "Dirección (opcional): ", validaciones.validar_direccion) or "N/A"
    datos["tipo_solicitud"] = pedir_opcion(
        TIPOS_SOLICITUD, "Tipo de solicitud:")
    datos["canal_recepcion"] = pedir_opcion(
        CANALES, "Canal de recepción:")
    datos["asunto_titulo"] = pedir_dato(
        "Asunto: ", validaciones.validar_asunto)
    datos["descripcion_detallada"] = pedir_dato(
        "Descripción: ", validaciones.validar_descripcion)
    datos["tipo_mascota"] = pedir_opcion(
        TIPOS_MASCOTA, "Tipo de mascota:")
    datos["campus_relacionado"] = pedir_opcion(
        CAMPUS, "Campus relacionado:")

    # Fechas y estado.
    ahora = datetime.now()
    datos["fecha_radicacion"] = ahora.strftime("%Y-%m-%d %H:%M:%S")
    datos["fecha_maxima_respuesta"] = (
        ahora + timedelta(days=DIAS_RESPUESTA)).strftime("%Y-%m-%d %H:%M:%S")
    datos["estado_peticion"] = "Registrada"
    datos["usuario_registro"] = usuario_registro

    tipo = datos["tipo_solicitud"]
    # El ID lo asigna archivos.py al guardar.
    datos["id"] = archivos.obtener_siguiente_id(tipo)

    archivos.guardar_pqrs(tipo, datos)
    nombre_archivo = radicado.generar_radicado(datos)
    print(f"\nPQRS registrada con ID {datos['id']}.")
    print(f"Radicado generado: {nombre_archivo}")


def consultar_pqrs():
    """Pregunta tipo e ID y muestra esa PQRS."""
    print("\n--- CONSULTAR PQRS ---")
    tipo = pedir_opcion(TIPOS_SOLICITUD, "Tipo de solicitud:")
    entrada = input("Número de ID: ").strip()
    if not entrada.isdigit():
        print("ID inválido.")
        return
    id_buscado = int(entrada)

    for pqrs in archivos.leer_pqrs(tipo):
        if int(pqrs.get("id", 0)) == id_buscado:
            print("\n--- PQRS ENCONTRADA ---")
            for campo, valor in pqrs.items():
                print(f"{campo}: {valor}")
            return
    print("No se encontró esa PQRS.")


def cambiar_estado():
    """Cambia el estado respetando el flujo Registrada -> En proceso -> Solucionada."""
    print("\n--- CAMBIAR ESTADO ---")
    tipo = pedir_opcion(TIPOS_SOLICITUD, "Tipo de solicitud:")
    entrada = input("Número de ID: ").strip()
    if not entrada.isdigit():
        print("ID inválido.")
        return
    id_pqrs = int(entrada)

    nuevo = pedir_opcion(
        ["En proceso", "Solucionada"], "Nuevo estado:")

    # Se busca la PQRS para saber si existe y cuál es su estado actual.
    pqrs = None
    for registro in archivos.leer_pqrs(tipo):
        if registro["id"].strip() == str(id_pqrs):
            pqrs = registro
            break
    if pqrs is None:
        print("No existe esa PQRS.")
        return

    if archivos.actualizar_estado(tipo, id_pqrs, nuevo):
        print(f"Estado actualizado: {pqrs['estado_peticion']} -> {nuevo}")
        # Días transcurridos desde que se radicó la PQRS hasta hoy
        radicada = datetime.strptime(pqrs["fecha_radicacion"], "%Y-%m-%d %H:%M:%S")
        dias = (datetime.now() - radicada).days
        if nuevo == "Solucionada":
            print(f"Fecha de respuesta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Días que tomó dar respuesta: {dias}")
        else:
            print(f"Días transcurridos desde la radicación: {dias}")
    else:
        print(f"No se permite pasar de '{pqrs['estado_peticion']}' a '{nuevo}'.")
        print("El orden es: Registrada -> En proceso -> Solucionada.")


def mostrar_menu():
    """Muestra el menú principal y devuelve la opción elegida."""
    print("\n========================================")
    print("        BURBUJA PETS - MEPEGA")
    print("========================================")
    print("1. Registrar PQRS")
    print("2. Consultar PQRS")
    print("3. Cambiar estado")
    print("4. Estadísticas")
    print("5. Salir")
    while True:
        opcion = input("Elige una opción: ").strip()
        if opcion in ["1", "2", "3", "4", "5"]:
            return opcion
        print("Opción inválida. Intenta de nuevo.")


def main():
    """Punto de entrada del programa."""
    archivos.preparar_archivos()  # agrega la columna fecha_respuesta si falta
    usuario = login.iniciar_sesion()
    if usuario is None:
        print("No se pudo iniciar sesión. Saliendo.")
        return

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            registrar_pqrs(usuario)
        elif opcion == "2":
            consultar_pqrs()
        elif opcion == "3":
            cambiar_estado()
        elif opcion == "4":
            reportes.mostrar_reporte()
            print("Reporte guardado en:", reportes.exportar_reporte())
            graficos.mostrar_graficos()
        elif opcion == "5":
            print("Hasta luego.")
            break


if __name__ == "__main__":
    main()
