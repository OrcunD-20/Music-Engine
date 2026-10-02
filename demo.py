"""Inspect an existing MIDI example; the composition engine is private."""

import argparse
import json
from pathlib import Path

from src.midi_summary import inspect_midi

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a MIDI container and list the Music Engine recordings.")
    parser.add_argument("--midi", type=Path,
                        default=ROOT / "examples" / "prototype-song-0.mid")
    args = parser.parse_args()
    try:
        summary = inspect_midi(args.midi)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot inspect MIDI: {error}\n")
    print("Music Engine — public output demo")
    print(f"MIDI: {args.midi.name}")
    print(json.dumps(summary, indent=2))
    print("\nListening examples (open with your audio player):")
    for audio in sorted((ROOT / "examples").glob("*.mp3")):
        print(f"  {audio}")
    print("\nThe full composition engine is maintained privately.")


if __name__ == "__main__":
    main()
