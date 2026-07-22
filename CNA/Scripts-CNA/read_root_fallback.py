import os
import re
import struct
from pathlib import Path


def read_root_file(path):
    """Best-effort extractor for simple ROOT files.

    This is a fallback for environments where ROOT or PyROOT is not available.
    It scans the file for numeric values that look like efficiency points and
    returns a list of (energy, efficiency) pairs when possible.
    """
    data = Path(path).read_bytes()
    text = data.decode('latin-1', errors='ignore')

    # Try to find simple numeric patterns from common ROOT output formats.
    numbers = re.findall(r'([0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)', text)
    values = []
    for idx, num in enumerate(numbers):
        try:
            val = float(num)
        except ValueError:
            continue
        if abs(val) < 1e-12:
            continue
        values.append(val)

    # Heuristic: pair the values as (energy, efficiency) when there are at least 2.
    if len(values) >= 2:
        pairs = []
        for i in range(0, len(values) - 1, 2):
            energy = values[i]
            efficiency = values[i + 1]
            if efficiency > 0 and efficiency <= 10:
                pairs.append((energy, efficiency))
        if pairs:
            return pairs

    return []


if __name__ == '__main__':
    for path in [
        'data/AbsoluteEfficiency_HPGe_8mm_1e6.root',
        'data/AbsoluteEfficiency_HPGe_50mm_1e6.root',
        'data/AbsoluteEfficiency_HPGe_100mm_1e6.root',
    ]:
        print(path, read_root_file(path))
