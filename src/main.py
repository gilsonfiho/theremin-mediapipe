import cv2
from pythonosc import udp_client
import time

from src.hand_tracker import HandTracker, draw_hand_landmarks
from src.theremin_controller import ThereminController, MIDI_NOTE_MIN


# Configurações
OSC_ADDRESS = "/play_note"
SONIC_PI_IP = "127.0.0.1"
SONIC_PI_PORT = 4560
FRAME_DELAY = 0.05
ESC_KEY = 27


def setup_camera(index=0):
    """Inicializa câmera."""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Não foi possível abrir a câmera.")
    return cap


def setup_osc_client(ip=SONIC_PI_IP, port=SONIC_PI_PORT):
    """Cria cliente OSC."""
    return udp_client.SimpleUDPClient(ip, port)


def send_osc(client, address, pitch, volume):
    """Envia mensagem OSC."""
    try:
        client.send_message(address, [pitch, volume])
        return True
    except Exception as e:
        print(f"ERRO OSC: {e}")
        return False


def process_theremin_frame(tracker, controller, frame):
    """Processa frame do theremin."""
    results, frame_processed = tracker.process_frame(frame)

    pitch = controller.MIDI_NOTE_MIN
    volume = 0.0

    if results.multi_hand_landmarks and results.multi_handedness:
        pitch, volume, _ = controller.get_theremin_params(
            results.multi_hand_landmarks,
            results.multi_handedness
        )
        draw_hand_landmarks(frame_processed, results)

    return pitch, volume, frame_processed


def run_theremin(cap, tracker, controller, osc_client):
    """Loop principal."""
    print("✓ Theremin iniciado! Pressione 'ESC' para sair.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERRO: Falha ao ler frame.")
                break

            pitch, volume, frame_processed = process_theremin_frame(
                tracker, controller, frame
            )

            send_osc(osc_client, OSC_ADDRESS, pitch, volume)

            cv2.imshow("Theremin Cam (Sonic Pi)", frame_processed)

            if cv2.waitKey(1) & 0xFF == ESC_KEY:
                print("Saindo...")
                break

            time.sleep(FRAME_DELAY)

    except KeyboardInterrupt:
        print("\nInterrompido.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cleanup(cap)


def cleanup(cap):
    """Libera recursos."""
    print("Liberando recursos...")
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Função principal."""
    try:
        print("Inicializando theremin...")
        osc_client = setup_osc_client()
        tracker = HandTracker(max_hands=2)
        controller = ThereminController()
        cap = setup_camera()

        run_theremin(cap, tracker, controller, osc_client)

    except RuntimeError as e:
        print(f"\n❌ ERRO: {e}")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()
