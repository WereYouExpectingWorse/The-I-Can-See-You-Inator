import numpy as np
import sounddevice as sd

def play_live_tone(frequency, duration):
    fs = 44100  # Sample rate
    t = np.linspace(0, duration, int(fs * duration), False)
    
    # Generate a square wave (just like the GPIO toggling)
    tone = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))
    
    # Send it directly to the sound card
    sd.play(tone, fs)
    sd.wait()

# Example: A quick "Ding"
play_live_tone(660, 0.5)
