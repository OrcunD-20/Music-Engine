# Architecture and engineering notes

## Design goal

Generate a complete instrumental arrangement from musical rules and random choices. Harmony, melody, bass and percussion should remain coherent while outputs vary between runs.

This document describes the private engine at a high level. The public MIDI inspection utility is independent of the composition implementation.

## Composition stages

| Stage | Responsibility | Output |
| --- | --- | --- |
| Harmony and structure | Choose a key, mode, progression patterns and song sections | Chord progression and harmonic context |
| Voice leading | Compare candidate inversions by pitch movement | Chord voicings |
| Melody | Sample chord tones with movement and repetition weights; assign rhythms | Pitch, velocity and duration events |
| Accompaniment dynamics | Derive accompaniment levels from the melody | Chord velocities |
| Bass | Combine motifs, chord tones and approach notes | Bass note events |
| Percussion | Choose a rhythmic template and place drum events | Percussion events |
| Export | Map instruments and write separate MIDI parts | MIDI file and generation metadata |
| Optional rendering | Render MIDI using FluidSynth and a user-supplied SoundFont | WAV audio |

## Engineering choices

- **Rules plus randomness:** use musical constraints to guide sampling without requiring training data.
- **MIDI as an intermediate format:** separate composition from sound rendering so outputs can be inspected or edited in a DAW.
- **Seeded generation:** make the MIDI sequence repeatable for the same batch settings and code/dependency versions. The supplied prototype recordings predate this workflow and have no recorded seeds.
- **Command-line configuration:** use explicit tempo, seed, batch size and output paths instead of machine-specific settings.
- **Output protection:** prevent an accidental overwrite unless the user explicitly enables it.

## Validation in the private implementation

The private test suite checks generated parts across 100 seeds, including duration agreement, MIDI pitch ranges and positive note durations. It also checks repeated seeded exports, distinct tracks within a batch, invalid command-line inputs and protection of existing outputs.

These checks exercise mechanical invariants. They do not establish musical quality or verify all possible seeds. WAV rendering requires a separate FluidSynth and SoundFont setup.

## Current limitations

- Quality is subjective and varies; there has been no formal listening study.
- Bass sections currently use a proportional layout while harmony and melody use explicit song sections. Sharing one timeline would improve consistency.
- Melody predominantly selects chord tones; scale fallbacks and bass timing heuristics need further review.
- Module-level state makes sequential generation the current intended use.
- User controls cover tempo, seed, batch size and output location. Key, mode and instrument choices are automatic.

## Public demonstration scope

`src/midi_summary.py` validates MIDI header and track-chunk boundaries, reports the format and timing division, and checks the declared track count. It does not parse note events, calculate musical duration, assess musical quality or reconstruct the composition algorithm.
