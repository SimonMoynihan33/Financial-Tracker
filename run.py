import sqlite3
from datetime import datetime
import plotly.express as px
import pandas as pd 

# Connect to SQL database
conn = sqlite3.connect('expense_tracker_db.expense_tracker_db.py')
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

def register_user():
    """
    Register user with name and unique ID
    """
    name = input('Enter you name: ')
    user_id = input('Create a 4-digit ID: ')

    if len(user_id) != 4 or not user_id.isdigit():
        print('Invalid ID. Your ID must be exactly 4 digits.')
        return
        
    try:
        c.execute('INSERT INTO users (name, user_id) VALUES (?, ?)', 
        (name, user_id))
        conn.commit()
        print('Registration successful!')
    except sqlite3.IntegrityError:
        print('This ID is already in use. Please choose another.')
    except Exception as e:
        print(f'An error occurred: {e}')
    
register_user()