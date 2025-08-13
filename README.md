# Bank CLI APP in python
One of my first projects created in python. Simple banking CLI based app in order to practice python.

## Technologies used
Program was created in python. I used pwinput module for masking input when entering password. Other than that all other modules are build into python standard library.

## Project Goal
The main goal of this project was to practice python and  OOP(Object Oriented Programming).The program was not tested on Linux or other operating system. It should work on Windows machines.

Program itself does not have any GUI - It's cmd based so input from user is entering text - most of the times digit.

## What can be done in that program ?

In this program you can create new accounts, login(either as admin or user), check account balance, transfer money, deposit or withdraw it.
When withdrawing or depositing money is in fact role of ATM - for sake of simplicity and increase interactability  these functionalities are included in that program.

Each new account has randomised bank account number which is unique.

The same is for usernames - once created you get information about username.

Passwords are hashed using **sha256** function from hashlib module from python standard library  with addition of [password salt](https://en.wikipedia.org/wiki/Salt_(cryptography)).

By default balance is 0PLN(or any **other currency**  in fact).

### User type account ###
As user logged in - it's possible to check account balanace and perform basic account operations like depositing money, withdrawing it, transferring to other account
There are also some hidden functionalities but even if you know command - without admin privileges they will not work.


### Admin type account ###
As admin logged in user - you can add new accounts(user or admin) or remove existing ones, get information about particular person, impersonate person to perform actions on behalf

There are also some *"hidden"* functionalities in impersonation menu for admin user:

Admin can lock account by typing **lock** command

There is no information if lock was successful - but if command was typed in correctly account is locked

Similary, an account can be unlocked by typing **unlock** when in impersonation menu

In this case the information will appear: "Account 'username' was unlocked"

Admin can also change password for impersonated user - to trigger this action type **chpwd** command

## Additional Notes ##
All the data used in program is stored in .json files in data folder.

In this repo I have included example data files which are allowing to perform various operations either as user or admin.

It also contains admin and some  example username / password as passwords in .json file are already hashed.

As when there is no data - the only account injected via code is admin one.

That admin username is **ADM013** and password **admin** - It will ask to change password when you first time login.

In pre-populated data(example data .json files included in repo) password for ADM013 is already changed - but there is easy way to override it(even if not directly due to hashing and way of checking passwords).

For creating account admin type account is not required - but for other actions mentioned above it is.









