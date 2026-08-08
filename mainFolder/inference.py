"""Unified inference interface for minimal demo."""
from .tts import TTSModel
from .vc import VCModel

def tts_infer(text, out_path="output_tts.wav"):
    model = TTSModel()
    return model.synthesize(text, out_path=out_path)

def vc_infer(ref_path=None, out_path="output_vc.wav"):
    model = VCModel()
    return model.convert(ref_path=ref_path, out_path=out_path)
