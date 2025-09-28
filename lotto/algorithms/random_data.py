import random


MIN_NUMBER = 1
MAX_NUMBER = 49

_selected_numbers = []


def generate_numbers():
    numbers = [_get_number() for _ in range(6)]
    _selected_numbers.clear()
    return numbers


def _get_number():
    number = random.randint(MIN_NUMBER, MAX_NUMBER)

    while number in _selected_numbers:
        number = random.randint(MIN_NUMBER, MAX_NUMBER)

    return number
