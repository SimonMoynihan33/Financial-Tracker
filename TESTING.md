## Contents
- [User goals and experience](#user-goals)
- [Manual Testing](#manual-testing)
  - [Login](#login)
  - [Registration](#register)
  - [Expense Menu](#expense_menu)
- [Bugs](#bugs)
  - [Fixed Bugs](#fixed-bugs)
  - [Unfixed Bugs](unfixed-Bugs)

**Goal**|**Achieved?**|**How is this Achieved?**
:-----:|:-----:|:-----:
A friendly and accommodating interface|Yes|The program is intuitive and guides the user through each step of using it. It is a simple program and the colors used add character and life to the app
A unique identifier so I can log in and out of the application at my own will|Yes|This is added through the program's unique 4-digit ID that you must create
Be redirected back to the prompt, each time I enter a wrong input|Yes|Achieved through while loops
Be clearly shown when an input is correct or incorrect using colors on validation|Yes|Achieved with green and red colors for correct and incorrect validation respectively
Be able to log my expenses by amount, date and category|Yes|Achieved with the add_expense function
Show my expenses by month and category, and the aggregate of my expenditure for each category within the month in a table|Yes|Achieved with the get_report function using the rich library for table display
Be able to return back a step if I input the wrong decision|Yes|Achieved with proper error handling and while loops to guide the user back to the previous step
Be able to delete an expense I have logged|Yes|Achieved with the delete_expense function, allowing the user to remove specific logged expenses
Be able to see all expenses in a table|Yes|Achieved with the list_expenses function using the rich library for table display

### Manual Testing

The following section outlines the manual testing process for the expense tracker application. Each key functionality will be tested to ensure it performs as expected. Screenshots or images should be added to provide visual confirmation of each step.

#### 1. Application Start and User Registration/Login

**Test Steps:**
1. Run the application.
2. Verify the welcome message and logo are displayed correctly.

**Expected Result:**
- The welcome message and logo should be centered and displayed with the appropriate colors.

**Image Here:**
![Welcome message](docs/readme-images/home-screen.webp)

#### Register
**Test Steps:**
1. Enter 'n' to register a new user.
2. Follow the prompts to enter your name and create a unique 4-digit ID.
3. Verify the registration success message is displayed.

**Expected Result:**
- User should be able to register with a valid name and unique 4-digit ID.
- Registration success message should be displayed.

**Achieved?** 
- Yes

#### Login
**Test Steps:**
1. After registration, proceed to log in.
2. Enter the unique 4-digit ID to log in.
3. Verify the login success message is displayed.

**Expected Result:**
- User should be able to log in with the correct ID.
- Login success message should be displayed.

**Achieved?** 
- Yes

#### 2. Expense Menu

**Test Steps:**
1. After logging in, choose the option to add an expense.
2. Enter a valid amount, category, and date (within one year from today and after 2010).
3. Verify the expense is logged successfully.

**Expected Result:**
- The expense should be logged with the correct details.
- Success message should be displayed.

**Achieved?** 
- Yes

**Test Errors:**
1. Enter an invalid amount (e.g., a string instead of a number).
2. Enter an invalid date format or a date outside the allowed range.
3. Enter a date in the future beyond one year from today.

**Expected Result:**
- Appropriate error messages should be displayed for invalid inputs.
- User should be prompted to re-enter the information.

**Achieved?** 
- Yes

#### 3. Viewing Expenses by Month and Category

**Test Steps:**
1. After logging in, choose the option to get a report on recent expenses.
2. Verify the report displays expenses by month and category, along with the aggregate of expenditure for each category within the month.

**Expected Result:**
- The report should display expenses grouped by month and category.
- The aggregate expenditure for each category within the month should be shown.

**Achieved?** 
- Yes

#### 4. Viewing All Expenses

**Test Steps:**
1. After logging in, choose the option to list all expenses.
2. Verify all expenses are displayed in a table format.

**Expected Result:**
- All expenses should be listed in a table with the correct details.

**Achieved?** 
- Yes

#### 5. Deleting an Expense

**Test Steps:**
1. After logging in, choose the option to delete an expense.
2. Enter the index of the expense to delete.
3. Verify the expense is deleted successfully.

**Expected Result:**
- The specified expense should be deleted.
- Success message should be displayed.

**Achieved?** 
- Yes

**Test Errors:**
1. Enter an invalid index for deletion.
2. Try to delete an expense when there are none logged.

**Expected Result:**
- Appropriate error messages should be displayed for invalid inputs.
- User should be prompted to re-enter the information.

**Achieved?** 
- Yes

#### 6. Navigating the Application

**Test Steps:**
1. At any prompt, enter an invalid option (e.g., a letter instead of a number).
2. Verify the user is redirected back to the prompt with an error message.

**Expected Result:**
- An error message should be displayed for invalid inputs.
- User should be redirected back to the prompt to make a valid selection.

**Achieved?** 
- Yes

**Test Steps:**
1. At any prompt, enter '0' to log out.
2. Verify the user is logged out and returned to the main menu.

**Expected Result:**
- User should be logged out and returned to the main menu.

**Achieved?** 
- Yes

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

## Unfixed Bugs

Currently there are no unfixed bugs found.