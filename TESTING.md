## Contents
- [Validation](#validation)
- [User goals and stories](#user-goals)
- [Manual Testing](#manual-testing)
  - [Login](#login)
  - [Registration](#register)
  - [Expense Menu](#expense_menu)
  - [Add Expense](#add-expense)
  - [Show Report](#show-report)
  - [List and Delete](#list-delete)
- [Bugs](#bugs)
  - [Fixed Bugs](#fixed-bugs)
  - [Unfixed Bugs](unfixed-Bugs)

**Goal**|**How is this Achieved?**
:-----:|:-----:
A simple program that users will want to use|The program is intuitive and guides the user through each step of using it. It is a simple program and the colours used, for the fonts, provide interest to the user
An program that meets the user’s needs|The program allows the user to input transactions, to be able to analyse their spending and to view their transactions
The user to feel their security is taken seriously|When an existing user enters their password the text is shown as asterisks so it is hidden from anyone that could be watching. The passwords are stored, in Google Sheets, as encrypted to prevent hacking. The error message, for the username and password not matching, doesn't say whether it's the username or password that has been entered wrong. This is another level of security to stop another user working out these details from which is wrong


## Bugs 
### Fixed Bugs
### Bug 01
- **Issue** - `UnboundLocalError: cannot access local variable 'user_id' where it is not associated with a value` thrown when trying to log in with saved id.
- **Cause** - `register_user()` and `user_login()` were given different data types (string and integer).
- **Fix** - Change both user_id inputs to integers.

### Bug 02 
- **Issue** - `TypeError: object of type 'int' has no len()` when trying to input a name and id after changes made.
- **Cause** - This was due to me using `len()` for integers which python does not allow.
- **Fix** - Check the length of the id input before converting to an int().

### Bug 03 
- **Issue** - `NameError: name 'user_id' is not defined` relating to the `check_user_id(user_id)` function. 
- **Cause** - This was due to user_id not being declared in the current scope.
- **Fix** - `c.excute` line had 'id' instead of 'user_id'. Correctly define it also in user_login.

### Bug 04 
- **Issue** - When an invalid input is used in the registration screen, it continues on to the log in code instead of going back to the create a code. 
- **Fix** - Create two while loops to check validate that the name inputted is alphabetical characters only and that it loops back around if not. Same was done for digit input to loop until correct.

### Bug 05
- **Issue** - When a date is put in for an expense, it brings you back to the 'Create a unique 4-digit ID' prompt. This only happens for a new user who directly goes to add an expense.
- **Cause** - I did not find the cause for this issue but I was able to find a work around.
- **Fix** - After registration, bring the user back to login prompt to log in, this now allows them to add expenses. 

### Bug 06
- **Issue** - Heroku does not support SQLite3 database.
- **Fix** - Change database to Google Sheets.

### Bug 07 
- **Issue** - Cannot validate the expense amount. `AttributeError: 'float' object has no attribute 'isdigit'` error being thrown in the console after an amount is entered.
- **Cause** - After a Google search I found `.isdigit()` cannot be used with `float()` due to it having decimal points.
- **Fix** - Add while loop and try statemet to convert the amount to a float after it is entered, given that it is a number and can be converted.

### Bug 08
- **Issue** - ```print(
            Fore.GREEN
            + f'  Expense on {row_to_delete["date"]} deleted successfully'
            + Style.RESET_ALL)``` In delete_expense function throwing error.
- **Cause** - Indentation was incorrect.

### Bug 09 
- **Issue** - Cannot get delete_expense function to show
- **Cause** - This was due to calling the list_expense function within delete function. This meant that the code would execute this function before finishing the delete expense function.
- **Fix** - Create a new function to call the original list_expense function (name now changed to display_expenses()). Use delete function and new list function to call this seperately.