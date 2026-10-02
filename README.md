# Music Engine

**Procedural music composition in Python: musical rules, weighted randomness and complete instrumental arrangements.**

A personal project by **Orcun Duzbeyaz**, an MSci Mathematical Physics student at the University of Nottingham. The engine generates harmony, melody, bass and percussion, then exports the arrangement as MIDI and optionally WAV.

This repository is the public portfolio showcase. The full composition engine is maintained privately; the code here is a separate demonstration utility for inspecting the supplied MIDI example. It does not generate new music.

## Listen to the results

| Track | Audio |
| --- | --- |
| Prototype output 1 | [Listen / download MP3](examples/prototype-output-1.mp3) |
| Prototype song 1 | [Listen / download MP3](examples/prototype-song-1.mp3) |
| Prototype song 10 | [Listen / download MP3](examples/prototype-song-10.mp3) |

GitHub may offer a download instead of an audio player. A separate [MIDI example](examples/prototype-song-0.mid) can be opened in a DAW or MIDI player. These outputs come from the original prototype; their settings and seeds were not recorded, and the MIDI is not claimed to match any of the MP3s.

## What I built

- **Harmony and song structure:** key and mode selection, chord progressions and recurring song sections.
- **Voice leading:** chord inversions selected using pitch movement between successive chords.
- **Melody:** weighted chord-tone selection, rhythmic patterns and repetition penalties.
- **Bass and percussion:** recurring bass motifs, approach notes and rhythmic templates.
- **Export:** separate MIDI parts and optional audio rendering through FluidSynth and an external SoundFont.

The engine is rule based. It does not train a machine-learning model or use a dataset of songs. Random choices provide variation, while musical constraints guide how the parts fit together.

## Technical approach

| Component | Design |
| --- | --- |
| Composition | Python rules and weighted random sampling |
| Harmony | Six modes, progression patterns, chord extensions and inversions |
| Musical timing | Note durations fitted to the arrangement's beat budget |
| Instrumentation | General MIDI program mapping |
| MIDI export | MIDIUtil |
| Optional WAV rendering | FluidSynth with a separately supplied SoundFont |
| Repeatability | Seeded batch generation in the private export implementation |

Read the [architecture and engineering notes](docs/architecture.md) for the design, validation approach and current limitations.

## Run the public demo

Download or clone this repository and use Python 3.10 or newer. The public demo uses only the Python standard library.

```bash
python demo.py
```

It reports the MIDI format, track count, timing resolution and file size for the bundled example, then lists the listening files. To inspect a different MIDI file:

```bash
python demo.py --midi path/to/example.mid
```

Run the public utility tests:

```bash
python -m unittest discover -s tests -v
```

These tests check the demonstration utility. The private engine has separate tests for part durations, pitch ranges, reproducibility and output protection. Neither suite measures subjective musical quality.

## Repository contents

| Path | Purpose |
| --- | --- |
| `examples/` | Three recordings and one separate MIDI output |
| `docs/architecture.md` | Design and engineering notes |
| `demo.py` | Command-line inspection of an existing MIDI file |
| `src/midi_summary.py` | Independent MIDI container validation utility |
| `tests/` | Tests for the public utility |

## Project status

The prototype produces complete arrangements, but musical quality varies. Next steps include sharing one section timeline across all parts, reviewing bass timing and separating composition and export into independent modules. The current private implementation is intended for sequential generation.

## Credits and access

The full engine uses [MIDIUtil](https://github.com/MarkCWirt/MIDIUtil) for MIDI export and optionally [FluidSynth](https://www.fluidsynth.org/) for rendering. SoundFonts are external assets and are not included here.

Copyright © 2026 Orcun Duzbeyaz. No open-source licence is included in this showcase. The full generator source is not distributed here.
