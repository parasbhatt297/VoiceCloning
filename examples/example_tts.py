"""Example usage: generate robotic TTS from text."""
from mainFolder.inference import tts_infer
import sys

def main():
    text = "Hello, this is a robotic test." if len(sys.argv) < 2 else " ".join(sys.argv[1:])
    out = tts_infer(text, out_path="examples/output_tts.wav")
    print("Generated:", out)

if __name__ == "__main__":
    main()
