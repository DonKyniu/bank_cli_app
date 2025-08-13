from random import randint
from string import ascii_letters
from datetime import datetime
class Person:
    __id = "000"
    max_wallet_amount = 3000

    def __init__(self, name:str, surname:str, birth_date:str):
            self.name = name
            self.surname = surname
            self.birth_date = birth_date
            self.id = self.__obtain_id()
            self.cash_in_wallet = self.randomise_starting_money()

    def __str__(self):
         return f"{self.name} {self.surname} born in {self.birth_date}"

    @property
    def birth_date(self):
        return self._birth_date
    
    @birth_date.setter
    def birth_date(self, birth_date:str):
        birth_date_splitted = birth_date.split(".")

        if(self.__is_birth_date_correct(birth_date_splitted)):
             self._birth_date = birth_date
        else:
             self._birth_date = "invalid date"
             
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name:str):
              if not (self.__is_name_correct(name, 3)):
               self._name = "unknown"
              else:
               self._name = name
    @property
    def surname(self):
         return self._surname
    
    @surname.setter
    def surname(self, surname: str):
         if(not(self.__is_name_correct(surname))):
              self._surname = "unknown"
         else:
               self._surname = surname

    def __obtain_id(self):
         if(self.birth_date == "invalid date"):
              return "999999999"
         
         birth_date_in_pieces = self.birth_date.split(".")
         current_id = Person.__id 
         Person.__calculate_new_id()
         return current_id + str(birth_date_in_pieces[2][2:4]) + str(birth_date_in_pieces[0]) + str(birth_date_in_pieces[1])   
   
    def __is_birth_date_correct(self, birth_date: list):
         #birthday_regex_format = r"^(0[1-9]|1[0-9]|2[0-9]|3[0-1])\.(0[1-9]|1[0-2])\.([0-9][0-9][0-9][0-9])$"
         try:
              new_dateTime = datetime(int(birth_date[2]), int(birth_date[1]), int(birth_date[0]))
         except:
               return False
         
         return True
    
    def __is_name_correct(self, name_or_surname:str , min_length: int = 2):
          if(len(name_or_surname)  < min_length):
               return False
          elif(any(letter not in ascii_letters for letter in name_or_surname)):
               return False
          
          return True
    def __check_if_age_is_correct(self, age: int):
          return age >=0 and age <=120
    
    @classmethod
    def __calculate_new_id(cls):
         next_id = int(Person.__id)
         next_id+=1
         
         if(next_id < 10):
              Person.__id = "00" + str(next_id)
         elif(next_id  < 100):
               Person.__id = "0"+ str(next_id)
         else:
              Person.__id = str(next_id)
              

    def get_person_age(self):
         if(self.birth_date == "invalid date"):
              return 0
         
         birth_date_converted_to_date = datetime.strptime(self.birth_date,"%d.%m.%Y")
         age = datetime.now() - birth_date_converted_to_date
         age = int(age.days / 365)
         if(self.__check_if_age_is_correct(age)):
              return age
         else:
              return 0
    
    @property
    def cash_in_wallet(self):
          return self._cash_in_wallet
    
    @cash_in_wallet.setter
    def cash_in_wallet(self, cash):
         if(cash >= 0):
              self._cash_in_wallet = cash

    def remove_cash_from_wallet(self, amount):
         if(self.cash_in_wallet - amount >= 0 and amount > 0):
              self.cash_in_wallet -= amount

    def add_cash_to_wallet(self,amount):
         if(amount > 0 and amount + self.cash_in_wallet <= self.__wallet_max_amount):
              self.cash_in_wallet += amount
         elif(amount + self.cash_in_wallet >= Person.max_wallet_amount):
              self.cash_in_wallet = Person.max_wallet_amount
    
    def randomise_starting_money(self):
       return randint(500,Person.max_wallet_amount)
    

if __name__ == "__main__":
     test_person = Person("Krs","mi", "03.11.2024")
     print(test_person.id)
     test_person2 = Person("Hello","Mate", "24.06.2000")
     print(test_person2.surname)
     test_person.add_cash_to_wallet(350)
     print(test_person.cash_in_wallet)

     
    