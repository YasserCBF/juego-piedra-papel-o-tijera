# Juego de Piedra, Papel o Tijera con Detección de Gestos

Este es un juego interactivo de "Piedra, Papel o Tijera" que utiliza la cámara de tu computadora para detectar gestos de la mano en tiempo real, permitiéndote jugar contra una IA que elige jugadas aleatoriamente. El juego está implementado en Python usando OpenCV para la captura de video y MediaPipe para la detección de gestos.

## Características
- **Detección de gestos**: Reconoce "Piedra" (puño cerrado), "Papel" (mano abierta) y "Tijera" (dedos índice y medio extendidos).
- **Interfaz visual**: Muestra un contador, una barra de progreso, el puntaje (jugador vs. IA), y el resultado de cada ronda.
- **Interacción profesional**: Textos pequeños y no intrusivos, ventana grande (1280x720), instrucciones iniciales, y un borde rojo para indicar cuando se procesa una jugada.
- **Controles**: Presiona 'q' para salir, 'r' para reiniciar el puntaje.
- **Robustez**: Maneja casos en los que no se detecta un gesto o la cámara no funciona.

## Requisitos
- **Sistema operativo**: Windows, macOS o Linux.
- **Python**: Versión 3.9 (recomendada para compatibilidad).
- **Anaconda**: Para gestionar el entorno virtual y las dependencias.
- **Cámara**: Una cámara web funcional conectada al dispositivo.

## Instalación
1. **Instala Anaconda**:
   - Descarga e instala Anaconda desde [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution).
   - Asegúrate de tener Anaconda Prompt configurado.

2. **Crea un entorno virtual**:
   Abre Anaconda Prompt y ejecuta:
   ```bash
   conda create -n rock_paper_scissors python=3.9
   ```

3. **Activa el entorno**:
   ```bash
   conda activate rock_paper_scissors
   ```

4. **Instala las dependencias**:
   ```bash
   pip install opencv-python==4.10.0.84 mediapipe==0.10.14
   ```

5. **Guarda el código**:
   - Copia el archivo `rock_paper_scissors_pro.py` (proporcionado en el proyecto) en el directorio de tu elección.

## Uso
1. **Asegúrate de que el entorno esté activado**:
   ```bash
   conda activate rock_paper_scissors
   ```

2. **Ejecuta el juego**:
   Navega al directorio donde guardaste `rock_paper_scissors_pro.py` y ejecuta:
   ```bash
   python rock_paper_scissors_pro.py
   ```

3. **Cómo jugar**:
   - Al iniciar, se muestran instrucciones durante 5 segundos:
     - **Piedra**: Puño cerrado.
     - **Papel**: Mano abierta con todos los dedos extendidos.
     - **Tijera**: Dedos índice y medio extendidos.
   - Una ventana de 1280x720 muestra el video de la cámara.
   - Haz un gesto frente a la cámara. Cada 3 segundos, el juego detecta tu gesto, la IA elige una jugada, y se muestra el resultado.
   - Observa el contador y la barra de progreso en la pantalla. Un borde rojo y el mensaje "¡Jugada procesada!" indican que se ha registrado tu jugada.
   - El puntaje (Tú vs. IA) se actualiza automáticamente.
   - **Controles**:
     - Presiona 'q' para salir.
     - Presiona 'r' para reiniciar el puntaje.

## Solución de problemas
- **La cámara no se abre**:
  - Asegúrate de que la cámara esté conectada y no esté siendo utilizada por otra aplicación.
  - Prueba cambiar el índice de la cámara en el código (`cv2.VideoCapture(0)` a `cv2.VideoCapture(1)` o `cv2.VideoCapture(2)`).
- **No se detectan los gestos**:
  - Asegúrate de tener buena iluminación.
  - Ajusta `min_detection_confidence` en la línea `hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)` (por ejemplo, a `0.5` para mayor sensibilidad o `0.8` para mayor precisión).
- **Errores de dependencias**:
  - Verifica que `opencv-python` y `mediapipe` estén instalados con:
    ```bash
    pip list
    ```
  - Si no están, repite la instalación en el entorno activo.
- **Textos tapan el rostro**:
  - Los textos ya están diseñados para ser pequeños y estar en las esquinas. Si aún son intrusivos, edita la escala de la fuente en el código (por ejemplo, cambia `0.8` a `0.5` en `draw_text_with_background`).

## Personalización
Para ajustar el juego, puedes modificar el código:
- **Tiempo del contador**: Cambia la variable `countdown = 3` por otro valor (por ejemplo, `5` para 5 segundos).
- **Tamaño de la ventana**: Edita `cv2.resizeWindow("Piedra, Papel o Tijera", 1280, 720)` y `frame = cv2.resize(frame, (1280, 720))` para un tamaño diferente (por ejemplo, `1920, 1080`).
- **Tamaño de los textos**: Ajusta los valores de `scale` en las llamadas a `draw_text_with_background` (por ejemplo, de `0.6` a `0.4` para textos aún más pequeños).

## Contribuciones
Si deseas contribuir, puedes:
- Mejorar la detección de gestos con un modelo de machine learning personalizado.
- Agregar sonidos o imágenes para representar las elecciones.
- Implementar un límite de rondas o un modo multijugador.

## Licencia
Este proyecto es de código abierto bajo la licencia MIT.



