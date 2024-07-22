import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd 

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
    name = input('Enter your name: ')
    user_id = input('Create a unique 4-digit ID: ')

    # Check if the name is aplhabetical
    if not name.isalpha():
        print('Please make sure you use alpabetical characters (a-z) only.')
        return
    
    # Check if the user input was a 4 digit code and numeric
    if not len(user_id) == 4 and user_id.isdigit():
        print('Invalid ID. Your ID must be exactly 4 digits.')
        return
        
    try:
        # insert user into the database
        c.execute('INSERT INTO users (name, user_id) VALUES (?, ?)', 
        (name, user_id))
        conn.commit()
        print('Registration successful!')
    except sqlite3.IntegrityError:
        print('This ID is already in use. Please choose another.')
    except Exception as e:
        print(f'An error occurred: {e}')
    
greet_msg()

conn.close()