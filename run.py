from datetime import datetime, timedelta
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
# Import colorama (Link)
# (https://sparkbyexamples.com/python/print-colored-text-to-the-terminal-in-python/#:~:text=ANSI%20Escape%20Sequences%20to%20Add%20Color%20to%20Terminal%20Output&text=The%20escape%20sequence%20for%20setting,followed%20by%20the%20letter%20m%20.)
from colorama import init, Fore, Style
from os import system, name
from time import sleep
# Import Rich (Link) (https://pypi.org/project/rich/)
from rich.console import Console
from rich.table import Table

# Google sheets credentials and setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("expense_tracker")

# Sheets for users and expenses
PersonalDetails = SHEET.worksheet("user-sheet")
Expenses = SHEET.worksheet("expenses-sheet")

# Global variable for user_id
current_user_id = None


# define our clear function CREDS
# (https://www.geeksforgeeks.org/clear-screen-python/)
def clear():
    """
    Clear function to clear screen
    """
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


def center_text(text, width):
    """
    Centers text for welcome message
    """
    lines = text.splitlines()
    centered_lines = [line.center(width) for line in lines]
    return "\n".join(centered_lines)


def logo():
    """
    Function to print logo for app
    """
    ascii_art = r"""
__        _______ _     ____ ___  __  __ _____ __
\ \      / / ____| |   / ___/ _ \|  \/  | ____| |
 \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _| | |
  \ V  V / | |___| |__| |__| |_| | |  | | |___|_|
   \_/\_/  |_____|_____\____\___/|_|  |_|_____(_)"""
    centered_ascii_art = center_text(ascii_art, 80)
    print(
        Fore.GREEN
        + "  ==============================================================" +
        "===============\n"
        + Style.RESET_ALL
        + " \n"
        + Fore.BLUE
        + centered_ascii_art
        + "\n"
        + Style.RESET_ALL
        + " \n"
        + Fore.GREEN
        + "  ==============================================================" +
        "===============\n"
        + Style.RESET_ALL
    )


def greet_msg():
    """
    Message to greet user and ask if they have an account.
    """
    clear()
    logo()
    while True:
        response = input("  Are you already registered? (y/n): \n"
                         "  ").strip().lower()
        if response == "y":
            print("\n  Proceeding to login...")
            sleep(1)
            user_login()
            break
        elif response == "n":
            print("\n  You must register to use this app\n")
            register_user()
            break
        else:
            print(
                Fore.RED
                + "  Invalid input. Please enter 'y' for yes or 'n' for no."
                + Style.RESET_ALL
            )


def register_user():
    """
    Register user with name and unique ID
    """
    global current_user_id
    print('  Type "BACK" to return to the main menu\n')
    while True:
        name = input("  Enter your name: \n" "  ").capitalize()
        if name.upper() == "BACK":
            clear()
            greet_msg()
            continue
        # Check if the name is aplhabetical
        elif not name.isalpha():
            print(
                Fore.RED
                + "  Please make sure you use alphabetical characters " +
                "(a-z) only."
                + Style.RESET_ALL
            )
        else:
            clear()
            print(Fore.GREEN + f"  Welcome {name}" + Style.RESET_ALL)
            break

    while True:
        print('  Type "BACK" to return to the main menu')
        user_id = input(
            "\n  Create a unique 4-digit ID (this cannot be retrieved if "
            "forgotten): \n"
            "  "
        )
        # Check if the user input was a 4 digit code and numeric
        if len(user_id) == 4 and user_id.isdigit():
            user_id = int(user_id)
            try:
                # Check if user is in database
                if not PersonalDetails.find(str(user_id), in_column=2):
                    PersonalDetails.append_row([name, user_id])
                    clear()
                    print(
                        Fore.GREEN
                        + f"  Valid ID entered. Welcome {name}.\n"
                        + Style.RESET_ALL
                    )
                    current_user_id = user_id
                    sleep(1.5)
                    user_login()
                    return
                else:
                    print(
                        Fore.RED
                        + "  This ID is already in use. Please choose another."
                        + Style.RESET_ALL
                    )
            except Exception as e:
                print(Fore.RED + f"  An error occurred: {e}" + Style.RESET_ALL)
        elif user_id.upper() == "BACK":
            greet_msg()
            continue
        else:
            print(
                Fore.RED + "  Invalid ID. It must be 4 digits long." +
                Style.RESET_ALL
            )


def user_login():
    """
    Accepts user login details and retrives data
    """
    global current_user_id
    print('\n  Type "BACK" to return to previous page\n')
    while True:
        user_input_id = input(
            "  Please enter your unique 4 digit code: \n"
            "  ").strip()
        if user_input_id.upper() == "BACK":
            clear()
            greet_msg()
            continue
        # Validate and process the user ID
        if len(user_input_id) == 4 and user_input_id.isdigit():
            user_input_id = int(user_input_id)
            # Check user ID and recieve both status and name
            valid, name = check_user_id(user_input_id)
            if valid:
                clear()
                current_user_id = user_input_id
                print(Fore.GREEN + f"  Welcome back, {name}" + Style.RESET_ALL)
                sleep(2)
                expense_menu()
                return
            else:
                print(Fore.RED + "  No user found with the given ID." +
                      Style.RESET_ALL)
        else:
            print(Fore.RED + "  Invalid ID. It must be 4 digits long" +
                  Style.RESET_ALL)


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
        print(Fore.RED + f"  An error occurred: {e}" + Style.RESET_ALL)
        return False, none


def expense_menu():
    """
    Asks user if they wish to log an expense or get a report on financial data
    """
    while True:
        print('\n  Press "0" if you wish to log out\n  ')
        response = input(
            '  Would you like to\n'
            '  (1) Add an expense\n'
            '  (2) Get a report on recent expenses\n'
            '  (3) List and delete expenses\n'
            '  '
        ).strip()
        if response == '1':
            add_expense()
            break
        elif response == '2':
            clear()
            get_report()
            break
        elif response == '3':
            clear()
            print('  Fetching data...')
            sleep(1.5)
            list_expenses()
            break
        elif response == '0':
            clear()
            sleep(1.5)
            greet_msg()
            break
        else:
            print(
                Fore.RED
                + '  Invalid input. Please enter "1", "2", "3" '
                ' or "0" to log out.'
                + Style.RESET_ALL
            )


def add_expense():
    """
    Function to add an expense
    """
    global current_user_id
    while True:
        amount = input("  Enter the expense amount: \n  ").strip()
        try:
            amount = float(amount)
            print(Fore.GREEN + f"  Amount of {amount}" + Style.RESET_ALL)
            break
        except ValueError:
            print(Fore.RED + "  Input must be a number" + Style.RESET_ALL)
    category_map = {
        "1": "Bills",
        "2": "Subscriptions",
        "3": "Fun",
        "4": "Food",
        "5": "Other",
    }
    while True:
        category = input(
            "  Enter the category of the expense: \n"
            "          (1) "
            + Fore.LIGHTYELLOW_EX
            + "Bills"
            + Style.RESET_ALL
            + "          (3) "
            + Fore.LIGHTBLUE_EX
            + "Fun\n"
            + Style.RESET_ALL
            + "          (2) "
            + Fore.LIGHTCYAN_EX
            + "Subscriptions"
            + Style.RESET_ALL
            + "  (4) "
            + Fore.LIGHTMAGENTA_EX
            + "Food\n"
            + Style.RESET_ALL
            + "          (5) "
            + Fore.LIGHTRED_EX
            + "Other\n"
            + Style.RESET_ALL
            + "  "
        )
        if category in category_map:
            break
        else:
            print(
                Fore.RED +
                '  Invalid category. Please try again'
                + Style.RESET_ALL
            )
    while True:
        date = input(
            "  Enter the date of expenses (DD-MM-YYYY) or " +
            "leave blank for "
            "today: \n"
            "  "
            )
        if not date:
            date = datetime.today().strftime("%d-%m-%Y")
            break
        try:
            entered_date = datetime.strptime(date, "%d-%m-%Y")
            today = datetime.today()
            one_year_future = today + timedelta(days=365)
            if entered_date.year > 2010 and entered_date <= one_year_future:
                break  # Exit loop if date valid and within year from today
            else:
                print(
                    Fore.RED +
                    "  Date must be after the year 2010 and within one year" +
                    " from "
                    + "today." + Style.RESET_ALL
                    )
        except ValueError:
            print(
                Fore.RED
                + "  Incorrect date format, should be DD-MM-YYYY"
                + Style.RESET_ALL
                )

    try:
        Expenses.append_row([current_user_id, amount, category_map[category],
                            date])
        sleep(1.5)
        print(
            Fore.GREEN
            + f"  Expense of {amount} in category " +
            f"{category_map[category]} added for {date}."
            + Style.RESET_ALL
        )
        expense_menu()
    except Exception as e:
        print(Fore.RED + f"  An error occurred: {e}" + Style.RESET_ALL)


def get_report():
    """
    Function to get a report on recent expenses that have been logged
    Function written by ChatGPT
    """
    global current_user_id
    console = Console()
    print("\n  Fetching data...\n")
    sleep(1.5)
    try:
        records = Expenses.get_all_records()
        rows = [row for row in records if str(row["user_id"])
                == str(current_user_id)]

        if not rows:
            print("  You have logged no expenses so far. Let's get started!")
            return expense_menu()

        df = pd.DataFrame(rows, columns=["user_id", "amount", "category",
                          "date"])
        df["amount"] = df["amount"].astype(float)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")

        # Extract month and year from the date
        df["month_year"] = df["date"].dt.to_period("M")
        # Group by month and category
        grouped = (
            df.groupby(["month_year", "category"]).agg({"amount": "sum"})
            .reset_index()
        )
        # Sort the grouped data
        grouped = grouped.sort_values(by=["month_year", "category"])

        table = Table(title="Recent Expenses (Grouped by Month and Category)")
        table.add_column("Month-Year", justify="right", style="cyan",
                         no_wrap=True)
        table.add_column("Category", style="magenta")
        table.add_column("Amount", justify="right", style="green")

        for _, row in grouped.iterrows():
            table.add_row(str(row["month_year"]), row["category"],
                          f'{row["amount"]:.2f}')

        console.print(table)
        return expense_menu()
    except Exception as e:
        print(f"  An error occurred: {e}")


def display_expenses():
    """
    Helper function to list all expenses for the current user
    Written by ChatGPT
    """
    global current_user_id
    console = Console()
    try:
        records = Expenses.get_all_records()
        rows = [row for row in records if str(row['user_id']) ==
                str(current_user_id)]

        if not rows:
            print("  No expenses found")
            return expense_menu()

        df = pd.DataFrame(rows, columns=['user_id', 'amount', 'category',
                                         'date'])
        df['amount'] = df['amount'].astype(float)
        df['date'] = pd.to_datetime(df['date'],
                                    format='%d-%m-%Y').dt.strftime('%d-%m-%Y')

        # Adjust index to start from 1 instead of 0
        df.index += 1

        table = Table(title="Your Expenses:")

        table.add_column("Index", justify="right", style="cyan", no_wrap=True)
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Category", style="magenta")
        table.add_column("Date", justify="right", style="cyan")

        for index, row in df.iterrows():
            table.add_row(str(index), f'{row["amount"]:.2f}',
                          row["category"], row["date"])

        console.print(table)
        return df
    except Exception as e:
        print(f'  An error occurred: {e}')
        return None


def delete_expense():
    """
    Function to delete a specific expense by its index
    """
    global current_user_id
    df = display_expenses()
    if df is None or df.empty:
        print('  You have nothing to delete!')
        print('  Returning...')
        sleep(1)
        return expense_menu()

    while True:
        try:
            index = int(
                input(
                    "\n  Enter the index of the expense to delete: "
                ).strip())
            if index in df.index:
                row_to_delete = df.loc[index]
                cell = Expenses.find(str(row_to_delete['date']))
                if cell:
                    Expenses.delete_rows(cell.row)
                    print(
                        Fore.GREEN
                        + f'  Expense on {row_to_delete["date"]} deleted '
                        + 'successfully'
                        + Style.RESET_ALL
                    )
                    return list_expenses()
            else:
                print(Fore.RED + '  Invalid index. Please try again.'
                      + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + '  Invalid input. Please enter a valid index.'
                  + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f'  An error occurred: {e}' + Style.RESET_ALL)


def list_expenses():
    """
    Function to list all expenses for the current user and return to expense
    menu
    """
    df = display_expenses()
    if df is None or df.empty:
        print('  No expenses found or an error occurred!')
        sleep(1)
        expense_menu()
        return

    while True:
        go_back = input('\n  Type "1" to return to main menu or "2" to'
                        + ' delete an expense\n  ').strip()
        if go_back == '1':
            print('  Returning...')
            sleep(0.5)
            expense_menu()
            break
        elif go_back == '2':
            print('  Redirecting...')
            sleep(0.5)
            delete_expense()
            break
        else:
            print(Fore.RED + 'Invalid input. Please enter "1" or "2".'
                  + Style.RESET_ALL)


clear()
greet_msg()
