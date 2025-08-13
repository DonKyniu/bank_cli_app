from useraccount import UserAccount
from string import punctuation, digits
from random import randrange
from person import Person
from hashlib import sha256
import re

class UserAccountManager:
    username_length = 6
    max_logon_attempts = 5


    def __init__(self):
        self.user_base= {}
        self._usernames_taken = []

    def create_new_user_account(self,person: Person, password:str, account_type:str):
        username = self.create_user_name(person.name, person.surname, account_type)

        while(self.__is_username_in_database(username)):
            username = self.create_user_name(person.name, person.surname)

        self._usernames_taken.append(username)

        password_salt = UserAccountManager.generate_salt()
        encrypted_password = self.encrypt_password(password, password_salt)

        new_account = UserAccount(username,account_type, encrypted_password, password_salt)
        if(account_type == "admin"):
            new_account.password_change_required = True
            self.inject_special_id(person, new_account)

        self.add_to_base(new_account,person)
        return new_account

    def remove_user_account(self, user_to_remove:UserAccount):
        return self.user_base.pop(user_to_remove, None)
    
    def add_to_base(self, user_to_add: UserAccount, person:Person):
        self.user_base[user_to_add] = person
    
    def create_user_name(self, name:str = "default", surname:str = "default", account_type:str = "user"):
        start_range = 1
        end_range = 5
        user_name = [""] * UserAccountManager.username_length
        if(account_type == "admin"):
            user_name[0] = "A"
            user_name[1] = "D"
            user_name[2] = "M"
            start_range = 3
            end_range = 6
        else:
            user_name[0] = surname[0]
            user_name[-1] = name[0]

        for character in range(start_range,end_range):
            random_number = randrange(0,9)
            user_name[character] = str(random_number)

        return "".join(user_name)
    
    def inject_special_id(self, admin_person: Person, new_accont: UserAccount):
        admin_id = "ADM"
        admin_person.id = admin_id + new_accont.username[3:]
        
    @classmethod
    def generate_salt(cls):
        salt = ""
        possible_salt_symbols = punctuation + digits
        for key in range(0,4):
            random_index = randrange(0, len(possible_salt_symbols) - 1)
            salt+=possible_salt_symbols[random_index]

        return salt
    
    def create_new_password(self, new_password:str, user: UserAccount):
        new_salt = UserAccountManager.generate_salt()
        encrypted_password = self.encrypt_password(new_password, new_salt)

        user.password = encrypted_password
        user._password_salt = new_salt
        user.password_change_required = False
    
    def encrypt_password(self, password:str, password_salt:str):
        encrypted_password = sha256((password + password_salt).encode()).hexdigest()
        return encrypted_password
        
    
    def verify_password_correctness(self, user_entered_password:str, password:str , password_salt: str):
        user_enetered_encrypted_password = self.encrypt_password(user_entered_password, password_salt)
        return password == user_enetered_encrypted_password

    def lock_account(self, user_account: UserAccount):
        user_account.locked = True
    
    def unlock_account(self, user_account: UserAccount):
        user_account.locked = False
        user_account.failed_logon_attempts = 0

    def get_user(self, user_name:str) -> UserAccount:
        found_user_name = [user for user in self.user_base.keys() if user.username == user_name]

        if(len(found_user_name) == 0):
            return None
        
        return found_user_name[0]
    
    def get_user_by_id(self, id:str):
        user_base = self.get_all_data()
        for user, person in user_base.items():
            if(person.id == id):
                return user
        return None
    
    def get_user_and_person(self, user_name:str):
        user = self.get_user(user_name)
        
        if(user == None):
            return None, None
        
        return user, self.user_base[user]
    
    def get_all_people_from_base(self):
        return list(self.get_all_data().values())
    
    def get_all_data(self):
        return self.user_base
    
    
    def is_login_successfull(self, username:str , password:str):
        user = self.get_user(username)
        if(user == None):
            return False
        
        return self.verify_password_correctness(password,user.password,user._password_salt)

    def __is_username_in_database(self, created_username:str):
        return any( username for username in self._usernames_taken if username == created_username)
    

    @classmethod
    def is_password_meeting_requirements(cls, password_to_evaluate: str):
        password_requirements = r"^(?=.*[A-Z])(?=.*[1-9])(?=.*[$%@!#^&*])[a-zA-Z0-9$%@!#^&*]{8,32}$"
        check_result = re.match(password_requirements, password_to_evaluate)

        if(check_result == None):
            return False
          
        return True
    

if __name__ == "__main__":
    user_manager = UserAccountManager()
    test_person = Person("Krzysztof", "Muszynski", "13.07.1997")
    test2_person = Person("Jack", "Daniels", "05.11.1975")
    test3_person = Person("Michael", "Bay", "20.05.1964")

    print(test2_person.id)


    


