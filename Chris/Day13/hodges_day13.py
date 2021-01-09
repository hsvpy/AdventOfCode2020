from typing import Tuple, List
from sympy.ntheory.modular import crt

def parse_input(filename: str) -> Tuple[int, List[int]]:
    with open(filename, 'r') as f:
        departure_time = int(f.readline())
        bus_ids = list(map(lambda x: int(x) if x != 'x' else 'x', f.readline().split(',')))
    return (departure_time, bus_ids)


time, ids = parse_input('input.txt')

mods = [(id, time % id, id - time % id) for id in ids if id != 'x']
sorted_list = sorted(mods, key=lambda x: x[2])
q = sorted_list[0]
print(f"Part 1: {str(q[2]*q[0])}")

moduli = []
residues = []
for position, id in enumerate(ids):
    if id != 'x':
        moduli.append(id)
        residues.append(-position)

print(f"Part 2: {min(crt(moduli, residues))}")
