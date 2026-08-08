"""Minimal VC model: modifies reference audio slightly to demonstrate pipeline.
If reference audio is provided, it will apply a downpitch + robotization.
If not, generates a short robotic tone.
"""
import numpy as np
from ..audio.audio_io import save_wav, load_wav
import os

class VCModel:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate

    def convert(self, ref_path=None, out_path="output_vc.wav"):
        sr = self.sample_rate
        if ref_path:
            audio, r_sr = load_wav(ref_path)
            # resample simple nearest (if needed)
            if r_sr != sr:
                # naive resample by interpolation
                import numpy as np
                duration = len(audio)/r_sr
                new_len = int(duration*sr)
                audio = np.interp(
                    np.linspace(0, len(audio), new_len, endpoint=False),
                    np.arange(len(audio)),
                    audio
                )
            # apply pitch shift by speeding up then slowing with repeat (lower pitch)
            audio = audio.astype(float)
            # simple robotic effect: blocky quantize
            factor = 16
            audio = np.repeat(audio[::factor], factor)[:len(audio)]
            # small ring modulation
            t = np.linspace(0, len(audio)/sr, num=len(audio), endpoint=False)
            audio = audio * (0.8 * np.sign(np.sin(2*np.pi*30*t)))
        else:
            # generate short robotic beep
            t = np.linspace(0, 0.8, int(sr*0.8), endpoint=False)
            audio = 0.6 * np.sign(np.sin(2*np.pi*220*t))
            # bitcrush
            audio = np.repeat(audio[::8], 8)[:len(audio)]
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        save_wav(out_path, audio, sr)
        return out_path
