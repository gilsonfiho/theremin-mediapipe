# Constantes
MIDI_NOTE_MIN = 40
MIDI_NOTE_MAX = 90
VOLUME_MIN = 0.1
VOLUME_MAX = 1.0
INDEX_FINGER_TIP = 8


def map_value(value, in_min, in_max, out_min, out_max):
    """Mapeia valor de um range para outro."""
    if in_min == in_max:
        return out_min
    clamped = max(in_min, min(value, in_max))
    ratio = (clamped - in_min) / (in_max - in_min)
    return out_min + ratio * (out_max - out_min)


def get_hand_label(handedness_list, index):
    """Retorna label da mão (Left/Right)."""
    try:
        if not handedness_list or index >= len(handedness_list):
            return None

        hand = handedness_list[index]

        # Trata diferentes formatos
        if hasattr(hand, 'classification'):
            return hand.classification[0].label
        elif isinstance(hand, list) and len(hand) > 0:
            if hasattr(hand[0], 'label'):
                return hand[0].label
            elif hasattr(hand[0], 'category_name'):
                return hand[0].category_name

        return None
    except (AttributeError, IndexError, TypeError):
        return None


def get_finger_y(hand_landmarks):
    """Obtém coordenada Y do dedo indicador."""
    try:
        if isinstance(hand_landmarks, list):
            landmarks = hand_landmarks
        elif hasattr(hand_landmarks, 'landmark'):
            landmarks = hand_landmarks.landmark
        else:
            return None

        if len(landmarks) <= INDEX_FINGER_TIP:
            return None

        tip = landmarks[INDEX_FINGER_TIP]
        return tip.y if hasattr(tip, 'y') else None
    except (AttributeError, IndexError, TypeError):
        return None


def calculate_pitch(y_normalized):
    """Calcula pitch MIDI da posição Y."""
    return int(map_value(1 - y_normalized, 0, 1, MIDI_NOTE_MIN, MIDI_NOTE_MAX))


def calculate_volume(y_normalized):
    """Calcula volume da posição Y."""
    volume = map_value(1 - y_normalized, 0, 1, VOLUME_MIN, VOLUME_MAX)
    return max(0.0, min(volume, 1.0))


def get_theremin_params(multi_hand_landmarks, multi_handedness):
    """
    Extrai parâmetros do theremin.

    Returns:
        tuple: (pitch, volume, hand_detected)
    """
    pitch = MIDI_NOTE_MIN
    volume = 0.0
    hand_detected = False

    if not multi_hand_landmarks or not multi_handedness:
        return pitch, volume, hand_detected

    hand_detected = True

    for i, hand_landmarks in enumerate(multi_hand_landmarks):
        label = get_hand_label(multi_handedness, i)
        if not label:
            continue

        y_pos = get_finger_y(hand_landmarks)
        if y_pos is None:
            continue

        if label == "Right":
            pitch = calculate_pitch(y_pos)
        elif label == "Left":
            volume = calculate_volume(y_pos)

    return pitch, volume, hand_detected


# Classe para compatibilidade
class ThereminController:
    def __init__(self):
        self.MIDI_NOTE_MIN = MIDI_NOTE_MIN
        self.MIDI_NOTE_MAX = MIDI_NOTE_MAX
        self.VOLUME_MIN = VOLUME_MIN
        self.VOLUME_MAX = VOLUME_MAX

    def _map_value(self, value, in_min, in_max, out_min, out_max):
        return map_value(value, in_min, in_max, out_min, out_max)

    def get_theremin_params(self, multi_hand_landmarks, multi_handedness):
        return get_theremin_params(multi_hand_landmarks, multi_handedness)
