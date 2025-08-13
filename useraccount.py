class UserAccount:
    def __init__(self,username:str, account_type:str, password:str, password_salt: str):
        self._account_type = account_type
        self.username = username
        self._password_salt = password_salt
        self.password = password
        self.password_change_required = False
        self.failed_logon_attempts = 0
        self.locked = False

    def __str__(self):
        return f"{self.username}"
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        self._username = username
        
    
if __name__ == "__main__":
    test_account = UserAccount("John", "Doe", "1234560")
    test2_account = UserAccount("Dam", "Nal", "1234560")
    print(test2_account.username)
    print(test_account.password)
    print(test2_account.password)
    print(test2_account.username)
