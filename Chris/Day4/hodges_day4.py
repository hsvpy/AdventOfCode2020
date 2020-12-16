from typing import Optional, List, Tuple, Dict
import re

class Passport:
    def __init__(self, passport_dict: Dict[str, str]):
        try:
            self.byr = passport_dict['byr']
            self.iyr = passport_dict['iyr']
            self.eyr = passport_dict['eyr']
            self.hgt = passport_dict['hgt']
            self.hcl = passport_dict['hcl']
            self.ecl = passport_dict['ecl']
            self.pid = passport_dict['pid']
        except KeyError as err:
            raise AttributeError(f"Missing in passport: {err}")

        if 'cid' in passport_dict.keys():
            self.cid = passport_dict['cid']

    def is_valid_years(self) -> bool:
        def four_digits(year: str) -> bool:
            return re.search(r'^\d{4}$', year) != None
        date_validation = [
            {'year': self.byr, 'start': 1920, 'end': 2002},
            {'year': self.iyr, 'start': 2010, 'end': 2020},
            {'year': self.eyr, 'start': 2020, 'end': 2030}
        ]
        for date_field in date_validation:            
            if not four_digits(date_field['year']):
                return False 
            year = int(date_field['year'])
            if year < date_field['start'] or year > date_field['end']:
                return False
        return True
    
    def is_valid_height(self) -> bool:
        height = self.hgt
        try:
            if match := re.search(r'(\d*)cm$', height):
                return (150 <= int(match.group(1)) <= 193)
            elif match := re.search(r'(\d*)in$', height):
                return (59 <= int(match.group(1)) <= 76)
            else:
                return False
        except ValueError:
            return False

    def is_valid_hair(self) -> bool:
        return re.search('#[0-9a-f]{6}', self.hcl) is not None
    
    def is_valid_eye(self) -> bool:
        colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        return colors.count(self.ecl) > 0

    def is_valid_pid(self) -> bool:
        return re.search(r'^\d{9}$', self.pid) is not None

    def is_valid(self) -> bool:
       validators = [self.is_valid_years, 
                     self.is_valid_height, 
                     self.is_valid_hair, 
                     self.is_valid_eye, 
                     self.is_valid_pid]
       return all(list(map(lambda x: x(), validators)))

def combine_passport_lines(raw_lines: List[str]) -> List[str]:
    #todo : there is surely an easier way to do this
    passport_lines = []
    for idx, line in enumerate(raw_lines):
        if line != '\n' and idx != 0:
            raw_lines[idx] += (' ' + raw_lines[idx-1])
            if idx == len(raw_lines) - 1:
                passport_lines.append(raw_lines[idx])

        elif line == '\n':
            passport_lines.append(raw_lines[idx-1])
        
    passport_lines = list(map(lambda x: x.replace('\n', ' '), passport_lines))
    return passport_lines 



def parse_input(filename: str) -> (List[Passport], int):
    with open(filename, 'r') as fh:
        raw_lines = fh.readlines()
    passport_lines = combine_passport_lines(raw_lines)
    print(str(passport_lines))

    raw_passports = [dict(re.findall('(\w\w\w):(\S+)\s', passport_data)) for passport_data in passport_lines]
    invalid_passports = 0
    passports = []
    for passport_dict in raw_passports:
        try:
           passports.append(Passport(passport_dict))
        except AttributeError as err:
            print(str(passport_dict))
            print(err)
            invalid_passports += 1

    print(f'Raw number of potential passports: {str(len(passport_lines))}')
    return passports, invalid_passports

def determine_valid_passport(passport: Passport) -> bool:
    valid = True
    return valid


passports_required_fields, invalid = parse_input('input.txt')
print(f'Part 1: {str(len(passports_required_fields))}')
passports = list(map(lambda p: p.is_valid(), passports_required_fields))
print(f'Part 2: {str(len(list(filter(None, passports))))}')