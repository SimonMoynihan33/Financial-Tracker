from datetime import datetime
import pandas as pd 
import gspread
from google.oauth2.service_account import Credentials
# Import colorama CREDS (https://sparkbyexamples.com/python/print-colored-text-to-the-terminal-in-python/#:~:text=ANSI%20Escape%20Sequences%20to%20Add%20Color%20to%20Terminal%20Output&text=The%20escape%20sequence%20for%20setting,followed%20by%20the%20letter%20m%20.)
from colorama import init, Fore, Style
# Import only system from os
from os import system, name
from time import sleep
 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('expense_tracker')

# Sheets for users and expenses
PersonalDetails = SHEET.worksheet("user-sheet")
Expenses = SHEET.worksheet("expenses-sheet")
# Global variable for user_id
current_user_id = None

init()


# define our clear function CREDS (https://www.geeksforgeeks.org/clear-screen-python/)
def clear():
    """
    Clear function to clear screen
    """
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        

def logo():
    """
    Function to print logo for app
    """
    print( Fore.GREEN + '=============================================================================\n' + Style.RESET_ALL +
    ' \n' +
    Fore.BLUE + '                  Welcome to your personal expenses tracker!\n                  ' + Style.RESET_ALL + 
    ' \n' +
    Fore.GREEN + '=============================================================================\n' + Style.RESET_ALL)


def greet_msg():
    """
    Message to greet user and ask if they have an account.
    """
    while True:
        response = input('Are you already registered? (y/n): \n').strip().lower()
        if response == 'y':
            print('\nProceeding to login...')
            user_login()
            break
        elif response == 'n':
            print('\nYou must register to use this app')
            register_user() 
            break
        else:
            print(Fore.RED + "Invalid input. Please enter 'y' for yes or 'n' for no." + Style.RESET_ALL)


def register_user():
    """
    Register user with name and unique ID
    """
    global current_user_id
    print('Type "BACK" to return to the main menu')
    while True:
        name = input('Enter your name: \n').capitalize()
        if name.upper() == 'BACK':
            clear()
            greet_msg()
            continue        
        # Check if the name is aplhabetical
        elif not name.isalpha():
            print(Fore.RED + 'Please make sure you use alpabetical characters (a-z) only.' +  Style.RESET_ALL)
        else:
            clear()
            print(Fore.GREEN + f'Welcome {name}' + Style.RESET_ALL)
            break
    
    while True: 
        user_id = input('\nCreate a unique 4-digit ID (this cannot be retrieved if forgotten): \n')
        # Check if the user input was a 4 digit code and numeric
        if len(user_id) == 4 and user_id.isdigit():
            user_id = int(user_id)
            try:
                # Check if user is in database
                if not PersonalDetails.find(str(user_id), in_column=2):
                    PersonalDetails.append_row([name, user_id])
                    clear()
                    print(Fore.GREEN + f'Valid ID entered. Welcome {name}.\n' + Style.RESET_ALL)
                    current_user_id = user_id
                    sleep(1.5)
                    user_login()
                    return
                else:
                    print(Fore.RED + 'This ID is already in use. Please choose another.' + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f'An error occurred: {e}' + Style.RESET_ALL)
        elif user_id.upper() == 'BACK':
            greet_msg()
            continue
        else:
            print(Fore.RED + 'Invalid ID. It must be 4 digits long.' + Style.RESET_ALL)

    
def user_login():
    """
    Accepts user login details and retrives data
    """
    global current_user_id
    print('\nType "BACK" to return to previous page\n')
    while True:
        user_input_id = input('Please enter your unique 4 digit code: \n').strip()
        if user_input_id.upper() == 'BACK':
            clear()
            greet_msg()
            continue
        # Validate and process the user ID
        if len(user_input_id) == 4 and user_input_id.isdigit():
            user_input_id = int(user_input_id)
            valid, name = check_user_id(user_input_id) # Check user ID and recieve both status and name
            if valid:
                clear()
                current_user_id = user_input_id
                print(Fore.GREEN + f'Welcome back, {name}' + Style.RESET_ALL)
                sleep(2)
                expense_menu()
                return
            else:
                print(Fore.RED + 'No user found with the given ID.' + Style.RESET_ALL)
        else:
            print(Fore.RED + 'Invalid ID. It must be 4 digits long' + Style.RESET_ALL)


def check_user_id(user_id):
    """
    Check if the user ID exists in the database.
    """
    try:
        cell = PersonalDetails.find(str(user_id), in_column=2)
        if cell:
            row = PersonalDetails.row_values(cell.row)
            return True, row[0]
        else:
            return False, None
    except Exception as e:
        print(Fore.RED + f'An error occurred: {e}' + Style.RESET_ALL)
        return False, none



def expense_menu():
    """
    Asks user if they wish to log an expense or get a report on financial data
    """
    while True:
        print('\nPress "0" if you wish to log out\n')
        response = input('Would you like to\n'
         '(1) add an expense\n'
         '(2) get a report on recent expenses\n')
        if response == '1':
            add_expense()
            break
        elif response == '2':
            get_report()
            break
        elif response == '0':
            clear()
            sleep(1.5)
            user_login()
            break
        else:
            print(Fore.RED + 'Invalid input. Please enter "1" to add an expense or "2" to get a report' + Style.RESET_ALL)


def add_expense():
    """
    Function to add an expense
    """
    global current_user_id
    while True:
        amount = input('Enter the expense amount: \n').strip()
        try:
            float(amount)
            print(Fore.GREEN + f'Amount of {amount}' + Style.RESET_ALL)
            break
        except ValueError:
            print(Fore.RED + 'Input must be a number' + Style.RESET_ALL)   

    category = input('Enter the category of the expense: \n'
               '          (1) ' + Fore.LIGHTYELLOW_EX + 'Bills' + Style.RESET_ALL + '          (3) ' + Fore.LIGHTBLUE_EX + 'Fun\n' + Style.RESET_ALL + 
               '          (2) ' + Fore.LIGHTCYAN_EX + 'Subscriptions' + Style.RESET_ALL + '  (4) ' + Fore.LIGHTMAGENTA_EX + 'Food\n' + Style.RESET_ALL +
               '          (5) ' + Fore.LIGHTRED_EX + 'Other\n' + Style.RESET_ALL)
    category_map = {
        '1': 'Bills',
        '2': 'Subscriptions',
        '3': 'Fun',
        '4': 'Food',
        '5': 'Other'
        }
    if category not in category_map:
            print(Fore.RED + 'Invalid category. Please try again.' + Style.RESET_ALL)
            return add_expense()
    date = input('Enter the date of expenses (DD-MM-YYYY) or leave blank for today: \n')
    if not date:
        date = datetime.today().strftime('%d-%m-%Y')
    else:
        # Validate date format
        try:
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            print(Fore.RED + 'Incorrect date format, should be DD-MM-YYYY' + Style.RESET_ALL)
            return add_expense()
    try:
        Expenses.append_row([current_user_id, amount, category_map[category], date])
        sleep(1.5)
        print(Fore.GREEN + f'Expense of {amount} in category {category_map[category]} added for {date}.' + Style.RESET_ALL)
        expense_menu()
    except Exception as e:
        print(Fore.RED + f'An error occurred: {e}' + Style.RESET_ALL)


def get_report():
    """
    Function to get a report on recent expenses that have been logged
    Function written by ChatGPT
    """
    global current_user_id
    try:
        records = Expenses.get_all_records()
        rows = [row for row in records if str(row['user_id']) == str(current_user_id)]

        df = pd.DataFrame(rows, columns=['user_id', 'amount', 'category', 'date'])
        df['amount'] = df['amount'].astype(float)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')

        print("\nRecent Expenses:")
        print(df.to_string(index=False))

        return expense_menu()
    except Exception as e:
        print(f'An error occurred: {e}')


logo()
greet_msg()