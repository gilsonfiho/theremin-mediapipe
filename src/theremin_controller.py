import numpy as np
import mediapipe as mp

class ThereminController:
    def __init__(self):
        # --- Configurações de Mapeamento ---
        self.MIDI_NOTE_MIN = 40  # Nota MIDI mais grave (aprox. C3)
        self.MIDI_NOTE_MAX = 90  # Nota MIDI mais aguda (aprox. A6)
        
        self.VOLUME_MIN = 0.1    # Volume mínimo audível
        self.VOLUME_MAX = 1.0    # Volume máximo

    def _map_value(self, value, in_min, in_max, out_min, out_max):
        if in_min == in_max:
            return out_min 
        
        clamped_value = max(in_min, min(value, in_max))
        return out_min + (float(clamped_value - in_min) / (in_max - in_min)) * (out_max - out_min)

    def get_theremin_params(self, multi_hand_landmarks, multi_handedness):
        current_pitch = self.MIDI_NOTE_MIN # Valor padrão
        current_volume = 0.0 # Valor padrão: Mudo

        hand_detected_this_frame = False

        if multi_hand_landmarks and multi_handedness:
            hand_detected_this_frame = True
            for i, hand_landmarks in enumerate(multi_hand_landmarks):
                if not hand_landmarks.landmark or \
                   len(hand_landmarks.landmark) <= mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP.value:
                    continue 

                if i >= len(multi_handedness) or not multi_handedness[i].classification:
                    continue

                label = multi_handedness[i].classification[0].label 
                index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                y_coord_normalized = index_finger_tip.y # 0=topo, 1=baixo da tela

                if label == "Right": # Mão Direita para Pitch
                    current_pitch = int(self._map_value(1 - y_coord_normalized, 0, 1, self.MIDI_NOTE_MIN, self.MIDI_NOTE_MAX))
                    
                elif label == "Left": # Mão Esquerda para Volume
                    current_volume = self._map_value(1 - y_coord_normalized, 0, 1, self.VOLUME_MIN, self.VOLUME_MAX)
                    current_volume = max(0.0, min(current_volume, 1.0)) # Clampa entre 0 e 1
        
        return current_pitch, current_volume, hand_detected_this_frame