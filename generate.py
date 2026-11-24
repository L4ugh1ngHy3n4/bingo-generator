#!/usr/bin/env python3
"""Generate large-print bingo PDFs with fresh OS-backed randomness."""
import argparse
import json
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import os
import sys

RANGES = ((1, 15), (16, 30), (31, 45), (46, 60), (61, 75))

def make_cards(count):
    rng = random.SystemRandom()
    seen = set()
    cards = []
    while len(cards) < count:
        columns = [rng.sample(range(lo, hi + 1), 5) for lo, hi in RANGES]
        rows = tuple(zip(*columns))
        if rows not in seen:
            seen.add(rows)
            cards.append(rows)
    return cards

def generate_pdf(count, output):
    if count < 1:
        raise ValueError('Die Anzahl muss mindestens 1 sein.')
    bundled = Path(__file__).with_name('typst.exe' if os.name == 'nt' else 'typst')
    compiler = str(bundled) if bundled.is_file() else (None if getattr(sys, 'frozen', False) else shutil.which('typst'))
    if not compiler:
        raise RuntimeError('Typst wurde nicht gefunden. Bitte Typst installieren und zum PATH hinzufügen.')
    output = Path(output).expanduser().resolve()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        shutil.copyfile(Path(__file__).with_name('bingo.typ'), root / 'bingo.typ')
        (root / 'cards.json').write_text(json.dumps(make_cards(count)), encoding='utf-8')
        result = subprocess.run([compiler, 'compile', str(root / 'bingo.typ'), str(output)], creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or 'Typst compilation failed.')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('count', type=int, nargs='?', default=10)
    parser.add_argument('-o', '--output', type=Path, default=Path('bingo.pdf'))
    args = parser.parse_args()
    try:
        output = generate_pdf(args.count, args.output)
    except (ValueError, RuntimeError, OSError) as exc:
        parser.exit(1, f'{exc}\n')
    print(f'Created {args.count} cards: {output}')

if __name__ == '__main__':
    main()
