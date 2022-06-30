import itertools


class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        category_len = len(self.name)
        x = (30 - category_len) // 2

        to_print = '*' * x + self.name + '*' * x
        to_print += '\n'
        amount_format = '{amount:4.2f}'
        for d in self.ledger:
            y = len(d['description'])
            y = 29 - y if y < 23 else 6
            to_print += d['description'][:23] + ' ' + amount_format.format(amount=d['amount']).rjust(y)
            to_print += '\n'
        to_print += 'Total: ' + str(self.get_balance())

        return to_print

    def deposit(self, amount, description=''):
        d = {"amount": amount, "description": description}
        self.ledger.append(d)

    def withdraw(self, amount, description=''):

        if self.get_balance() > amount:
            d = {"amount": -amount, "description": description}
            self.ledger.append(d)
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for d in self.ledger:
            balance += d['amount']
        return balance

    def transfer(self, amount, category):

        withdraw_ok = self.withdraw(amount, description='Transfer to ' + category.name)
        if withdraw_ok:
            category.deposit(amount, description='Transfer from ' + self.name)
            return True

        else:
            return False

    def check_funds(self, amount):
        balance = self.get_balance()
        if amount > balance:
            return False
        else:
            return True


def create_spend_chart(categories):
    to_print = 'Percentage spent by category'

    d = dict()
    withdraw_total = 0

    for category in categories:
        ledger = category.ledger
        category_withdraw = 0
        for x in ledger:
            amount = x['amount']
            if amount < 0 and x['description'].startswith('Transfer') == False:
                category_withdraw -= amount
        withdraw_total += category_withdraw
        d[category.name] = category_withdraw


    for key in d:
        d[key] = (d[key] / withdraw_total) * 100

    # for (k,v) in d.items():
    #     print(k,v)
    for i in range(100, -10, -10):
        to_print += '\n' + str(i).rjust(3) + '| '
        for k in d.keys():
            if d[k] > i:
                to_print += 'o  '
            else:
                to_print += ' '*3

    to_print += '\n' + ' '*4 + '-'*10
    for c in itertools.zip_longest(*d.keys(), fillvalue=' '):
        s = '  '.join(c)
        to_print += '\n' + ' '*5 + s
        to_print += ' '*2

    return to_print
