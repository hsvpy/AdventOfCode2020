import re
from typing import List

class record:
    def __init__(self, lowerRange: int, higherRange: int, letter: str, password: str):
        self.lowerRange = int(lowerRange)
        self.higherRange = int(higherRange)
        self.letter = letter
        self.password = password
    
    def __repr__(self):
        return f"{self.lowerRange}-{self.higherRange} {self.letter}: {self.password}"


def parse_input(filename: str) -> List[record]:
    with open(filename, 'r') as fh:
        raw_entries = fh.readlines()
    entries = list(map(lambda x: x.rstrip(), raw_entries))
    records = []
    for entry in entries:
        match = re.search("^(\d+)-(\d+) (\D): (.+)$", entry)
        if match:
            records.append(record(match.group(1), match.group(2), match.group(3), match.group(4)))
        else:
            print(f"Error parsing record: {entry}")

    return records

def validate_record(rec: record) -> bool:
    count = rec.password.count(rec.letter)
    return rec.lowerRange <= count and count <= rec.higherRange

def validate_record_part_2(rec: record) -> bool:
    return (rec.letter in rec.password[rec.lowerRange-1]) != (rec.letter in rec.password[rec.higherRange-1])

records = parse_input('input.txt')
print(f"Part 1: {str(list(map(validate_record, records)).count(True))}")
print(f"Part 2: {str(list(map(validate_record_part_2, records)).count(True))}")


