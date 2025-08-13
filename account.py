from random import randrange
class Account:
    def __init__(self, balance:int):
        self.name = "Personal"
        self.number = self.generate_account_number()
        self.balance = balance

    def __str__(self):
        return f"Account Type: {self.name} nr: {self.number} balance: {self.balance}PLN"

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, amount: int):
        if(amount >= 0 ):
            self._balance = amount
        else:
            self._balance = 0
    
    def withdraw_money(self, amount:int):
        if(self.is_there_enough_money(amount) and amount > 0):
            self.balance -= amount
    
    def deposit_money(self, amount:int):
        if(amount > 0):
            self.balance += amount

    def transfer_money(self,amount:int,  other_account: "Account"):
        if not (self.is_there_enough_money(amount)):
            return 0

        self.withdraw_money(amount)
        other_account.deposit_money(amount)
        return amount
    
    def is_there_enough_money(self, amount: int):
        return self.balance - amount >= 0

    def generate_account_number(self):
        number_to_generate = ""
        for index in range (0,5):
            if(index == 0):
                randomised_number = randrange(1,9)
            else:
                randomised_number = randrange(10,99)
            number_to_generate+=f"{str(randomised_number)}-"

        return number_to_generate[:-1]


if __name__ == "__main__":
    test_account = Account(300)
    test_account.withdraw_money(200)
    test2_account = Account(5000)
    test2_account.deposit_money(500)
    test2_account.transfer_money(5200, test_account)
    print(f"{test_account.balance = } {test2_account.balance = }")

        