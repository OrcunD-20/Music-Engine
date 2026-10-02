"""Test the public container inspector with valid and malformed MIDI files."""

from pathlib import Path
import struct
import tempfile
import unittest

from src.midi_summary import inspect_midi

ROOT = Path(__file__).resolve().parents[1]


def midi_bytes(file_format=0, tracks=1, division=480):
    header = b"MThd" + struct.pack(">IHHH", 6, file_format, tracks, division)
    # Delta time 0 followed by an end-of-track meta event.
    track = b"MTrk" + struct.pack(">I", 4) + b"\x00\xff\x2f\x00"
    return header + track


class MidiSummaryTests(unittest.TestCase):
    def inspect_bytes(self, data):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.mid"
            path.write_bytes(data)
            return inspect_midi(path)

    def test_bundled_prototype(self):
        summary = inspect_midi(ROOT / "examples" / "prototype-song-0.mid")
        self.assertEqual(summary["format"], 1)
        self.assertEqual(summary["tracks"], 5)
        self.assertEqual(summary["timing"],
                         {"type": "PPQ", "ticks_per_quarter_note": 960})

    def test_valid_single_track(self):
        summary = self.inspect_bytes(midi_bytes())
        self.assertEqual(summary["tracks"], 1)
        self.assertEqual(summary["size_bytes"], 26)

    def test_smpte_timing(self):
        summary = self.inspect_bytes(midi_bytes(division=(0xE7 << 8) | 40))
        self.assertEqual(summary["timing"],
                         {"type": "SMPTE", "frame_code": 25,
                          "ticks_per_frame": 40})

    def test_rejects_truncated_and_invalid_containers(self):
        cases = [b"not MIDI", midi_bytes()[:-1], midi_bytes() + b"MTrk",
                 midi_bytes(file_format=3), midi_bytes(division=0),
                 midi_bytes(division=0xE600), midi_bytes(tracks=2),
                 midi_bytes(file_format=1, tracks=2)]
        for data in cases:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.inspect_bytes(data)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                inspect_midi(Path(folder) / "missing.mid")


if __name__ == "__main__":
    unittest.main()
