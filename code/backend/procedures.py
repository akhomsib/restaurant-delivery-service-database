from django.db import connection


def add_location(label, x_coord, y_coord, space):
    return execute('add_location', label, x_coord, y_coord, space)


def remove_location(label):
    return execute('remove_location', label)


def add_owner(username, first_name, last_name, address, bdate):
    return execute('add_owner', username, first_name, last_name, address, bdate)


def remove_owner(username):
    return execute('remove_owner', username)


def start_funding(username, long_name):
    return execute('start_funding', username, long_name)


def add_employee(username, first_name, last_name, address, bdate, taxID, hired, experience, salary):
    return execute('add_employee', username, first_name, last_name, address, bdate, taxID, hired, experience, salary)


def fire_employee(username, id):
    return execute('fire_employee', username, id)


def add_pilot_role(username, licenseID, experience):
    return execute('add_pilot_role', username, licenseID, experience)


def add_service(service_id, long_name, home_base, manager):
    return execute('add_service', service_id, long_name, home_base, manager)


def manage_service(username, service_id):
    return execute('manage_service', username, service_id)


def remove_service(service_id):
    return execute('remove_service', service_id)


def hire_employee(username, service_id):
    return execute('hire_employee', username, service_id)


def fire_employee(username, service_id):
    return execute('fire_employee', username, service_id)


def remove_drone(id, tag):
    return execute('remove_drone', id, tag)


def refuel_drone(id, tag, fuel):
    return execute('refuel_drone', id, tag, fuel)


def leave_swarm(id, tag):
    return execute('leave_swarm', id, tag)


def join_swarm(id, tag, leader_tag):
    return execute('join_swarm', id, tag, leader_tag)


def takeover_drone(id, tag, username):
    return execute('takeover_drone', username, id, tag)


def add_drone(id, tag, fuel, capacity, sales, pilot):
    return execute('add_drone', id, tag, fuel, capacity, sales, pilot)


def fly_drone(id, tag, destination):
    return execute('fly_drone', id, tag, destination)


def load_drone(id, tag, barcode, quantity, price):
    return execute('load_drone', id, tag, barcode, quantity, price)


def add_restaurant(long_name, rating, spent, location):
    return execute('add_restaurant', long_name, rating, spent, location)


def purchase_ingredient(long_name, id, tag, barcode, quantity):
    return execute('purchase_ingredient', long_name, id, tag, barcode, quantity)


def add_worker_role(username):
    return execute('add_worker_role', username)

def remove_pilot_role(username):
    return execute('remove_pilot_role', username)
def remove_ingredient(barcode):
    return execute('remove_ingredient', barcode)

def add_ingredient(barcode, name, weight):
    return execute('add_ingredient', barcode, name, weight)


def execute(procedure, *args):
    cursor = connection.cursor()
    query = f'CALL {procedure} ('
    for arg in args:
        query += f"'{arg}',"
    query = query[:-1] + ');'
    try:
        cursor.execute(query)
    finally:
        row = cursor.fetchone()
        cursor.close()
        return row
