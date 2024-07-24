from datetime import datetime
import plotly.express as px
import pandas as pd 
import gspread
from google.oauth2.service_account import Credentials

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
PersonalDetails = sheet.worksheet("users")
Expenses = sheet.worksheet("expenses")
# Global variable for user_id
current_user_id = None


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
            print('[red]Invalid input. Please enter "y" for yes or "n" for no.[/]')


def register_user():
    """
    Register user with name and unique ID
    """
    print('Type "BACK" to return to previous page')
    while True:
        name = input('Enter your name: \n').capitalize()
        if name.upper() == 'BACK':
            greet_msg()
            continue        
        # Check if the name is aplhabetical
        elif not name.isalpha():
            print('Please make sure you use alpabetical characters (a-z) only.')
        else:
            print(f'Welcome {name}')
            break
    
    while True: 
        user_id = input('\nCreate a unique 4-digit ID (this cannot be retrieved if forgotten): \n')
        # Check if the user input was a 4 digit code and numeric
        if len(user_id) == 4 and user_id.isdigit():
            user_id = int(user_id)
            try:
                # Insert user into the database
                c.execute('INSERT INTO users (name, user_id) VALUES (?, ?)', (name, user_id))
                conn.commit()
                print(f'Valid ID entered. Welcome {name}.\n')
                current_user_id = user_id
                user_login()
                break
            except sqlite3.IntegrityError:  # Raises error if ID is in use
                print('This ID is already in use. Please choose another.')
            except Exception as e:
                print(f'An error occurred: {e}')
        elif user_id == 'BACK':
            greet_msg()
            continue
        else:
            print('Invalid ID. It must be 4 digits long.')

    
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
                current_user_id = user_input_id
                print(f'Welcome back, {name}')
                expense_menu()
                break
            else:
                print('No user found with the given ID.')
        else:
            print('Invalid ID. It must be 4 digits long')


def check_user_id(user_id):
    """
    Check if the user ID exists in the database.
    """
    c.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result is None:
        return False, None
    else:
        name = result[0] 
        return True, name


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
            user_login()
            break
        else:
            print('Invalid input. Please enter "1" to add an expense or "2" to get a report')


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
            print('Incorrect date format, should be DD-MM-YYYY')
    # Insert expenses into database
    c.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)', (current_user_id, amount, category, date))
    conn.commit()

    print(f'Expense of {amount} in category {category} added for {date}.')


def get_report():
    """
    Function to get a report on recent expenses that have been logged
    """



greet_msg()

conn.close()