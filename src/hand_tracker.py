import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import time
from pathlib import Path
import urllib.request
import os


MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
MODEL_PATH = Path("assets/hand_landmarker.task")


def download_model():
    """Baixa o modelo se não existir."""
    if MODEL_PATH.exists():
        print(f"✓ Modelo já existe: {MODEL_PATH}")
        return str(MODEL_PATH)

    print(f"⬇ Baixando modelo do MediaPipe...")
    MODEL_PATH.parent.mkdir(exist_ok=True)

    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print(f"✓ Modelo baixado com sucesso: {MODEL_PATH}")
        return str(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(
            f"Erro ao baixar modelo: {e}\nBaixe manualmente de: {MODEL_URL}")


def create_hand_detector(max_hands=2):
    """Cria detector de mãos com download automático."""
    model_path = download_model()

    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        num_hands=max_hands,
        running_mode=vision.RunningMode.VIDEO
    )

    return vision.HandLandmarker.create_from_options(options)


def process_frame(detector, frame):
    """Processa frame e retorna resultados."""
    frame_flipped = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms = int(time.time() * 1000)
    results = detector.detect_for_video(mp_image, timestamp_ms)

    # Compatibilidade com código antigo
    results.multi_hand_landmarks = results.hand_landmarks
    results.multi_handedness = results.handedness

    return results, frame_flipped


def get_segment_color(landmark_idx):
    """Retorna cor BGR para cada segmento da mão."""
    segment_colors = {
        # Polegar (índices 1-4): Ciano
        1: (255, 255, 0),  # Ciano
        2: (255, 255, 0),
        3: (255, 255, 0),
        4: (255, 255, 0),
        # Indicador (índices 5-8): Verde
        5: (0, 255, 0),  # Verde
        6: (0, 255, 0),
        7: (0, 255, 0),
        8: (0, 255, 0),
        # Médio (índices 9-12): Amarelo
        9: (0, 255, 255),  # Amarelo
        10: (0, 255, 255),
        11: (0, 255, 255),
        12: (0, 255, 255),
        # Anelar (índices 13-16): Magenta
        13: (255, 0, 255),  # Magenta
        14: (255, 0, 255),
        15: (255, 0, 255),
        16: (255, 0, 255),
        # Mínimo (índices 17-20): Vermelho
        17: (0, 0, 255),  # Vermelho
        18: (0, 0, 255),
        19: (0, 0, 255),
        20: (0, 0, 255),
        # Palma (índice 0): Branco
        0: (255, 255, 255),  # Branco
    }
    return segment_colors.get(landmark_idx, (255, 255, 255))


def draw_hand_landmarks(image, results):
    """Desenha landmarks das mãos com cores individuais por segmento."""
    if not results.hand_landmarks:
        return

    h, w, _ = image.shape

    for hand_landmarks in results.hand_landmarks:
        # Desenha conexões com cores por segmento
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Polegar
            (0, 5), (5, 6), (6, 7), (7, 8),  # Indicador
            (5, 9), (9, 10), (10, 11), (11, 12),  # Médio
            (9, 13), (13, 14), (14, 15), (15, 16),  # Anelar
            (13, 17), (17, 18), (18, 19), (19, 20),  # Mínimo
            (0, 17)  # Palma
        ]

        for start_idx, end_idx in connections:
            if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]
                start_pt = (int(start.x * w), int(start.y * h))
                end_pt = (int(end.x * w), int(end.y * h))
                # Usa cor do índice final para o segmento
                color = get_segment_color(end_idx)
                cv2.line(image, start_pt, end_pt, color, 2)

        # Desenha pontos com cores por segmento
        for idx, lm in enumerate(hand_landmarks):
            cx, cy = int(lm.x * w), int(lm.y * h)
            color = get_segment_color(idx)
            cv2.circle(image, (cx, cy), 5, color, -1)
            # Borda branca para melhor contraste
            cv2.circle(image, (cx, cy), 5, (255, 255, 255), 1)


# Classe para compatibilidade
class HandTracker:
    def __init__(self, max_hands=2, **kwargs):
        self.detector = create_hand_detector(max_hands)

    def process_frame(self, frame):
        return process_frame(self.detector, frame)

    def draw_hand_landmarks(self, image, hand_landmarks):
        # Cria um objeto results temporário
        class Results:
            pass
        results = Results()
        results.hand_landmarks = [hand_landmarks] if not isinstance(
            hand_landmarks, list) else hand_landmarks
        draw_hand_landmarks(image, results)
