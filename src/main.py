import argparse
from transform.caesar import shift_text
from script.parser import parse_shifted_text
from render.svg import merge_svgs

def main():
    parser = argparse.ArgumentParser(description="Script Engine: English to Custom Script Generator")
    parser.add_argument("text", type=str, help="The English text to convert")
    parser.add_argument("-o", "--output", type=str, default="output.svg", help="Output filename")
    
    args = parser.parse_args()
    
    print(f"Input Text: {args.text}")
    
    shifted = shift_text(args.text, shift=4)
    print(f"Cipher Text (+4): {shifted}")
    
    paths = parse_shifted_text(shifted)
    
    if paths:
        merge_svgs(paths, args.output)
    else:
        print("No valid glyphs found to render.")

if __name__ == "__main__":
    main()