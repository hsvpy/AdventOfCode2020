from typing import Counter, Dict, List, Set

TEST_INPUT = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitlines()


with open("day21.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def parse_input(puzzle: List[str]) -> List[List[List[str]]]:
    result = []
    for line in puzzle:
        ingredient_str, allergen_str = line.split(" (contains ")
        allergens = allergen_str[:-1].split(", ")
        ingredients = ingredient_str.split()
        result.append([ingredients, allergens])
    return result


def part_one(puzzle_input: List[str]) -> int:
    parsed = parse_input(puzzle_input)
    overall_ingredients = sum((i[0] for i in parsed), [])
    ingredient_count = Counter(overall_ingredients)
    ingredient_allergen_map: Dict[str, Set] = {}
    for ingredients, allergens in parsed:
        for allergen in allergens:
            try:
                ingredient_allergen_map[allergen] &= set(ingredients)
            except KeyError:
                ingredient_allergen_map[allergen] = set(ingredients)
    possible_ingredients = set()
    for ingredients in ingredient_allergen_map.values():
        possible_ingredients |= ingredients
    return sum(
        count
        for ingredient, count in ingredient_count.items()
        if ingredient not in possible_ingredients
    )


def part_two(puzzle_input: List[str]) -> str:
    parsed = parse_input(puzzle_input)
    ingredient_allergen_map: Dict[str, Set] = {}
    for ingredients, allergens in parsed:
        for allergen in allergens:
            try:
                ingredient_allergen_map[allergen] &= set(ingredients)
            except KeyError:
                ingredient_allergen_map[allergen] = set(ingredients)
    definite_ingredients = {}
    while ingredient_allergen_map:
        for allergen, ingredients in list(ingredient_allergen_map.items()):
            if len(ingredients) == 1:
                ingredient = ingredients.pop()
                definite_ingredients[ingredient] = allergen
                del ingredient_allergen_map[allergen]
        for ingredients in ingredient_allergen_map.values():
            for ingredient in definite_ingredients:
                try:
                    ingredients.remove(ingredient)
                except KeyError:
                    pass
    return ",".join(
        i[0] for i in sorted(definite_ingredients.items(), key=lambda k: k[1])
    )


assert part_one(TEST_INPUT) == 5
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == "mxmxvkd,sqjhc,fvjkl", part_two(TEST_INPUT)
print(part_two(REAL_INPUT))
