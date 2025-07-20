# theremin-mediapipe/src/main.py

import cv2
from pythonosc import udp_client
import time

# Importar as classes dos outros módulos
from src.hand_tracker import HandTracker
from src.theremin_controller import ThereminController
# from src.fractal import FractalVisualizer # Descomente se for usar a visualização fractal

def main():
    # --- Configuração OSC ---
    OSC_ADDRESS = "/play_note" 
    SONIC_PI_IP = "127.0.0.1" 
    SONIC_PI_PORT = 4560      # <<<<<< Aqui está a definição correta

    client = udp_client.SimpleUDPClient(SONIC_PI_IP, SONIC_PI_PORT) # CORREÇÃO: Usar SONIC_PI_PORT aqui

    # --- Inicializar Rastreador de Mãos e Controlador de Theremin ---
    tracker = HandTracker(max_hands=2, model_complexity=1) 
    controller = ThereminController() 
    # fractal = FractalVisualizer() # Descomente se for usar a visualização fractal

    cap = cv2.VideoCapture(0) # Tenta abrir a câmera padrão
    if not cap.isOpened():
        print("ERRO: Não foi possível abrir a câmera. Verifique se está conectada e não em uso.")
        return

    print("Câmera aberta. Inicie o Sonic Pi e o código de recepção OSC. Pressione 'ESC' para sair.")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERRO: Falha ao ler quadro da câmera. Saindo...")
                break

            # Processar o frame e obter os resultados do MediaPipe
            results, frame_processed_for_display = tracker.process_frame(frame)
            
            # Valores padrão para pitch e volume
            current_pitch = controller.MIDI_NOTE_MIN 
            current_volume = 0.0 # Mudo por padrão

            hand_detected_this_frame = False

            if results.multi_hand_landmarks and results.multi_handedness:
                # Obter pitch e volume do controlador de theremin
                current_pitch, current_volume, hand_detected_this_frame = controller.get_theremin_params(
                    results.multi_hand_landmarks, results.multi_handedness
                )
                
                # Desenha os landmarks em todas as mãos detectadas com os estilos padrão
                for hand_landmarks in results.multi_hand_landmarks:
                    tracker.draw_hand_landmarks(frame_processed_for_display, hand_landmarks)
            
            # --- ENVIO DA MENSAGEM OSC ---
            try:
                client.send_message(OSC_ADDRESS, [current_pitch, current_volume])
                # print(f"OSC SENT -> Endereço: {OSC_ADDRESS}, Dados: [Pitch={current_pitch}, Volume={current_volume:.4f}]")
            except Exception as osc_e:
                print(f"ERRO OSC: Não foi possível enviar mensagem: {osc_e}")

            # --- Visualização e Controle de Loop ---
            # if hand_detected_this_frame:
            #     normalized_pitch_for_fractal = (current_pitch - controller.MIDI_NOTE_MIN) / (controller.MIDI_NOTE_MAX - controller.MIDI_NOTE_MIN)
            #     fractal.draw(normalized_pitch_for_fractal) 
            
            cv2.imshow("Theremin Cam (Sonic Pi)", frame_processed_for_display)
            
            # Pressionar 'ESC' (código 27) para sair
            if cv2.waitKey(1) & 0xFF == 27:
                print("Tecla 'ESC' pressionada. Saindo...")
                break
            
            # Pequeno delay para controlar a taxa de quadros e o consumo de CPU
            time.sleep(0.05) # ~20 FPS

    except Exception as e:
        print(f"Ocorreu um erro inesperado no loop principal: {e}")

    finally:
        print("Liberando recursos da câmera e fechando janelas.")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()