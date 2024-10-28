import random
import time

MIN_NUMBER = 1
MAX_NUMBER = 49


def get_number():
    number = random.randint(MIN_NUMBER, MAX_NUMBER)

    while number in all_numbers:
        number = random.randint(MIN_NUMBER, MAX_NUMBER)

    return number


all_numbers = []

print('Welcome to the Lotto Number Generator!')
print('Here are your lucky numbers:\n')

for i in range(1, 7):
    number = get_number()
    all_numbers.append(number)
    print(number)
    time.sleep(random.uniform(0.5, 1.5))

print('\nYour lucky numbers are: ', end='')
all_numbers.sort()

for number in all_numbers:
    print(number, end=' ')

print('\nGood luck!')
