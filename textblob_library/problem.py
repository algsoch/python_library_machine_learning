"""Small demo/CLI wrapper that uses the `spell` module for corrections.

This file preserves the original examples but delegates the core correction
to `spell.correct_text` (which prefers TextBlob when available and falls back
to a mapping/difflib-based approach if TextBlob is not installed).

Run from the command line:
    python problem.py          # runs a few sample corrections
    python problem.py --file typo.txt --out corrected_typos.txt

"""
import argparse
from spell import correct_text, get_backend_info


SAMPLE_SEARCHES = [
    "metal plate cover gcfi",
    "artric air portable",
    "roll roofing lap cemet",
    "basemetnt window",
    "vynal grip strip",
    "lawn mower- electic",
]


def demo_print():
    """Print demo corrections for sample searches."""
    backend = get_backend_info()
    print(f"--- Spell Correction Demo (using {backend['backend']}) ---")
    for s in SAMPLE_SEARCHES:
        corrected = correct_text(s)
        print(f'"{s}" -> "{corrected}"')


def perform_spell_check_on_file(input_file, output_file):
    """Correct spelling for all lines in a file."""
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            corrected_line = correct_text(line.strip())
            outfile.write(corrected_line + '\n')


def main():
    parser = argparse.ArgumentParser(description='Spell correction demo')
    parser.add_argument('--file', '-f', help='Input file to correct (one query per line)')
    parser.add_argument('--out', '-o', default='corrected_typos.txt', help='Output file')
    args = parser.parse_args()

    if args.file:
        perform_spell_check_on_file(args.file, args.out)
        print(f'Corrected file written to {args.out}')
    else:
        demo_print()


if __name__ == '__main__':
    main()