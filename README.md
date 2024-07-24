# Expense Tracker

[Deployed Project](https://financial-expense-tracker-602c9c911447.herokuapp.com/)

**Table of Contents**
- [Creation Structure](#creation-structure)
- [User Experience](#user-experience)
- [Goals](#goals)
- [Features](#features)
  - [Validation Errors](#validation-errors)
- [Design](#design)
- [Future Deployment](future_deployment)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Credits](#credits)

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!

## Bugs 
### Bug 01
Issue - `UnboundLocalError: cannot access local variable 'user_id' where it is not associated with a value` thrown when trying to log in with saved id.
Cause - `register_user()` and `user_login()` were given different data types (string and integer).
Fix - Change both user_id inputs to integers.

### Bug 02 
Issue - `TypeError: object of type 'int' has no len()` when trying to input a name and id after changes made.
Cause - This was due to me using `len()` for integers which python does not allow.
Fix - Check the length of the id input before converting to an int().

### Bug 03 
Issue - `NameError: name 'user_id' is not defined` relating to the `check_user_id(user_id)` function. 
Cause - This was due to user_id not being declared in the current scope.
Fix - `c.excute` line had 'id' instead of 'user_id'. Correctly define it also in user_login.

### Bug 04 
Issue - When an invalid input is used in the registration screen, it continues on to the log in code instead of going back to the create a code.
Cause - 
Fix - Create two while loops to check validate that the name inputted is alphabetical characters only and that it loops back around if not. Same was done for digit input to loop until correct.

### Bug 05
Issue - When a date is put in for an expense, it brings you back to the 'Create a unique 4-digit ID' prompt. This only happens for a new user who directly goes to add an expense.
Cause - I did not find the cause for this issue but I was able to find a work around
Fix - After registration, bring the user back to login prompt to log in, this now allows them to add expenses. 

### Bug 06
Issue - Heroku does not support SQLite3 database
Fix - Change database to Google Sheets

### Bug 07 
Issue - Cannot validate the expense amount. `AttributeError: 'float' object has no attribute 'isdigit'` error being thrown in the console after an amount is entered.
Cause - After a Google search I found `.isdigit()` cannot be used with `float()` due to it having decimal points.
Fix - 
