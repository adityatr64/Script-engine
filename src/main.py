import argparse
import sys
import eng_to_ipa as p
from script.parser import parse_ipa_text
from render.svg import merge_svgs

# Ensure UTF-8 output formatting for Windows consoles printing IPA Unicode
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Script Engine: English to Custom Script Generator")
    parser.add_argument("text", type=str, help="The English text to convert")
    parser.add_argument("-o", "--output", type=str, default="output.svg", help="Output filename")
    
    args = parser.parse_args()
    
    print(f"Input Text: {args.text}")
    
    # Convert English text to IPA phonemes (skipping Caesar shift)
    ipa_text = p.convert(args.text)
    print(f"IPA Phonemes: {ipa_text}")

    paths = parse_ipa_text(ipa_text)
    
    if paths:
        merge_svgs(paths, args.output)
    else:
        print("No valid glyphs found to render.")

if __name__ == "__main__":
    main()