# theremin-mediapipe/src/hand_tracker.py

import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5, model_complexity=1):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
            model_complexity=model_complexity
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles 
        self.mp_hands = mp.solutions.hands # Necessário para acessar as conexões de landmarks

    def process_frame(self, frame):
        # Inverte a imagem horizontalmente para uma visualização de espelho.
        frame_flipped = cv2.flip(frame, 1) 
        
        # Converte a imagem de BGR para RGB (MediaPipe usa RGB)
        image_rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
        
        # Define image como não gravável antes de processar para melhorar a performance
        image_rgb.flags.writeable = False
        results = self.hands.process(image_rgb)
        
        # Define image como gravável novamente para desenho e converte de volta para BGR
        image_rgb.flags.writeable = True
        frame_processed_for_display = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR) 
        
        return results, frame_processed_for_display

    def draw_hand_landmarks(self, image, hand_landmarks):
        # Usa os estilos de desenho padrão do MediaPipe para simplicidade
        self.mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )