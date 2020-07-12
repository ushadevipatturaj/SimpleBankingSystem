import random


# Write your code here
def apply_luhn_algorithm(cardno):
    _sum = 0
    for i, value in enumerate(cardno, start=1):
        if i % 2 == 1:
            value = int(value) * 2 - 9 if int(value) * 2 > 9 else int(value) * 2
        _sum += int(value)
    return _sum % 10


def create_account():
    cardno = str(400000) + str(random.randint(000000000, 999999999))
    checksum = apply_luhn_algorithm(cardno)
    if checksum == 0:
        cardno = cardno + '0'
    else:
        cardno = cardno + str(10 - checksum)
    pinno = random.randint(0000, 1111)
    return cardno, str(pinno).ljust(4, '0')


def login(card, pinno):
    global card_pin_details, balance
    if card in card_pin_details:
        if card_pin_details[card] == pinno:
            print('You have successfully logged in!\n')

            while True:
                print('1. Balance\n2. Log out\n0. Exit')
                choice = input()
                if choice == '1':
                    print('Balance: {}'.format(balance))
                elif choice == '2':
                    print('You have successfully logged out!\n')
                    return 0
                elif choice == '0':
                    print('Bye!')
                    exit(0)
        else:
            print('Wrong card number or PIN!\n')
    else:
        print('Wrong card number or PIN!\n')


run = True
card_pin_details = {}
while run:
    print('\n1. Create an account\n2. Log into account\n0. Exit')
    user_choice = input()
    if int(user_choice) == 1:
        card_no, pin = create_account()
        print('\nYour card has been created')
        print("Your card number:\n" + card_no)
        print("Your card PIN:\n" + pin)
        card_pin_details[card_no] = pin
        balance = 0

    elif int(user_choice) == 2:
        print('Enter your card number:')
        card_no = input()
        print('Enter your PIN')
        pin = input()
        login(card_no, pin)
    else:
        print('\nBye!')
        run = False
        exit(0)


