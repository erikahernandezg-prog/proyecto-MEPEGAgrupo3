# Manual de Usuario – Burbuja Pets

Este manual explica cómo usar el sistema de consola **Burbuja Pets** para gestionar PQRS (Peticiones, Quejas, Reclamos y Sugerencias).

## 1. Cómo abrir el programa
1. Abre la terminal o consola en la carpeta del proyecto.
2. Ejecuta el archivo principal con Python:
   `python main.py` (o `python src/main.py`, según la ubicación del archivo).
3. Espera a que cargue la pantalla inicial del sistema.

> *[Captura de pantalla: pantalla al abrir el programa]*[cite: 3]

## 2. Cómo iniciar sesión
1. El sistema te pedirá tu **usuario** (o correo) y tu **contraseña**[cite: 3].
2. Escribe tus datos autorizados y presiona **Enter**[cite: 3].
3. Si ingresas mal los datos **3 veces seguidas**, el programa se bloqueará por **30 segundos** con una cuenta regresiva[cite: 3].
4. Al entrar correctamente, el sistema guardará tu sesión para registrar quién hizo cada movimiento[cite: 3].

> *[Captura de pantalla: inicio de sesión]*[cite: 3]

## 3. Cómo registrar una PQRS
1. En el menú principal, elige la opción **1. Registrar PQRS**[cite: 3].
2. Responde los datos que te pide el sistema uno por uno (nombre, documento, teléfono, correo, dirección si aplica, tipo de solicitud, canal, asunto, descripción, tipo de mascota y campus)[cite: 3].
3. Si escribes un dato con formato incorrecto (por ejemplo, un correo sin `@` o un teléfono que no tenga 10 números), el programa te pedirá corregir solo ese dato[cite: 3].
4. Al terminar, el sistema asigna el estado **Registrada**, calcula la fecha máxima de respuesta (15 días), guarda la PQRS y genera el comprobante de radicado[cite: 3].

> *[Captura de pantalla: registro de PQRS y radicado generado]*[cite: 3]

## 4. Cómo consultar una PQRS
1. En el menú principal, selecciona la opción **2. Consultar PQRS**[cite: 3].
2. Escribe el **tipo** (`Peticion`, `Queja`, `Reclamo` o `Sugerencia`) y presiona **Enter**[cite: 3].
3. Escribe el **número de ID** de la PQRS que quieres buscar[cite: 3].
4. En pantalla aparecerá la información de ese registro[cite: 3].

> *[Captura de pantalla: consulta de una PQRS]*[cite: 3]

## 5. Cómo cambiar el estado de una PQRS
1. En el menú principal, elige la opción **3. Cambiar estado**[cite: 3].
2. Indica el tipo de PQRS, el ID y el nuevo estado[cite: 3].
3. Ten en cuenta que el cambio solo se permite en este orden:
   **Registrada → En proceso → Solucionada**[cite: 3].
4. Si intentas saltarte un paso o devolver un estado, el sistema no lo permitirá[cite: 3].

> *[Captura de pantalla: cambio de estado de una PQRS]*[cite: 3]

## 6. Cómo ver las estadísticas
1. En el menú principal, selecciona la opción **4. Estadísticas**[cite: 3].
2. Podrás ver los cálculos estadísticos (como el promedio de días de respuesta, cantidades por categoría y PQRS próximas a vencer o vencidas) y los gráficos generados en Python[cite: 3].

> *[Captura de pantalla: estadísticas y gráficos]*[cite: 3]

## Salir del programa
Para cerrar el sistema, elige la opción **5. Salir** en el menú principal[cite: 3].
