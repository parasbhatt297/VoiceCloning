"""Example usage: run minimal VC conversion (robotic)"""
from mainFolder.inference import vc_infer
import sys

def main():
    ref = None
    if len(sys.argv) >= 2:
        ref = sys.argv[1]
    out = vc_infer(ref_path=ref, out_path="examples/output_vc.wav")
    print("Generated:", out)

if __name__ == "__main__":
    main()
