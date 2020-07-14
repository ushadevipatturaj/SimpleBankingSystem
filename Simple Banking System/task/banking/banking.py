import random
import sqlite3


# Write your code here
def apply_luhn_algorithm(cardno):
    _sum = 0
    for i, value in enumerate(cardno, start=1):
        if i % 2 == 1:
            value = int(value) * 2 - 9 if int(value) * 2 > 9 else int(value) * 2
        _sum += int(value)
    return _sum % 10


def check_luhn_algorithm(cardno):
    _sum = 0
    for i, value in enumerate(cardno[:-1], start=1):
        if i % 2 == 1:
            value = int(value) * 2 - 9 if int(value) * 2 > 9 else int(value) * 2
        _sum += int(value)
    _sum +=int(cardno[-1])
    return _sum % 10 == 0


def create_account():
    _id = random.randint(1, 999)
    cardno = str(400000) + str(random.randint(000000000, 999999999)).ljust(9,'0')
    checksum = apply_luhn_algorithm(cardno)
    if checksum == 0:
        cardno = cardno + '0'
    else:
        cardno = cardno + str(10 - checksum)
    pinno = str(random.randint(0000, 1111)).ljust(4, '0')
    _balance = 0
    insert_query = "insert into card (id, number, pin, balance) values ({0},{1},{2},{3});".format(_id, cardno, pinno,
                                                                                                  _balance)
    cur.execute(insert_query)
    conn.commit()
    return cardno, pinno


def print_balance(card):
    cur.execute("select balance from card where number =" + card + " ;")
    _balance = cur.fetchone()
    if _balance is not None:
        print('\nBalance:{}\n'.format(_balance[0]))


def add_income(card, income):
    update_query = str("update card set balance=balance+{0} where number =" + card + " ;").format(income)
    cur.execute(update_query)
    conn.commit()
    print("Income was added!\n")


def check_card_availablity(card):
    cur.execute("select number from card where number =" + card + ";")
    row = cur.fetchone()
    if row is not None:
        if row[0] == card:
            return True
        else:
            print('Such a card does not exist.\n')
            return False
    else:
        print('Such a card does not exist.\n')
        return False


def check_balance(_transfer_amount, card):
    cur.execute("select balance from card where number =" + card + ";")
    row = cur.fetchone()
    if row is not None:
        if row[0] >= _transfer_amount:
            return True
        else:
            print('Not enough money!\n')
            return False


def do_transfer(card, amount, to_tranfer_card):
    update_query_from = str("update card set balance=balance-{0} where number =" + card + " ;").format(amount)
    update_query_to = str("update card set balance=balance+{0} where number =" + to_tranfer_card + " ;").format(amount)
    cur.execute(update_query_from)
    conn.commit()
    cur.execute(update_query_to)
    conn.commit()
    print("Success!\n")


def transfer_amount(card):
    print('\nTransfer')
    print('Enter card number:')
    to_transfer_card = input()
    if to_transfer_card == card:
        print("You can't transfer money to the same account!\n")
        return 0
    if check_luhn_algorithm(to_transfer_card):
        if check_card_availablity(to_transfer_card):
            print('Enter how much money you want to transfer:')
            _transfer_amount = int(input())
            if check_balance(_transfer_amount, card):
                do_transfer(card, _transfer_amount, to_transfer_card)
    else:
        print('Probably you made mistake in the card number. Please try again!\n')


def check_card_pin_details(card, pinno):
    cur.execute("select number,pin from card where number =" + card + " and pin=" + pinno + ";")
    row = cur.fetchone()
    if row is not None:
        if row[0] == card and row[1] == pinno:
            return True
        else:
            return False


def close_account(card):
    cur.execute("delete from card where number =" + card + ";")
    conn.commit()
    print('The account has been closed!\n')


def banking(card):
    print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
    choice = input()
    if choice == '1':
        print_balance(card)
        return True
    elif choice == '2':
        print('\nEnter income:')
        income = int(input())
        add_income(card, income)
        return True
    elif choice == '3':
        transfer_amount(card)
        return True
    elif choice == '4':
        close_account(card)
        return True
    elif choice == '5':
        print('You have successfully logged out!\n')
        return False
    elif choice == '0':
        print('Bye!')
        exit(0)


def login(card, pinno):
    global card_pin_details, balance
    if check_card_pin_details(card, pinno):
        print('\nYou have successfully logged in!\n')
        run = True
        while run:
            run = banking(card)
    else:
        print('Wrong card number or PIN!\n')


def check_if_table_exists():
    cur.execute(
        """create table if not exists card(
            id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0
            );""")


run = True
card_pin_details = {}
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
check_if_table_exists()
balance = 0
while run:
    print('\n1. Create an account\n2. Log into account\n0. Exit')
    user_choice = input()
    if int(user_choice) == 1:
        card_no, pin = create_account()
        print('\nYour card has been created')
        print("Your card number:\n" + card_no)
        print("Your card PIN:\n" + pin)

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
