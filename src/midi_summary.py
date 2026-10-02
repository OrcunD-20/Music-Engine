"""Inspect a Standard MIDI File container without external dependencies.

This is a showcase utility, not part of the private composition engine.
It validates container structure, not the individual MIDI events.
"""

from pathlib import Path
import struct


def inspect_midi(path: Path) -> dict:
    data = Path(path).read_bytes()
    if len(data) < 14 or data[:4] != b"MThd":
        raise ValueError("Expected a MIDI header (MThd).")
    header_size = struct.unpack_from(">I", data, 4)[0]
    if header_size < 6 or 8 + header_size > len(data):
        raise ValueError("Invalid or truncated MIDI header.")
    file_format, tracks, division = struct.unpack_from(">HHH", data, 8)
    if file_format not in (0, 1, 2) or tracks == 0:
        raise ValueError("Invalid MIDI format or track count.")
    if file_format == 0 and tracks != 1:
        raise ValueError("Format 0 requires exactly one track.")
    if division & 0x8000:
        frames = -struct.unpack("b", bytes([division >> 8]))[0]
        ticks_per_frame = division & 0xFF
        if frames not in (24, 25, 29, 30) or ticks_per_frame == 0:
            raise ValueError("Invalid SMPTE timing division.")
        timing = {"type": "SMPTE", "frame_code": frames,
                  "ticks_per_frame": ticks_per_frame}
    else:
        if division == 0:
            raise ValueError("Ticks per quarter note must be positive.")
        timing = {"type": "PPQ", "ticks_per_quarter_note": division}

    cursor = 8 + header_size
    found_tracks = 0
    while cursor < len(data):
        if len(data) - cursor < 8:
            raise ValueError("Truncated MIDI chunk header.")
        tag, size = struct.unpack_from(">4sI", data, cursor)
        cursor += 8
        if size > len(data) - cursor:
            raise ValueError("Truncated MIDI chunk payload.")
        if tag == b"MTrk":
            found_tracks += 1
        cursor += size
    if found_tracks != tracks:
        raise ValueError("Declared MIDI track count does not match the file.")
    return {"format": file_format, "tracks": tracks,
            "timing": timing, "size_bytes": len(data)}
