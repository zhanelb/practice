class Account:
    def __init__(self, balance):
        self.balance = balance
    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        else:
            self.balance -= amount
            return self.balance
b, w = map(int, input().split())
acc = Account(b)
print(acc.withdraw(w))
