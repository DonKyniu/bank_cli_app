from accountmanager import AccountManager
from useraccountmanager import UserAccountManager
from datafilemanager import DataFileManager
import pwinput
from person import Person
import time
from os import system
 
def display_welcome_message():
    print("Welcome to Bank")
    time.sleep(1)
    print("All options which you can perform will be displayed below")
    time.sleep(1)
    print("Please remember to be vigiliant - our app is the only one to interact with our bank!")
    time.sleep(1)
    print("if you see anything suspicious or need any help - please call us at 999-999-999")
    time.sleep(1)
    
def show_intial_screen_messages():
    print("Welcome to Bank")
    time.sleep(0.5)
    print("To continue you need to login or register if you don't have account at our Bank just yet")

def show_start_options():
    print("-----------------------------------------------")
    print("1.Login")
    print("2.Change password")
    print("3.Register new account")
    print("0.Exit program")

def show_user_options():
   print("-----------------------------------------------")
   time.sleep(1)
   print("1.Show account information")
   print("2.Manage Account")
   print("0.Logout")

def show_admin_options():
    print("---ADMIN MENU---")
    time.sleep(1)
    print("1.Get all accounts")
    print("2.Get accounts sorted by balance")
    print("3.Get customer information")
    print("4.Manage customer account(impersonate)")
    print("5.Create new account")
    print("6.Remove account")
    print("0.Logoff")
    print("h.to display this menu again")

def show_customer_information_submenu():
    print("-----------------------------------------------")
    print("1.Find customer(s) by full name")
    print("2.Find customer(s) by name ")
    print("3.Find customer(s) by surname")
    print("4.Find customer by ID")
    print("5.Find customer by account number")
    print("0.Return to menu")
    print("h.to display this menu again")


def show_account_management_submenu():
    print("----------------------------------------------")
    print("1.Check current account balance")
    print("2.Transfer money")
    print("3.Deposit money")
    print("4.Withdraw money")
    print("0.Go back to main menu")
    print("h.To display this menu again")

def show_money_deposit_and_withdraw_options():
    print("-----------------------------------------------")
    print("1.50PLN")
    print("2.100PLN")
    print("3.200PLN")
    print("4.500PLN")
    print("5.1000PLN")
    print("6.Custom Amount")
    print("0.Cancel")

def initialize_data(data_file_manager: DataFileManager, account_manager: AccountManager, user_account_manager: UserAccountManager):
    loaded_data = data_file_manager.import_data()
    loaded_reserved_data = data_file_manager.load_reserved_data()

    account_manager.accounts = loaded_data["bank_accounts_data"]
    account_manager.accounts_number_taken = loaded_reserved_data["reserved_account_nr"]

    user_account_manager.user_base = loaded_data["user_database_data"]
    user_account_manager._usernames_taken = loaded_reserved_data["reserved_usernames"]

def save_data(data_file_manager:DataFileManager, user_account_manager: UserAccountManager, account_manager:AccountManager):
    data_file_manager.export_data(user_account_manager.get_all_people_from_base(), account_manager.get_all_accounts(), user_account_manager.get_all_data())
    data_file_manager.save_reserved_data(user_account_manager._usernames_taken, account_manager.accounts_number_taken)

def show_exit_information():
    print("Thank you for using our bank services and goodbye!")
    time.sleep(1)

def ask_for_name_and_surname():
    name = str(input("Please enter name "))
    surname = str(input("Please enter surname "))
    
    return name, surname

def set_up_password():
    new_password = pwinput.pwinput("Enter new password: ")
    while(is_password_not_validated(new_password)):
        print("Password does not meet the criteria! Try again")
        time.sleep(0.5)
        new_password = pwinput.pwinput("Enter new password: ")
        
    return new_password

def change_password(user_account_manager : UserAccountManager, is_acccessed_by_admin = False):
    if(is_acccessed_by_admin):
        username = str(input("Please enter person username to confirm identity "))
    else:
        username = str(input("Please enter username "))

    if not(is_acccessed_by_admin):
        password = str(pwinput.pwinput("Enter current password "))
        if not(user_account_manager.is_login_successfull(username, password)):
            print("Invalid username or password!")
            return
    
    user_data = user_account_manager.get_user(username)
    if(user_data == None):
        print("No such account in database!")  # this check is made when admin is changing password for user to prevent exception when given  username is not found
        return
    
    if(user_data.locked):
        print("Account locked! Please contact us in order to unlock it!")
        return
    
    new_password = set_up_password()
    user_account_manager.create_new_password(new_password, user_data)
    print("Password changed successfully!")
    time.sleep(1)

def is_password_not_validated(password:str):
    return not UserAccountManager.is_password_meeting_requirements(password)

def create_new_user_account(account_type:str, user_account_manager: UserAccountManager, person: Person, password:str):
    return user_account_manager.create_new_user_account(person, password, account_type)

def create_new_account(user_account_manager: UserAccountManager , account_manager: AccountManager):
    print("Thank you for selecting our bank services!")
    time.sleep(1)
    name_surname = ask_for_name_and_surname()
    birth_date = str(input("Please enter birth date in format: dd.mm.yyyy "))
    new_account = account_manager.create_new_user_account(name_surname[0], name_surname[1], birth_date)

    if(new_account == None):
        print("You need to be at least 18 years old to create account!")
        time.sleep(1)
        print("Or you didn't provide a date in valid format!")
        return
    
    print("Please enter new password - at least 8 characters including 1 or more digits, 1 or more special characters")

    new_password = set_up_password()

    new_user = create_new_user_account("user", user_account_manager, new_account, new_password)
    account_manager.create_new_account(new_account)

    time.sleep(0.5)
    print(f"account has been created:\n username is {new_user.username}")
    time.sleep(0.5)
    print("Details about your account you can find once you login with username provided and password you just set!")

def create_new_account_admin_version(user_account_manager: UserAccountManager, account_manager: AccountManager):
    account_type = str(input("Type \"adm\" for admin account or \"usr\" for user "))

    if(account_type == "adm"):
        admin_person = Person("Admin", "Admin", "no birth date")
        account = create_new_user_account("admin",user_account_manager, admin_person,"admin")

        print(f"admin account has been created\nusername: {account.username} and password admin - when you first time login it will ask you to set new password")
    elif(account_type == "usr"):
        create_new_account(user_account_manager, account_manager)
    else:
        print("invalid account type!")


def remove_account(account_manager: AccountManager,user_account_manager: UserAccountManager):
    customer_username_to_remove = str(input("Enter username of person to remove "))
    user, customer = user_account_manager.get_user_and_person(customer_username_to_remove)
    
    if(user == None):
        print("Such account not found in our system!")
        return
    
    account_manager.remove_account(customer)
    user_account_manager.remove_user_account(user)
    print("Account has been removed!")

def login_to_account(user_account_manager: UserAccountManager):
    not_logged_in = True
    login_attempts = 0
    
    while(not_logged_in):
        username = str(input("Please enter your username: "))
        potential_logged_in_user  = get_person_data(user_account_manager, username)

        if(potential_logged_in_user != None):
            if(potential_logged_in_user[0].locked):
                print("You are locked out - please contact us in order to unlock it!")
                return
        
        password = pwinput.pwinput()
        login_attempts+=1
        
        (not_logged_in := False) if user_account_manager.is_login_successfull(username, password) else (not_logged_in := True)

        if(not_logged_in and login_attempts < UserAccountManager.max_logon_attempts):
            print("Invalid username or password!")
            if(potential_logged_in_user != None):
                potential_logged_in_user[0].failed_logon_attempts+=1

            continue

        elif(not_logged_in and login_attempts == UserAccountManager.max_logon_attempts):
            print("Unfortunately you tried to login too many times with no success") 
            if(potential_logged_in_user!=None):

                if(potential_logged_in_user[0].failed_logon_attempts >= UserAccountManager.max_logon_attempts -1 ):
                    lock_user_account(user_account_manager, potential_logged_in_user[1].id)
            system("pause")
            return
        
        user_account_manager.unlock_account(potential_logged_in_user[0]) # the only purpose is to clear failed_logon_attempts back to 0
        return potential_logged_in_user
    
def unlock_user_account(user_account_manager: UserAccountManager, user_id: str): 
    user_to_unlock = user_account_manager.get_user_by_id(user_id)                
    user_account_manager.unlock_account(user_to_unlock)

    print(f"{user_to_unlock.username} unlocked!")

def lock_user_account(user_account_manager: UserAccountManager, user_id:str):
    user_account = user_account_manager.get_user_by_id(user_id)
    if(user_account == None):
        return
        
    user_account_manager.lock_account(user_account)                                  

def get_person_data(user_account_manager : UserAccountManager, username:str):
    username, person = user_account_manager.get_user_and_person(username)
    return [username, person] if username != None else None

def show_account_information(account_manager: AccountManager, logged_in_person: Person):
    customer_account = account_manager.get_customer_account(logged_in_person)
    print()
    if(customer_account == None):
      print("Such account not found in our system!")
      return
    
    print(customer_account[0])
    
def show_all_accounts_information(account_manager: AccountManager):
    accounts = account_manager.get_all_accounts()
    for owner, owner_accounts in accounts.items():
        print(f"{owner.name} {owner.surname}")
        for account in owner_accounts:
            print(" ",account)

def show_accounts_sorted_by_balance(account_manager: AccountManager):
    sort_order = str(input("Type \"asc\" for ascending order or \"desc\" for descending "))
    if(sort_order == "asc"):
         accounts_sorted_by_balance = account_manager.get_accounts_sorted_by_balance()
    elif(sort_order == "desc"):
         accounts_sorted_by_balance = account_manager.get_accounts_sorted_by_balance(reversed_order= True) 
    else:
        print("Wrong parameter!")
        return
    
    for account in accounts_sorted_by_balance:
        print(account)

def get_user_information(account_manager: AccountManager, info_type:str = "fullname"): 
    if(info_type == "fullname"):
        name_surname = ask_for_name_and_surname()
        customers_information =  account_manager.get_customer_by_full_name(name_surname[0], name_surname[1])

    elif(info_type == "name"):
        name = input("Enter name: ")
        customers_information = account_manager.get_customers_by_name(name)
    
    elif(info_type == "surname"):
        surname = input("Enter surname: ")
        customers_information = account_manager.get_customers_by_surname(surname)
    
    elif(info_type == "ID"):
        id_data = input("Enter ID number:")
        customers_information = account_manager.get_customer_by_id(id_data)
    
    if(customers_information == None):
        print("Customer(s) not found!")
        return
    
    for customer in customers_information:
        print(f"{customer.name} {customer.surname} age:{customer.get_person_age()} years old id:{customer.id}")
        customer_accounts = account_manager.get_customer_account(customer)
        for account in customer_accounts:
            print(f"  {account}")

def get_user_information_by_bank_account(account_manager: AccountManager):
    account_nr = str(input("Please enter account number: "))
    user, account = account_manager.get_account_by_number(account_nr)
    if(user == None):
        print("Not found!")
        return
    
    print(f"{user.name} {user.surname} {user.get_person_age()} years old")
    print("Associated with",account)

def get_impersonated_user_data(username:str , user_account_manager:UserAccountManager):
    user_to_impersonate, person_to_impersonate  = user_account_manager.get_user_and_person(username)
    if(user_to_impersonate == None):
        return None
    
    return person_to_impersonate


def transfer_money(account_manager: AccountManager, user_account):
    account_number = str(input("Please enter account number where you want to transfer money "))
    account_owner , transfer_account = account_manager.get_account_by_number(account_number)

    if(account_owner == None and transfer_account == None):
        print("There is no such account number in our systems!")
        time.sleep(1)
        return
    else:
        print("Account found!")
        time.sleep(1)
    
    amount = int(input("Please enter amount of money to transfer - 1 at minimum "))
    transfer_result = account_manager.transfer_money(user_account, transfer_account, amount)
    if(transfer_result == 0):
        print("Transfer not successfull. You either tried to send 0PLN or have not sufficient funds on your account!")
    else:
        print(f"Transfer successfull. {transfer_result}PLN sent to {account_number}")


def deposit_money(account_manager: AccountManager, person:Person, user_account, amount: int):
    deposit_result = account_manager.deposit_money_to_account(user_account, person, amount)

    if(deposit_result  == 0):
        print("Deposit was not successfull")
        return

    print("Money has been deposit in your account")
    time.sleep(0.5)
    
def withdraw_money(account_manager:AccountManager, person, user_account, amount:int):
    withdraw_result = account_manager.withdraw_money_from_account(user_account, person, amount)
    print(f"{withdraw_result = }")
    if(withdraw_result == 0):
        print("Withdraw was not succesfull")
        return
    
    print(f"You have withdrawed {withdraw_result}PLN from {user_account.number}")
    time.sleep(0.5)

def obtain_customer_data(account_manager: AccountManager):
    while(True):
        show_customer_information_submenu()
        command = str(input("Enter command: "))
        
        if(command == "1"):
            get_user_information(account_manager) # by default it is a full name
            system("pause")
            
        elif(command == "2"):
            get_user_information(account_manager, "name")
            system("pause")
            
        elif(command == "3"):
            get_user_information(account_manager, "surname")
            system("pause")
        
        elif(command == "4"):
            get_user_information(account_manager, "ID")
            system("pause")
        
        elif(command == "5"):
            get_user_information_by_bank_account(account_manager)
            system("pause")
        
        elif(command == "0"):
            break
            


def manage_account(account_manager: AccountManager,user_account_manager : UserAccountManager,logged_in_user: Person, accessed_by_admin: bool = False):
    customer_data = logged_in_user
    try:
        account_data = account_manager.get_customer_account(logged_in_user)
    except:
        print("Warning! This person do not have any bank accounts associated. Functionality related to bank account management will NOT WORK")

    show_account_management_submenu()
    submenu_active = True

    while(submenu_active):
        user_selection = input("Please enter command: ")
        if(user_selection == "1"):
            print(f"Account Nr {account_data[0].number} current balance: {account_data[0].balance}PLN")
            system("pause")

        elif(user_selection == "2"):
            transfer_money(account_manager, account_data[0])

        elif(user_selection == "3"):
            show_money_deposit_and_withdraw_options()
            amount = ask_for_amount()

            if(amount == 0 or amount == None):
                continue

            deposit_money(account_manager, customer_data, account_data[0], amount)

        elif(user_selection == "4"):
            show_money_deposit_and_withdraw_options()
            amount = ask_for_amount()

            if(amount == 0 or amount == None):
                continue

            withdraw_money(account_manager, customer_data, account_data, amount)

        elif(user_selection == "chpwd" and accessed_by_admin == True):
            change_password(user_account_manager, accessed_by_admin)
        
        elif(user_selection == "unlock" and accessed_by_admin == True):
            unlock_user_account(user_account_manager , logged_in_user.id)
        
        elif(user_selection == "lock" and accessed_by_admin == True):
            lock_user_account(user_account_manager, logged_in_user.id)
            print("Account locked!")
        
        elif(user_selection == "h"):
            show_account_management_submenu()

        elif(user_selection == "0"):
            submenu_active = False

def ask_for_amount():
    command = str(input("Enter command: "))
    amount = 0

    if(command == "1"):
        amount = 50
        
    elif(command == "2"):
        amount = 100
    
    elif(command == "3"):
        amount = 200
    
    elif(command == "4"):
        amount = 500
    
    elif(command == "5"):
        amount = 1000
    
    elif(command == "6"):
        amount = int(input("Enter custom amount: "))

    elif(command == "0"):
        amount = 0

    else:
        print("Invalid command")
        return None

    return amount

def execute_app():
    is_app_running = True
    not_logged_in = True
    user_logged_in = None
    account_manager = AccountManager()
    user_accont_manager = UserAccountManager()
    data_file_manager = DataFileManager()

    try:
        initialize_data(data_file_manager, account_manager , user_accont_manager)
    except:  # if data could not be initialized - create first admin account
        first_admin_person = Person("Admin", "Admin", "no date")
        admin_account = user_accont_manager.create_new_user_account(first_admin_person, "admin", "admin")
        user_accont_manager._usernames_taken.pop(0) # to remove username created by method from user account_manager to don't occupy place when not needed
        user_accont_manager._usernames_taken.append("ADM013") # add username to reserved list to avoid situation where two admins share same username - odds are small but it's still possible.
        admin_account.username = "ADM013"


    show_intial_screen_messages()

    while(is_app_running):
        while(not_logged_in):
            show_start_options()
            user_selection = str(input("Enter command: "))
        
            if(user_selection == "1"):
                user_logged_in = login_to_account(user_accont_manager)

                if(user_logged_in  == None): # in case if user will fail to login after max limit of attemps specified - go back to start of the loop
                    continue

                while(user_logged_in[0].password_change_required):# loop as long as user won't set up correct password when asked to change it
                    change_password(user_accont_manager)
                
                print(f"Welcome {user_logged_in[1].name}")
                not_logged_in = False
            
            elif(user_selection == "2"):
                change_password(user_accont_manager)
            
            elif(user_selection == "3"):
                create_new_account(user_accont_manager, account_manager)

            elif(user_selection == "0"):
                show_exit_information()
                is_app_running = False
                break

        if not (is_app_running):
            break
            
        if(user_logged_in[0]._account_type == "admin"):
            show_admin_options()
        else:
            show_user_options()
            
        user_selection = input("Enter command: ")

        if(user_logged_in[0]._account_type == "user"):
            if(user_selection == "1"):
                show_account_information(account_manager, user_logged_in[1]) # pass person data 

            elif(user_selection == "2"):
                manage_account(account_manager,user_accont_manager,user_logged_in[1])# pass person data
            
            elif(user_selection == "0"):
                not_logged_in = True
                time.sleep(1)
                continue
        else:

            if(user_selection == "1"):
                show_all_accounts_information(account_manager)
                system("pause")

            elif(user_selection == "2"):
               show_accounts_sorted_by_balance(account_manager)
               system("pause")
            
            elif(user_selection == "3"):
                obtain_customer_data(account_manager)
            
            elif(user_selection == "4"):
                username = str(input("Enter username of person to impersonate "))
                user_to_impersonate = get_impersonated_user_data(username, user_accont_manager)
                if(user_to_impersonate == None):
                    print("Invalid user!")
                    continue

                manage_account(account_manager,user_accont_manager, user_to_impersonate, accessed_by_admin = True)

            elif(user_selection == "5"):
                create_new_account_admin_version(user_accont_manager, account_manager)

            elif(user_selection == "6"):
                remove_account(account_manager, user_accont_manager)
            
            elif(user_selection == "0"):
                not_logged_in = True
                time.sleep(1)
                continue

    save_data(data_file_manager, user_accont_manager, account_manager)

def main():
    system("title Bank CLI App ")
    execute_app()

main()