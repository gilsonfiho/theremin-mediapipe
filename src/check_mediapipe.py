"""Script para diagnosticar a instalação do MediaPipe."""

import sys

print("=" * 60)
print("DIAGNÓSTICO DO MEDIAPIPE")
print("=" * 60)

# Verifica se MediaPipe está instalado
try:
    import mediapipe as mp
    print(f"✓ MediaPipe instalado")
    print(f"  Versão: {mp.__version__}")
    print(f"  Local: {mp.__file__}")
except ImportError as e:
    print(f"✗ MediaPipe NÃO instalado: {e}")
    sys.exit(1)

print("\n" + "-" * 60)
print("ATRIBUTOS DISPONÍVEIS:")
print("-" * 60)

# Lista todos os atributos do mediapipe
attrs = [a for a in dir(mp) if not a.startswith('_')]
for attr in attrs:
    print(f"  - {attr}")

print("\n" + "-" * 60)
print("TESTANDO IMPORTS:")
print("-" * 60)

# Testa imports comuns
tests = [
    ("mp.solutions", lambda: hasattr(mp, 'solutions')),
    ("mp.tasks", lambda: hasattr(mp, 'tasks')),
    ("mp.tasks.python", lambda: __import__('mediapipe.tasks.python')),
    ("mp.tasks.python.vision", lambda: __import__('mediapipe.tasks.python.vision')),
]

for name, test_func in tests:
    try:
        result = test_func()
        print(f"✓ {name}: Disponível")
    except Exception as e:
        print(f"✗ {name}: Indisponível ({type(e).__name__})")

print("\n" + "=" * 60)
print("RECOMENDAÇÃO:")
print("=" * 60)

if hasattr(mp, 'solutions'):
    print("Use: from mediapipe import solutions")
    print("API: solutions.hands.Hands()")
elif hasattr(mp, 'tasks'):
    print("Use: from mediapipe.tasks.python import vision")
    print("API: vision.HandLandmarker")
    print("\nATENÇÃO: Você precisa baixar o arquivo hand_landmarker.task")
    print("Link: https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task")
else:
    print("⚠ Versão do MediaPipe não reconhecida!")
    print("Tente: pip install mediapipe==0.10.14")

print("=" * 60)
