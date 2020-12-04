from typing import List


REQUIRED_FIELDS = {
    "byr",  # (Birth Year)
    "iyr",  # (Issue Year)
    "eyr",  # (Expiration Year)
    "hgt",  # (Height)
    "hcl",  # (Hair Color)
    "ecl",  # (Eye Color)
    "pid",  # (Passport ID)
}
OPTIONAL_FIELDS = {
    "cid",  # (Country ID)
}

TEST_INPUT = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""".splitlines()


PART_TWO_VALID_TEST_INPUTS = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""".splitlines()

PART_TWO_INVALID_TEST_INPUTS = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""".splitlines()


with open("day04.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def part_one(puzzle_input: List[str]) -> int:
    active_puzzle = {}
    count = 0
    for line in puzzle_input:
        if not line.strip():
            # we found a break
            count += set(active_puzzle).issuperset(REQUIRED_FIELDS)
            active_puzzle = {}
            continue
        tokens = line.split()
        pairs = dict(i.split(":") for i in tokens)
        active_puzzle.update(pairs)
    if active_puzzle:
        # parse the last one:
        count += set(active_puzzle) == REQUIRED_FIELDS
    return count


def part_two(puzzle_input: List[str]) -> int:
    active_puzzle = {}
    count = 0
    for line in puzzle_input:
        if not line.strip():
            # we found a break
            all_fields_present = set(active_puzzle).issuperset(REQUIRED_FIELDS)
            all_fields_valid = all(
                validate_field(key, val) is not False
                for key, val in active_puzzle.items()
            )
            count += all_fields_present and all_fields_valid
            active_puzzle = {}
            continue
        tokens = line.split()
        pairs = dict(i.split(":") for i in tokens if ":" in i)
        active_puzzle.update(pairs)
    if active_puzzle:
        # parse the last one:
        all_fields_present = set(active_puzzle).issuperset(REQUIRED_FIELDS)
        all_fields_valid = all(
            validate_field(key, val) is not False for key, val in active_puzzle.items()
        )
        count += all_fields_present and all_fields_valid

    return count


def validate_field(key: str, value: str) -> bool:
    field_funcs = {
        "byr": validate_byr,
        "iyr": validate_iyr,
        "eyr": validate_eyr,
        "hgt": validate_height,
        "hcl": validate_hcl,
        "ecl": validate_ecl,
        "pid": validate_pid,
        "cid": lambda x: True,
    }
    try:
        result = field_funcs[key](value)
        return result
    except KeyError:
        print(f"unknown field {key}")
        return None


def validate_byr(value: str) -> bool:
    """Birth year must be 1920-2002"""
    try:
        return int(value) in range(1920, 2003)
    except (TypeError, ValueError):
        return False


def validate_iyr(value: str) -> bool:
    """issue year must be an int between 2010 and 2020, inclusive"""
    try:
        return int(value) in range(2010, 2021)
    except (TypeError, ValueError):
        return False


def validate_eyr(value: str) -> bool:
    """Expiration must be between 2020 and 2030, inclusive"""
    try:
        return int(value) in range(2020, 2031)
    except (TypeError, ValueError):
        return False


def validate_height(value: str) -> bool:
    """value must be xxxcm or xxin:
    if cm, must be 150-193, else 59-76"""
    try:
        if value.endswith("cm"):
            return int(value[:-2]) in range(150, 194)
        elif value.endswith("in"):
            return int(value[:-2]) in range(59, 77)
        return False
    except (TypeError, ValueError):
        return False


def validate_hcl(value: str) -> bool:
    """Value must be an HTML color string"""
    if not value.startswith("#") or len(value) != 7:
        return False
    try:
        # remainder must be a valid hex string
        int(value[1:], 16)
    except ValueError:
        return False
    else:
        return True


def validate_ecl(value: str) -> bool:
    return value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def validate_pid(value: str) -> bool:
    return len(value) == 9 and value.isdigit()


assert part_one(TEST_INPUT) == 2
print(part_one(REAL_INPUT))
assert part_two(PART_TWO_INVALID_TEST_INPUTS) == 0
assert part_two(PART_TWO_VALID_TEST_INPUTS) == 4
print(part_two(REAL_INPUT))
