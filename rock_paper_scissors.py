import cv2
import mediapipe as mp
import random
import time
import numpy as np

# Inicializar MediaPipe para detección de manos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)

# Inicializar la captura de video
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara. Verifica que esté conectada.")
    exit()

# Opciones del juego
choices = ["Piedra", "Papel", "Tijera"]

# Variables de estado
player_score = 0
ai_score = 0
countdown = 1.5  # Contador reducido a 1.5 segundos
last_time = time.time()
play_processed = False
player_choice = None
ai_choice = None
result = None
last_result_time = 0
show_instructions = True
instructions_start_time = time.time()
player_history = []  # Historial de jugadas del jugador

# Función para detectar el gesto de la mano
def detect_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    fingers_up = 0
    if index_tip.y < landmarks[6].y:
        fingers_up += 1
    if middle_tip.y < landmarks[10].y:
        fingers_up += 1
    if ring_tip.y < landmarks[14].y:
        fingers_up += 1
    if pinky_tip.y < landmarks[18].y:
        fingers_up += 1

    if fingers_up == 0:
        return "Piedra"
    elif fingers_up == 4:
        return "Papel"
    elif fingers_up == 2 and index_tip.y < landmarks[6].y and middle_tip.y < landmarks[10].y:
        return "Tijera"
    return None

# Función para determinar el ganador
def determine_winner(player_choice, ai_choice):
    global player_score, ai_score
    if player_choice == ai_choice:
        return "Empate"
    elif (player_choice == "Piedra" and ai_choice == "Tijera") or \
         (player_choice == "Papel" and ai_choice == "Piedra") or \
         (player_choice == "Tijera" and ai_choice == "Papel"):
        player_score += 1
        return "¡Ganaste!"
    else:
        ai_score += 1
        return "Perdiste"

# Función para elegir la jugada de la IA basada en el historial
def ai_choose_move(player_history):
    if not player_history:
        # Sesgo inicial: 40% Papel, 35% Tijera, 25% Piedra
        return random.choices(choices, weights=[0.25, 0.40, 0.35])[0]
    
    # Contar frecuencia de jugadas del jugador (últimas 5)
    history_size = min(len(player_history), 5)
    recent_moves = player_history[-history_size:]
    rock_count = recent_moves.count("Piedra")
    paper_count = recent_moves.count("Papel")
    scissors_count = recent_moves.count("Tijera")
    
    # Calcular probabilidades para contrarrestar
    total = rock_count + paper_count + scissors_count
    if total == 0:
        total = 1
    weights = [
        paper_count / total,    # Contrarrestar Piedra con Papel
        scissors_count / total, # Contrarrestar Papel con Tijera
        rock_count / total      # Contrarrestar Tijera con Piedra
    ]
    
    # Normalizar pesos y agregar un pequeño factor aleatorio
    weights = [w + 0.1 for w in weights]  # Evitar ceros
    total = sum(weights)
    weights = [w / total for w in weights]
    
    return random.choices(choices, weights=weights)[0]

# Función para dibujar texto con fondo
def draw_text_with_background(frame, text, position, font, scale, text_color, bg_color, thickness):
    text_size, _ = cv2.getTextSize(text, font, scale, thickness)
    text_w, text_h = text_size
    x, y = position
    padding = 3
    cv2.rectangle(frame, (x - padding, y - text_h - padding), 
                 (x + text_w + padding, y + padding), bg_color, -1)
    cv2.putText(frame, text, position, font, scale, text_color, thickness)

# Configurar ventana más grande
cv2.namedWindow("Piedra, Papel o Tijera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Piedra, Papel o Tijera", 1280, 720)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el video. Verifica la cámara.")
        break

    # Escalar el fotograma para que coincida con el tamaño de la ventana
    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Detectar gesto si hay una mano
    current_player_choice = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            current_player_choice = detect_gesture(hand_landmarks.landmark)
    else:
        draw_text_with_background(frame, "No se detecta mano", (10, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), (255, 255, 255, 100), 1)

    # Mostrar instrucciones iniciales durante 5 segundos
    if show_instructions and (time.time() - instructions_start_time < 5):
        instructions = [
            "Piedra, Papel o Tijera",
            "Muestra tu gesto frente a la cámara:",
            "- Piedra: Puño cerrado",
            "- Papel: Mano abierta",
            "- Tijera: Índice y medio extendidos",
            "Presiona 'q' para salir, 'r' para reiniciar puntaje"
        ]
        for i, line in enumerate(instructions):
            draw_text_with_background(frame, line, (10, 30 + i * 20), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), (0, 0, 0, 100), 1)
    else:
        show_instructions = False

    # Actualizar contador cada 0.5 segundos para mayor precisión
    current_time = time.time()
    if current_time - last_time >= 0.5:
        countdown -= 0.5
        last_time = current_time
        play_processed = False

    # Cuando el contador llega a 0, procesar la jugada
    if countdown <= 0:
        if current_player_choice:
            player_choice = current_player_choice
            player_history.append(player_choice)
            ai_choice = ai_choose_move(player_history)
            result = determine_winner(player_choice, ai_choice)
            last_result_time = current_time
            play_processed = True
        else:
            result = "No se detectó gesto válido"
            last_result_time = current_time
            play_processed = True
        countdown = 1.5  # Reiniciar contador

    # Dibujar barra de progreso para el contador (más pequeña)
    bar_width = int((1.5 - countdown) * (frame.shape[1] - 20) / 1.5)
    cv2.rectangle(frame, (10, frame.shape[0] - 20), 
                 (10 + bar_width, frame.shape[0] - 10), (0, 255, 0), -1)
    cv2.rectangle(frame, (10, frame.shape[0] - 20), 
                 (frame.shape[1] - 10, frame.shape[0] - 10), (255, 255, 255), 1)

    # Dibujar borde rojo cuando la jugada se procesa
    if play_processed:
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 3)

    # Mostrar información en la pantalla (textos más pequeños)
    draw_text_with_background(frame, f"Contador: {countdown:.1f}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), (0, 0, 0, 100), 2)
    draw_text_with_background(frame, "¡Prepárate!", (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), (0, 0, 0, 100), 1)
    draw_text_with_background(frame, f"Puntaje - Tú: {player_score}  IA: {ai_score}", (10, frame.shape[0] - 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), (0, 0, 0, 100), 1)

    # Mostrar elecciones y resultado
    if player_choice:
        draw_text_with_background(frame, f"Tú: {player_choice}", (10, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), (0, 0, 0, 100), 1)
    if ai_choice:
        draw_text_with_background(frame, f"IA: {ai_choice}", (10, 130), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), (0, 0, 0, 100), 1)
    if result:
        draw_text_with_background(frame, f"Resultado: {result}", (10, 160), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), (0, 0, 0, 100), 1)
        if play_processed:
            draw_text_with_background(frame, "¡Jugada procesada!", (10, 190), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), (0, 0, 0, 100), 1)

    # Mostrar la ventana
    cv2.imshow("Piedra, Papel o Tijera", frame)

    # Manejar teclas
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        player_score = 0
        ai_score = 0
        player_history = []  # Reiniciar historial

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
hands.close()