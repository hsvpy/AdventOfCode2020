DOOR_KEY = 9093927
CARD_KEY = 11001876


def establish_secret_key(door_key: int, card_key: int) -> int:

    exponent = 0
    value = 1
    while value != card_key:
        exponent += 1
        value = 7 * value % 20201227
    return pow(door_key, exponent, 20201227)


if __name__ == "__main__":
    print(establish_secret_key(DOOR_KEY, CARD_KEY))
