import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd 

# Global variable for user_id
current_user_id = None

# Connect to SQL database
conn = sqlite3.connect('expense_tracker.db')
c = conn.cursor()

# Create table if it does not exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL UNIQUE
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

conn.commit()



def greet_msg():
    """
    Message to greet user and ask if they have an account.
    """
    print('Hello World!')
    while True:
        response = input('Are you already registered? (y/n): ').strip().lower()
        if response == 'y':
            print('Proceeding to login...')
            user_login()
            break
        elif response == 'n':
            print('You must register to use this app')
            register_user() # Call registration function
            break
        else:
            print('Invalid input. Please enter "y" for yes or "n" for no.')


def register_user():
    """
    Register user with name and unique ID
    """
    print('Type "BACK" to return to previous page')
    while True:
        name = input('Enter your name: ').capitalize()
        if name.upper() == 'BACK':
            greet_msg() # Return to start function
            continue        
        # Check if the name is aplhabetical
        elif not name.isalpha():
            print('Please make sure you use alpabetical characters (a-z) only.')
        else:
            print(f'Welcome {name}')
            break
    
    while True: 
        user_id = input('Create a unique 4-digit ID (this cannot be retrieved if forgotten): ')
        # Check if the user input was a 4 digit code and numeric
        if len(user_id) == 4 and user_id.isdigit():
            user_id = int(user_id)
            try:
                # Insert user into the database
                c.execute('INSERT INTO users (name, user_id) VALUES (?, ?)', (name, user_id))
                conn.commit()
                print(f'Valid ID entered. Welcome {name}.\n'
                'Registration successful!')
                current_user_id = user_id
                expense_menu()
                break
            except sqlite3.IntegrityError:  # Raises error if ID is in use
                print('This ID is already in use. Please choose another.')
            except Exception as e:
                print(f'An error occurred: {e}')
        elif user_id == 'BACK':
            greet_msg() # Return to start function
            continue
        else:
            print('Invalid ID. It must be 4 digits long.')

    
def user_login():
    """
    Accepts user login details and retrives data
    """
    global current_user_id
    print('Type "BACK" to return to previous page')
    while True:
        user_input_id = input('Please enter your unique 4 digit code: ').strip()
        if user_input_id.upper() == 'BACK':
            greet_msg() # Return to start function
            continue

        # Validate and process the user ID
        if len(user_input_id) == 4 and user_input_id.isdigit():
            user_input_id = int(user_input_id) # Convert to integer
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
        return False, None # Return false and none for id and name 
    else:
        name = result[0] # Extract name from query result
        return True, name


def expense_menu():
    """
    Asks user if they wish to log an expense or get a report on financial data
    """
    while True:
        response = input('Would you like to (1) add an expense, or (2) get a report on recent expenses. Press 1 or 2: ')
        if response == '1':
            add_expense()
            break
        elif response == '2':
            get_report()
            break
        else:
            print('Invalid input. Please enter "1" to add an expense or "2" to get a report')


def add_expense():
    """
    Function to add an expense
    """
    global current_user_id
    amount = float(input('Enter the expense amount: '))
    category = input('Enter the category of the expense: ').capitalize()
    date = input('Enter the date of expenses (DD-MM-YYYY) or leave blank for today: ')
    if not date:
        date = datetime.today().strftime('%d-%m-%Y')
    else:
        # Validate date format
        try:
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            print('Incorrect date format, should be DD-MM-YYYY')
            return add_expense()

    # Insert expenses into database
    c.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)', (current_user_id, amount, category, date))
    conn.commit()

    print(f'Expense of {amount} in category {category} on {date} added.')


def get_report():
    """
    Function to get a report on recent expenses that have been logged
    """



greet_msg()

conn.close()