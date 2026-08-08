"""Simple WAV IO using the built-in wave module (16-bit PCM)."""
import wave, struct, os
import numpy as np

def save_wav(path, audio_float32, sr=22050):
    # clamp to [-1,1]
    a = np.asarray(audio_float32)
    a = a / max(1e-9, a.max() if a.max()>-a.min() else -a.min())
    a = (a * 32767).astype('<i2')  # little-endian 16-bit
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(a.tobytes())

def load_wav(path):
    with wave.open(path, 'rb') as wf:
        sr = wf.getframerate()
        n = wf.getnframes()
        frames = wf.readframes(n)
        import numpy as np
        a = np.frombuffer(frames, dtype='<i2').astype(np.float32) / 32767.0
        return a, sr
