import numpy as np
import sounddevice as sd

class Synth:
    def __init__(self, sample_rate=44100, duration=0.1):
        self.sample_rate = sample_rate
        self.duration = duration

    def generate_tone(self, freq, volume):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        wave = np.sin(freq * 2 * np.pi * t)
        return wave * volume

    def play_tone(self, freq, volume):
        tone = self.generate_tone(freq, volume)
        sd.play(tone, samplerate=self.sample_rate, blocking=True)
