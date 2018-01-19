class Customer(object):
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise RuntimeError('Insufficient funds')
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

cena = Customer('John Cena,', 250000.55)

foo = 2323
name = 'Jo'
print('give me %s dollars, %s boy' % (foo + 3, name*2))
