# Restaurant Supply Delivery Service: Relational Database Development
--------------------------------------------------------------------------------

A virtual environment is used to run all the code and corresponding visualization.
Please follow the intructions below to setup and run the online system.

## Useful Links
* [MySql (Database)](https://www.mysql.com/)
* [Django (Backend)](https://www.djangoproject.com/)
* [Bootstrap (Frontend)](https://getbootstrap.com/)

## How to Set Up & Run (Windows)
1. Clone this repository to access required materials
2. Run \4400_Phase4\phase4\sql\init_database.sql script in MySql
3. Create Python Virtual Environment
   pip -m venv env
4. Activate the environment with the provided requirements from requirements.txt file
   pip install -r requirements.txt
5. Update the password in \4400_Phase4\phase4\phase4\secure.py to match MySql database password **NEVER PUSH THIS CHANGE TO THE GIT**
6. Navigate to \4400_Phase4\phase4 directory in your environment
7. Run python server in aforementioned directory to serve necessary files
   python manage.py runserver
8. Go to http://127.0.0.1:8000/restaurant_supply_express/home/ to interact with the online system

## Technologies Used
A MySql database is connected to a Django backend that allowed for database operations to be made. 
To keep the user interface consistent, Bootstrap was used for the frontend design.
