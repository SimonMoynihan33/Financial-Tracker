![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

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
