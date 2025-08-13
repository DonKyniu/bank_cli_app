import json
from pathlib import Path
from person import Person # the only reason for import both person and useraccount is to have IDE highlight
from useraccount import UserAccount
from account import Account

class DataFileManager:
    data_path = Path("data")
    
    PEOPLE_DATA_FILENAME = "people_list"
    BANK_ACCOUNTS_DATA_FILENAME = "bank_accounts_data"
    USER_DATABASE_FILENAME = "user_database"

    def load_from_file(self, file_name):
        if not(DataFileManager.data_path.exists()):
            return # as data was not yet saved and folder does not exist, just simply end execution of this method

        file_path = f"{str(DataFileManager.data_path)}/{file_name}.json"

        with open(f"{file_path}", "r") as data:
            data_converted = json.load(data)

        return data_converted
    
    def save_to_file(self, file_name, data_to_save):  
        if not (DataFileManager.data_path.exists()):
            DataFileManager.data_path.mkdir()

        
        file_path = f"{str(DataFileManager.data_path)}/{file_name}.json"

        with open(f"{file_path}", "w") as database:
            database.write(json.dumps(data_to_save, indent= 2))
            
    def save_reserved_data(self, user_accounts_taken: list, bank_numbers_taken: list):
        reserved_data = {"reserved_usernames": user_accounts_taken, "reserved_account_nr": bank_numbers_taken}
        self.save_to_file("reserved", reserved_data)

    def load_reserved_data(self):
        reserved_data = self.load_from_file("reserved")
        
        return reserved_data
    
    def export_data(self, people_list:list , bank_accounts:dict, user_accounts:dict):
        people_dict = self.convert_people_list_to_dict(people_list)
        bank_accounts_dict = self.convert_bank_accounts_obj_to_dict(bank_accounts)
        user_accounts_dict = self.convert_user_accounts_to_dict(user_accounts)
        
        self.save_to_file(DataFileManager.PEOPLE_DATA_FILENAME, people_dict)
        self.save_to_file(DataFileManager.BANK_ACCOUNTS_DATA_FILENAME, bank_accounts_dict)
        self.save_to_file(DataFileManager.USER_DATABASE_FILENAME, user_accounts_dict)

    def import_data(self):
        list_of_people = self.load_from_file(DataFileManager.PEOPLE_DATA_FILENAME)
        list_of_bank_accounts = self.load_from_file(DataFileManager.BANK_ACCOUNTS_DATA_FILENAME)
        list_of_users = self.load_from_file(DataFileManager.USER_DATABASE_FILENAME)
        
        people_as_objects = self.convert_to_people_obj(list_of_people)
        bank_accounts_and_people = self.associate_people_and_bank_accounts(people_as_objects, list_of_bank_accounts)
        users_and_people = self.associate_people_and_user_accounts(people_as_objects , list_of_users)
        
        data_imported = {"bank_accounts_data": bank_accounts_and_people, "user_database_data": users_and_people}

        return data_imported

    def convert_people_list_to_dict(self, people_list:list):
        people_list_in_dict = {}
        
        for person in people_list:
            if(isinstance(person, Person)):
                if not(person.id in people_list_in_dict):
                    people_list_in_dict[person.id] = {}

                people_list_in_dict[person.id]["name"] = person.name
                people_list_in_dict[person.id]["surname"] = person.surname
                people_list_in_dict[person.id]["birthdate"] = person.birth_date
                people_list_in_dict[person.id]["cash_in_wallet"] = person.cash_in_wallet

        return people_list_in_dict
    
    def convert_user_accounts_to_dict(self, user_accounts:dict): # at the moment only one account per person is supported
        accounts_as_dict = {}
        
        for user, person in user_accounts.items():
            if(isinstance(person, Person)):
                if not(person.id in accounts_as_dict):
                    accounts_as_dict[person.id] = {}

            if(isinstance(user, UserAccount)):
                accounts_as_dict[person.id]["username"] = user.username
                accounts_as_dict[person.id]["account_type"] = user._account_type
                accounts_as_dict[person.id]["password"] = user.password
                accounts_as_dict[person.id]["password_salt"] = user._password_salt
                accounts_as_dict[person.id]["password_change_required"] = user.password_change_required
                accounts_as_dict[person.id]["failed_logon_attempts"] = user.failed_logon_attempts
                accounts_as_dict[person.id]["locked"] = user.locked

        return accounts_as_dict
    
    def convert_bank_accounts_obj_to_dict(self, bank_accounts:dict): # method converts bank accounts objects to dictionary in format {person.id:{attribute:value}}
        accounts_in_dict = {}
        
        for person, accounts in bank_accounts.items():
            if(isinstance(person, Person)):
                if not(person.id in accounts_in_dict):
                    accounts_in_dict[person.id] = {}
            for account in accounts:
                if(isinstance(account, Account)):
                    accounts_in_dict[person.id]["account_name"] = account.name 
                    accounts_in_dict[person.id]["account_number"] = account.number
                    accounts_in_dict[person.id]["balance"] = account.balance
                    
        return accounts_in_dict
    
    def save_taken_user_names_and_account_nr(self, usernames_taken:list, account_numbers_taken: list):
        simple_dict = {"username_taken":usernames_taken, "bank_numbers_taken": account_numbers_taken}
        self.save_to_file("reserved_names", simple_dict)
    
    def convert_to_people_obj(self, people_list:dict):
        people_as_objects = []
        for id, person_data in people_list.items():

            person_name = person_data["name"]
            person_surname = person_data["surname"]
            person_birthdate = person_data["birthdate"]
            person_cash_in_wallet = person_data["cash_in_wallet"]

            person = Person(person_name, person_surname, person_birthdate)
            person.id = id
            person.cash_in_wallet = person_cash_in_wallet
            
            people_as_objects.append(person)

        return people_as_objects
    
    def associate_people_and_bank_accounts(self, people_object_list: list, bank_accounts_dict: dict):
        accounts_dict = {}
        for id, bank_account_dict in bank_accounts_dict.items():
            for person in people_object_list:
                if(isinstance(person, Person)):
                    if(id == person.id):
                        accounts_dict[person] =[]
                        account_name = bank_account_dict["account_name"]
                        account_number = bank_account_dict["account_number"]
                        account_balance = bank_account_dict["balance"]

                        person_account = Account(account_balance)

                        person_account.name = account_name
                        person_account.number = account_number
                        
                        accounts_dict[person].append(person_account)

        return accounts_dict
    
    def associate_people_and_user_accounts(self, people_object_list:list, user_dict:dict):
        users_dict = {}

        for id, user_details in user_dict.items():
            for person in people_object_list:
                if(isinstance(person, Person)):
                    if(id == person.id):
                        username = user_details["username"]
                        account_type = user_details["account_type"]
                        password = user_details["password"]
                        password_salt = user_details["password_salt"]
                        password_change_required = user_details["password_change_required"]
                        failed_logon_attempts = user_details["failed_logon_attempts"]
                        user_locked = user_details["locked"]
                        
                        user = UserAccount(username, account_type, password, password_salt)
                        user.password_change_required = password_change_required
                        user.failed_logon_attempts = failed_logon_attempts
                        user.locked = user_locked

                        users_dict[user] = person

        return users_dict

    
if __name__ == "__main__":
    data_file_manager = DataFileManager()
    person_k_m = Person("Krzysztof", "Muszynski", "13.07.1997")
    person_t_m = Person("Tobiasz", "Merk", "02.10.1993")
    person_m_h = Person("Michal", "Jen", "02.05.1991")
    person_p_j = Person("Pamela", "Anderson", "07.05.1996")
    person_m_j = Person("Michael", "Jackson", "29.08.1958")

    k_m_user_account = UserAccount("km0123", "user", "12345", "no salt")
    t_m_user_account = UserAccount("tm0123", "user",  "pwd333", "no salt")
    m_h_user_account = UserAccount("mh0002" , "user", "452213123", "no salt")
    p_j_user_account = UserAccount("pj12323154", "user", "003007" , "no salt")
    m_j_user_account = UserAccount("billy345566", "user", "jean0123", "no salt")

    
    k_m_bank_account = Account(2500)
    t_m_bank_account = Account(1000)
    m_h_bank_account = Account(5000)
    p_j_bank_account = Account(500)
    m_j_bank_account = Account(50000)

    people_list = [person_k_m , person_t_m , person_m_h , person_p_j , person_m_j]
    user_account_dict = {k_m_user_account: person_k_m, t_m_user_account: person_t_m , m_h_user_account: person_m_h, p_j_user_account: person_p_j, m_j_user_account: person_m_j}
    bank_account_dict = {person_k_m: k_m_bank_account, person_t_m: t_m_bank_account, person_m_h: m_h_bank_account, person_p_j: p_j_bank_account, person_m_j: m_j_bank_account}

    bank_account_taken = [account.number for account in bank_account_dict.values()]
    user_name_taken = [user.username for user in user_account_dict.keys()]

   # data_file_manager.export_data(people_list, bank_account_dict , user_account_dict)
    #imported_data = data_file_manager.import_data()
    #print(imported_data)
    
    data_file_manager.save_reserved_data(user_name_taken, bank_account_taken)
    result = data_file_manager.load_reserved_data()
    print(result)


            



