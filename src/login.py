# login.py
# Módulo de autenticación de Burbuja Pets.
# Compara usuario/correo y contraseña contra data/Usuarios.txt.
# Bloquea 30 segundos tras 3 intentos fallidos.

import os
import time

CARPETA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_USUARIOS = os.path.join(CARPETA_BASE, "data", "Usuarios.txt")
MAX_INTENTOS = 3
SEGUNDOS_BLOQUEO = 30


def _cargar_usuarios():
    """Lee Usuarios.txt y devuelve una lista de diccionarios."""
    usuarios = []
    if not os.path.exists(RUTA_USUARIOS):
        return usuarios

    with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # La primera línea es el encabezado: se salta.
    for linea in lineas[1:]:
        linea = linea.strip()
        if not linea:
            continue
        campos = linea.split("|")
        if len(campos) < 6:
            continue
        usuarios.append({
            "usuario": campos[0].strip(),
            "nombre_completo": campos[1].strip(),
            "correo_institucional": campos[2].strip(),
            "contrasena": campos[3].strip(),
            "rol": campos[4].strip(),
            "estado": campos[5].strip(),
        })
    return usuarios


def iniciar_sesion():
    """
    Pide usuario (o correo) y contraseña.
    Devuelve el usuario que entró (string) o None si cancela.
    Tras 3 intentos fallidos, bloquea 30 segundos y vuelve a pedir.
    """
    usuarios = _cargar_usuarios()
    if not usuarios:
        print("No se encontró el archivo de usuarios.")
        return None

    while True:  # ciclo externo: permite reintentar tras el bloqueo
        intentos = 0
        while intentos < MAX_INTENTOS:
            print("\n--- INICIO DE SESIÓN ---")
            identificador = input("Usuario o correo (Enter para cancelar): ").strip()
            if identificador == "":
                print("Sesión cancelada.")
                return None

            contrasena = input("Contraseña: ").strip()

            encontrado = None
            for u in usuarios:
                if (u["usuario"].lower() == identificador.lower() or
                        u["correo_institucional"].lower() == identificador.lower()):
                    encontrado = u
                    break

            if encontrado is not None and encontrado["contrasena"] == contrasena:
                if encontrado["estado"].lower() != "activo":
                    print("El usuario no está activo.")
                    return None
                print(f"Bienvenido/a, {encontrado['nombre_completo']}.")
                return encontrado["usuario"]

            intentos += 1
            restantes = MAX_INTENTOS - intentos
            print(f"Datos incorrectos. Intentos restantes: {restantes}")

        # Se agotaron los 3 intentos: bloqueo con cuenta regresiva
        print(f"\nCuenta bloqueada por {SEGUNDOS_BLOQUEO} segundos...")
        for seg in range(SEGUNDOS_BLOQUEO, 0, -1):
            print(f"  {seg}...", end="\r")
            time.sleep(1)
        print("\nBloqueo terminado. Puede intentar de nuevo.")
        # El while True vuelve a empezar: pide usuario otra vez

if __name__ == "__main__":
    # Prueba rápida del módulo.
    usuario = iniciar_sesion()
    print("Usuario en sesión:", usuario)


