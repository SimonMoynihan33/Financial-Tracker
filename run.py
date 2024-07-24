from datetime import datetime
import plotly.express as px
import pandas as pd 
import gspread
from google.oauth2.service_account import Credentials
# Import colorama (https://sparkbyexamples.com/python/print-colored-text-to-the-terminal-in-python/#:~:text=ANSI%20Escape%20Sequences%20to%20Add%20Color%20to%20Terminal%20Output&text=The%20escape%20sequence%20for%20setting,followed%20by%20the%20letter%20m%20.)
from colorama import init, Fore, Style

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

def clear():
    """
    Clear function to clear screen
    """
    print("\n" * 100)

def print_logo():
    """
    Function to print logo for app
    """
    print("Expense Tracker Logo")  # Placeholder for logo function


def greet_msg():
    """
    Message to greet user and ask if they have an account.
    """
    print('Hello World!')
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
        clear()
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
            user_login()
            break
        else:
            print(Fore.RED + 'Invalid input. Please enter "1" to add an expense or "2" to get a report' + Style.RESET_ALL)


def add_expense():
    """
    Function to add an expense
    """
    global current_user_id
    amount = float(input('Enter the expense amount: \n'))
    category = input('Enter the category of the expense: \n').capitalize()
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
        Expenses.append_row([current_user_id, amount, category, date])
    except Exception as e:
        print(Fore.RED + f'An error occurred: {e}' + Style.RESET_ALL)

    print(Fore.GREEN + f'Expense of {amount} in category {category} added for {date}.' + Style.RESET_ALL)


def get_report():
    """
    Function to get a report on recent expenses that have been logged
    """



greet_msg()