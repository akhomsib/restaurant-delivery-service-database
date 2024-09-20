# Restaurant Supply Delivery Service 
## Relational Database Development
--------------------------------------------------------------------------------

A virtual environment is used to run all the code and corresponding online system. <br />
Please follow the intructions below to setup and run the online system.

## Useful Links
* [MySql (Database)](https://www.mysql.com/)
* [Django (Backend)](https://www.djangoproject.com/)
* [Bootstrap (Frontend)](https://getbootstrap.com/)

## How to Set Up & Run
1. Navigate to the code/database/ directory. Run the `init_database.sql` script in MySQL.
2. Navigate to the code/ directory in the terminal. Create Python Virtual Environment <br />
   pip -m venv env
3. Activate the environment with the provided requirements from the `requirements.txt` file based on os. <br />
   pip install -r requirements.txt
4. Update the password in the `secure.py` file to match your MySQL database password. This file is located in the code/setup/ directory. *NEVER PUSH THIS CHANGE TO THE GIT*
5. Run a python server to serve necessary files using the `manage.py` file and the following command. <br />
   python manage.py runserver
6. Go to http://127.0.0.1:8000/restaurant_supply_express/home/ to interact with the online system

## Technologies Used
A MySql database is connected to a Django backend that allowed for database operations to be made. 
To keep the user interface consistent, Bootstrap was used for the frontend design.
