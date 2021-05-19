"""
This script is used to generate nice looking Markdown tables.

Usage: python md2table.py <path to input file> [<caption1> <caption2>...]
"""
import argparse
from typing import Pattern, Match, Optional, List, Any, Dict, NewType
import re


ColumnIndex = NewType('ColumnIndex', int)
ColumnWidth = NewType('ColumnWidth', int)


def get_max(array: List[List[Any]]) -> int:
    maximum: int = 0
    for element in array:
        if len(element) > maximum:
            maximum = len(element)
    return maximum


parser = argparse.ArgumentParser(description='MD table builder')
parser.add_argument('input',
                    action='store',
                    nargs=1,
                    type=str,
                    help='path to the input file')
parser.add_argument('captions',
                    action='store',
                    nargs='*',
                    type=str,
                    help='captions (a list of space separated labels)')
parser.add_argument('--verbose',
                    dest='verbose',
                    action='store_true',
                    help='verbosity flag')
parser.add_argument('--sep',
                    dest='sep',
                    action='store',
                    default='|',
                    help='field separator')


args = parser.parse_args()
path_input: str = args.input[0]
captions: List[str] = args.captions
verbose: bool = args.verbose
sep: str = args.sep

p = '^\\s*\\{}'.format(sep)
pattern: Pattern = re.compile(p)

# Read the input file.
table_lines: List[List[str]] = [captions]
with open(path_input, 'r') as fd:
    while True:
        line: str = fd.readline()
        if not line:
            break
        line = line.strip()
        m: Optional[Match] = pattern.search(line)
        if m is None:
            continue
        fields: List[str] = line.split(sep)
        fields.pop(0)
        fields = [s.strip() for s in fields]
        table_lines.append(fields)

# Add empty fields to lines, if necessary. At the end, all lines have the same number of fields.
columns_count: int = get_max(table_lines)
delta = columns_count-len(captions)
captions.extend(['' for _ in range(0 if delta < 0 else delta)])
columns_count = columns_count if delta > 0 else len(captions)

# Calculate the widths of all columns.
max_per_columns: Dict[ColumnIndex, ColumnWidth] = {i: 0 for i in range(columns_count)}
line: List[str]
for line in table_lines:
    column_index: ColumnIndex
    for column_index in range(columns_count):
        if column_index >= len(line):
            continue
        cell = line[column_index]
        if max_per_columns[column_index] < len(cell):
            max_per_columns[column_index] = ColumnWidth(len(cell))

if verbose:
    print("Columns lengths:")
    for c in range(columns_count):
        print(" - {:3d}: {}".format(c, max_per_columns[c]))

# Add spaces to lines' fields so that, within a given column, all fields have exactly the same width.
table: List[List[str]] = []
for line in table_lines:
    new_line: List[str] = []
    column_index: ColumnIndex
    for column_index in range(columns_count):
        cell = line[column_index] if len(line) > column_index else ''
        new_line.append(cell + ' '*(max_per_columns[column_index] - len(cell)))
    table.append(new_line)

# Add the caption on top of the table body.
caption = "| " + " | ".join(table.pop(0)) + " | "
lines: List[str] = ["| " + (" | ".join(line) + " | ").strip() for line in table]
lines.insert(0, caption)
lines.insert(1, "|" + "|".join(["-" * (max_per_columns[c] + 2) for c in range(columns_count)]) + "|")
print("\n".join(lines))
