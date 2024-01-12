#!/usr/bin/env python3
# Converts lmmz-style seat configuration to akx-style CSV

import csv
import re
import sys

SECTION_HEADER_RE = re.compile(r"^;;\s*([\w\s]+) \((\d+)")
PLACES_RE = re.compile(r"^([AB]\d+): (\d+)-(\d+)")


def lmmz2paikkala(input_stream=sys.stdin, output_stream=sys.stdout):
    output_csv = csv.writer(output_stream, dialect="excel")
    output_csv.writerow(("zone", "row", "start", "end"))

    zone = None
    for line in input_stream.readlines():
        match = SECTION_HEADER_RE.match(line)
        if match:
            zone_name = match.group(1).capitalize().replace(" a ", " A ").replace(" b ", " B ")
            floor_num = match.group(2)
            zone = f"{zone_name} ({floor_num}. krs)"
            print("Zone:", repr(zone), file=sys.stderr)
            continue

        match = PLACES_RE.match(line)
        if match:
            row = match.group(1)
            start = int(match.group(2))
            end = int(match.group(3))
            print(f"Places: row {row}, from {start} to {end}", file=sys.stderr)
            output_csv.writerow((zone, row, start, end))
            continue

        print("Line ignored:", repr(line), file=sys.stderr)


if __name__ == "__main__":
    lmmz2paikkala()
