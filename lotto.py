import random
import time

all_numbers = []

print('Welcome to the Lotto Number Generator!')
print('Here are your lucky numbers:\n')

for i in range(1, 7):
    number = random.randint(1, 49)

    while number in all_numbers:
        number = random.randint(1, 49)

    all_numbers.append(number)
    print(number)
    time.sleep(1)

print('\nYour lucky numbers are: ', end='')
all_numbers.sort()

for number in all_numbers:
    print(number, end=' ')

print('\nGood luck!')
