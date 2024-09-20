# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DeliveryServices(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    long_name = models.CharField(max_length=100)
    home_base = models.ForeignKey('Locations', models.DO_NOTHING, db_column='home_base')
    manager = models.OneToOneField('Workers', models.DO_NOTHING, db_column='manager')

    class Meta:
        managed = False
        db_table = 'delivery_services'
        app_label = 'restaurant_supply_express'


class Drones(models.Model):
    id = models.OneToOneField(DeliveryServices, models.DO_NOTHING, db_column='id', primary_key=True)
    tag = models.IntegerField()
    fuel = models.IntegerField()
    capacity = models.IntegerField()
    sales = models.IntegerField()
    flown_by = models.ForeignKey('Pilots', models.DO_NOTHING, db_column='flown_by', blank=True, null=True)
    swarm = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    swarm_tag = models.ForeignKey('self', models.DO_NOTHING, db_column='swarm_tag', to_field='tag', blank=True,
                                  null=True)
    hover = models.ForeignKey('Locations', models.DO_NOTHING, db_column='hover')

    class Meta:
        managed = False
        db_table = 'drones'
        unique_together = (('id', 'tag'),)
        app_label = 'restaurant_supply_express'


class Employees(models.Model):
    username = models.OneToOneField('Users', models.DO_NOTHING, db_column='username', primary_key=True)
    taxid = models.CharField(db_column='taxID', unique=True, max_length=40)  # Field name made lowercase.
    hired = models.DateField()
    experience = models.IntegerField()
    salary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'employees'
        app_label = 'restaurant_supply_express'


class Ingredients(models.Model):
    barcode = models.CharField(primary_key=True, max_length=40)
    iname = models.CharField(max_length=100)
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ingredients'
        app_label = 'restaurant_supply_express'


class Locations(models.Model):
    label = models.CharField(primary_key=True, max_length=40)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    space = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'locations'
        app_label = 'restaurant_supply_express'


class Payload(models.Model):
    id = models.OneToOneField(Drones, models.DO_NOTHING, db_column='id', primary_key=True)
    tag = models.ForeignKey(Drones, models.DO_NOTHING, db_column='tag', to_field='tag')
    barcode = models.ForeignKey(Ingredients, models.DO_NOTHING, db_column='barcode')
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'payload'
        unique_together = (('id', 'tag', 'barcode'),)
        app_label = 'restaurant_supply_express'


class Pilots(models.Model):
    username = models.OneToOneField(Employees, models.DO_NOTHING, db_column='username', primary_key=True)
    licenseid = models.CharField(db_column='licenseID', unique=True, max_length=40)  # Field name made lowercase.
    experience = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pilots'
        app_label = 'restaurant_supply_express'


class RestaurantOwners(models.Model):
    username = models.OneToOneField('Users', models.DO_NOTHING, db_column='username', primary_key=True)

    class Meta:
        managed = False
        db_table = 'restaurant_owners'
        app_label = 'restaurant_supply_express'


class Restaurants(models.Model):
    long_name = models.CharField(primary_key=True, max_length=40)
    rating = models.IntegerField()
    spent = models.IntegerField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, db_column='location')
    funded_by = models.ForeignKey(RestaurantOwners, models.DO_NOTHING, db_column='funded_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurants'
        app_label = 'restaurant_supply_express'


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    birthdate = models.DateField()

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'restaurant_supply_express'


class WorkFor(models.Model):
    username = models.OneToOneField(Employees, models.DO_NOTHING, db_column='username', primary_key=True)
    id = models.ForeignKey(DeliveryServices, models.DO_NOTHING, db_column='id')

    class Meta:
        managed = False
        db_table = 'work_for'
        unique_together = (('username', 'id'),)
        app_label = 'restaurant_supply_express'


class Workers(models.Model):
    username = models.OneToOneField(Employees, models.DO_NOTHING, db_column='username', primary_key=True)

    class Meta:
        managed = False
        db_table = 'workers'
        app_label = 'restaurant_supply_express'


class display_restaurant_view(models.Model):
    long_name = models.CharField(primary_key=True, max_length=40)
    rating = models.IntegerField()
    spent = models.IntegerField()
    location = models.CharField(max_length=40)
    funded_by = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'display_restaurant_view'
        app_label = 'restaurant_supply_express'


class display_pilot_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    licenseID = models.CharField(db_column='licenseID', unique=True, max_length=40) 
    experience = models.IntegerField()
    num_drones = models.IntegerField()
    num_locations = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'display_pilot_view'
        app_label = 'restaurant_supply_express'


class display_location_view(models.Model):
    label = models.CharField(primary_key=True, max_length=40)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    no_of_restaurants = models.IntegerField()
    no_of_services = models.IntegerField()
    no_of_drones = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'display_location_view'
        app_label = 'restaurant_supply_express'


class display_service_view(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    long_name = models.CharField(max_length=100)
    home_base = models.CharField(max_length=40)
    manager = models.CharField(max_length=40)
    total_sales = models.IntegerField()
    num_ingredients = models.IntegerField()
    total_cost = models.IntegerField()
    total_weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'display_service_view'
        app_label = 'restaurant_supply_express'


class display_ingredient_view(models.Model):
    ingredient_name = models.CharField(primary_key=True, max_length=100)
    location = models.CharField(max_length=40)
    amount_available = models.IntegerField()
    low_price = models.IntegerField()
    high_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'display_ingredient_view'
        unique_together = (('ingredient_name', 'location'),)
        app_label = 'restaurant_supply_express'


class display_employee_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    taxid = models.CharField(db_column='taxID', unique=True, max_length=40)  # Field name made lowercase.
    salary = models.IntegerField()
    hired = models.DateField()
    employee_experience = models.IntegerField()
    licenseid = models.CharField(db_column='licenseID', unique=True, max_length=40)  # Field name made lowercase.
    piloting_experience = models.IntegerField()
    manager_status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'display_employee_view'
        app_label = 'restaurant_supply_express'


class available_as_manager_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'available_as_manager_view'
        app_label = 'restaurant_supply_express'


class valid_managers_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    id = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'valid_managers_view'
        app_label = 'restaurant_supply_express'

class deletable_services_view(models.Model):
    id = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'deletable_services_view'
        app_label = 'restaurant_supply_express'


class hireable_employees_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'hireable_employees_view'
        app_label = 'restaurant_supply_express'


class work_for_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    id = models.CharField(primary_key=True, max_length=40)
    is_manager = models.BooleanField()
    drones_flown_for = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'work_for_view'
        app_label = 'restaurant_supply_express'

class display_owner_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    num_restaurants = models.IntegerField()
    num_places = models.IntegerField()
    highs = models.IntegerField()
    lows = models.IntegerField()
    debt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'display_owner_view'
        app_label = 'restaurant_supply_express'

class display_employee_view(models.Model):
    username = models.CharField(primary_key=True, max_length=40)
    taxID = models.CharField(max_length=40)
    hired = models.DateField()
    employee_experience = models.IntegerField()
    licenseID = models.CharField(max_length=40)
    piloting_experience = models.IntegerField()
    manager_status = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'display_employee_view'
        app_label = 'restaurant_supply_express'