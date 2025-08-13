from account import Account
from person import Person

class AccountManager():
    minimum_age = 18

    def __init__(self):
        self.accounts = {}
        self.accounts_number_taken = []

    def create_new_user_account(self, name: str, surname: str, birth_date: str):
        new_customer = Person(name, surname, birth_date)
        if not(new_customer.get_person_age() >= AccountManager.minimum_age):
            return None

        self.accounts[new_customer] = []
        return new_customer

    def create_new_account(self, person : Person):
        if not(person in self.accounts.keys()):
            return None

        new_account = Account(0)
        while(new_account.number in self.accounts_number_taken):
            new_account.number = new_account.generate_account_number()

        self.accounts[person].append(new_account)
        self.accounts_number_taken.append(new_account.number)

        return new_account
    
    def remove_account(self, person:Person):
        return self.accounts.pop(person, None)
    
    def get_all_accounts(self):
        return self.accounts
    
    def get_all_customers(self):
        return self.get_all_accounts().keys()
    
    def get_customer_by_id(self, id:str):
        customers_list = self.get_all_customers()

        customer_with_id = [customer for customer in customers_list if customer.id == id]
        if(len(customer_with_id) > 0):
            return customer_with_id
        else:
            return None
        
    def get_customers_by_name(self, name:str):
        customers_list = self.get_all_customers()

        customers_with_name = [customer for customer in customers_list if customer.name == name]
        if(len(customers_with_name) == 0):
            return None
        return customers_with_name
    
    def get_customers_by_surname(self, surname:str):
        customers_list = self.get_all_customers()
        customers_with_surname = [customer for customer in  customers_list if customer.surname == surname]
        if(len(customers_with_surname) == 0):
            return None

        return customers_with_surname
    
    def get_customer_by_full_name(self, name:str, surname:str):
        customers_list = self.get_all_customers()

        customers_details = [customer for customer in customers_list if customer.name == name and customer.surname == surname]
        if(len(customers_details) == 0):
            return None

        return customers_details
    
    def get_account_by_number(self, account_nr:str):
        accounts_dict = self.get_all_accounts()

        for owner, accounts in accounts_dict.items():
            for account in accounts:
                if(isinstance(account, Account)):
                    if(account_nr == account.number):
                     return owner, account
                    
        return None, None
    
    def get_customer_account(self, person: Person):
        if(person == None):
            return None
    
        return self.accounts[person]
        
    def get_account_owner(self, account: Account):
        for username, accounts in self.accounts.items():
            for current_account in accounts:
                if(isinstance(current_account, Account)):
                    if(current_account == account):
                        return username
        return None   
    
    def get_accounts_sorted_by_balance(self, reversed_order = False):
        lists_of_accounts = list(self.accounts.values())
        lists_of_accounts_merged = []
        
        for account_list in lists_of_accounts[:]:
            lists_of_accounts_merged.extend(account_list)

        return sorted(lists_of_accounts_merged, key = lambda account: account.balance, reverse= reversed_order)
        
    def deposit_money_to_account(self, account: Account , person: Person, amount : int):
        cash_in_wallet_before_transaction = person.cash_in_wallet
        person.remove_cash_from_wallet(amount)
        if(person.cash_in_wallet != cash_in_wallet_before_transaction):
            account.deposit_money(amount)
            return amount
        
        return 0

    def withdraw_money_from_account(self, account: Account, person: Person, amount: int):
        cash_in_account_before_transaction = account.balance
        account.withdraw_money(amount)
        if(account.balance != cash_in_account_before_transaction):
            person.add_cash_to_wallet(amount)
            return amount
        
        return 0

    def transfer_money(self, account: Account, account_to_transfer : Account, amount: int):
        return account.transfer_money(amount, account_to_transfer)
    
if __name__ == "__main__":
    account_manager = AccountManager()
    michal_account = account_manager.create_new_user_account("Michal", "Hliwa", "02.04.1991")
    tobiasz_account = account_manager.create_new_user_account("Tobiasz", "Muszynski", "02.10.1993")
    krzysztof_account = account_manager.create_new_user_account("Krzysztof", "Muszynski", "13.07.1997")

    m_acc = account_manager.create_new_account(michal_account)
    t_acc = account_manager.create_new_account(tobiasz_account)
    k_acc = account_manager.create_new_account(krzysztof_account)

    m_acc.number = "6-94-32-14-14"
    k_acc.number = "15-30-89-00-37"
    print(t_acc.number)
    #print(tobiasz_account)
    #print(krzysztof_account)

    michal_person = account_manager.get_customer_by_full_name("Michal", "Hliwa")
    #print(michal_person)
   # print(account_manager.get_all_accounts())
    customers = account_manager.get_all_customers()
    krzysztof_found = account_manager.get_customer_by_full_name("Krzysztof", "Muszynski")
    print(michal_person)
    owner, michaL_b_account = account_manager.get_account_by_number("6-94-32-14-14")
    print(michaL_b_account)
    print(owner)
    
    print(f"testing {account_manager.get_customer_account(michal_account)[0]}")
    
 
