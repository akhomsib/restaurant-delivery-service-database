from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

from django.forms import ModelChoiceField

from .models import *


class DisplayChoiceField(ModelChoiceField):
    def __init__(self, queryset, key, **kwargs):
        super().__init__(queryset, to_field_name=key, **kwargs)
        self.key = key

    def label_from_instance(self, obj):
        return getattr(obj, self.key)

    def clean(self, value):
        return value


class AddLocationForm(forms.Form):
    label = forms.CharField(label='Label', max_length=40)
    x_coord = forms.IntegerField(label='X Coordinate')
    y_coord = forms.IntegerField(label='Y Coordinate')
    space = forms.IntegerField(label='Drone Space',
                               validators=[
                                   MinValueValidator(limit_value=0, message='Drone space cannot be negative.')
                               ])

    def clean(self):
        clean_label = self.data['label']
        clean_x_coord = int(self.data['x_coord'])
        clean_y_coord = int(self.data['y_coord'])
        for location in display_location_view.objects.values():
            if location['label'] == clean_label:
                self.add_error('label', ValidationError('Label must be unique.'))
            if location['x_coord'] == clean_x_coord and location['y_coord'] == clean_y_coord:
                self.add_error('x_coord', ValidationError('Location coordinates must be unique.'))
                self.add_error('y_coord', ValidationError('Location coordinates must be unique.'))
        return super().clean()


class AddServiceForm(forms.Form):
    id = forms.CharField(label='ID', max_length=40)
    long_name = forms.CharField(label='Long Name', max_length=100)
    home_base = DisplayChoiceField(
        label='Home Base',
        queryset=display_location_view.objects.only('label'),
        key='label',
        empty_label=None
    )
    manager = DisplayChoiceField(
        label='Manager',
        queryset=available_as_manager_view.objects.only('username'),
        key='username',
        empty_label=None
    )

    def clean(self):
        clean_id = self.data['id']

        for service in display_service_view.objects.values():
            if service['id'] == clean_id:
                self.add_error('id', ValidationError('ID must be unique.'))

        return super().clean()


class ManageServiceForm(forms.Form):
    id = forms.CharField(label='Business ID', max_length=40)
    manager = DisplayChoiceField(
        label='Manager',
        queryset=valid_managers_view.objects.only('username'),
        key='username',
        empty_label=None
    )

    def clean(self):
        cleaned_id = self.data['id']
        cleaned_manager = self.data['manager']
        if len(valid_managers_view.objects.filter(username=cleaned_manager, id=cleaned_id)) == 0:
            self.add_error('manager', ValidationError('This user is not eligible to manage the selected service.'))
        return super().clean()


class AddRestaurantForm(forms.Form):
    long_name = forms.CharField(label='Long Name', max_length=100)
    rating = forms.IntegerField(label='Rating', validators=[
        MinValueValidator(limit_value=1, message='Rating cannot be less than 1.'),
        MaxValueValidator(limit_value=5, message='Rating cannot exceed 5.')
    ])
    spent = forms.IntegerField(label='Spent', validators=[
        MinValueValidator(limit_value=0, message='Spent cannot be negative.')
    ])
    location = DisplayChoiceField(
        label='Location',
        queryset=display_location_view.objects.only('label'),
        key='label',
        empty_label=None
    )

    def clean(self):
        clean_long_name = self.data['long_name']

        for restaurant in display_restaurant_view.objects.values():
            if restaurant['long_name'] == clean_long_name:
                self.add_error('long_name', ValidationError('Long name must be unique.'))

        return super().clean()


class PurchaseIngredientForm(forms.Form):
    long_name = forms.CharField(label='Long Name', max_length=100)
    id = DisplayChoiceField(
        label='Drone ID',
        queryset=Drones.objects.only('id').distinct().order_by('id'),
        key='id_id',
        empty_label=None
    )
    tag = DisplayChoiceField(
        label='Drone Tag',
        queryset=Drones.objects.only('tag').distinct().order_by('tag'),
        key='tag',
        empty_label=None
    )
    barcode = DisplayChoiceField(
        label='Ingredient Barcode',
        queryset=Ingredients.objects.only('barcode').order_by('barcode'),
        key='barcode',
        empty_label=None
    )
    quantity = forms.IntegerField(label='Quantity', validators=[
        MinValueValidator(1, message='Quantity cannot be less than 1')
    ])

    def clean(self):
        cleaned_long_name = self.data['long_name']
        cleaned_id = self.data['id']
        cleaned_tag = self.data['tag']
        cleaned_barcode = self.data['barcode']
        cleaned_quantity = int(self.data['quantity'])
        location = display_restaurant_view.objects.filter(long_name=cleaned_long_name).values()[0]['location']
        drone = Drones.objects.filter(id=cleaned_id, tag=cleaned_tag).values()
        payload = Payload.objects.filter(id=cleaned_id, tag=cleaned_tag, barcode=cleaned_barcode).values()
        valid_drone = True
        valid_payload = True
        if len(drone) == 0:
            valid_drone = False
            self.add_error('tag', ValidationError(f'Drone with specified id and tag does not exist.'))
        else:
            drone = drone[0]
        if len(payload) == 0:
            valid_payload = False
            self.add_error('barcode', ValidationError('Drone is not carrying requested item.'))
        else:
            payload = payload[0]
        if valid_drone and location != drone['hover_id']:
            self.add_error('tag', ValidationError('Drone is not in the same location as the restaurant.'))
        if valid_payload and payload['quantity'] < cleaned_quantity:
            self.add_error('quantity', ValidationError('Drone is not carrying the number of requested items.'))

        return super().clean()


class HireEmployeeForm(forms.Form):
    username = DisplayChoiceField(
        label='Employee Username',
        queryset=hireable_employees_view.objects.only('username'),
        key='username',
        empty_label=None
    )
    id = DisplayChoiceField(
        label='Company ID',
        queryset=DeliveryServices.objects.only('id'),
        key='id',
        empty_label=None
    )

    def clean(self):
        clean_username = self.data['username']
        clean_id = self.data['id']

        employments = work_for_view.objects.values()
        for employment in employments:
            if clean_username == employment['username'] and clean_id == employment['id']:
                self.add_error('id', ValidationError('Employee already works for the selected service.'))
        return super().clean()


class RemoveEntityForm(forms.Form):
    entity_id = forms.CharField()


class FundForm(forms.Form):
    long_name = forms.CharField(label="Restaurant Name", max_length=40)

    def clean(self):
        cleaned_data = super().clean()
        rename = cleaned_data.get('long_name')
        exists = False
        for restaurant in Restaurants.objects.values():
            if restaurant['long_name'] == rename:
                exists = True

        if not exists:
            self.add_error('long_name', ValidationError('The provided restaurant doesn\'t exist!'))
            
            return super().clean()

        return super().clean()


class AddOnwerForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    address = forms.CharField(label="Address", max_length=500)
    bdate = forms.DateField(label="Birthdate", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        bdate = cleaned_data.get('bdate')
        if bdate > date.today():
            self.add_error('bdate', ValidationError('The date of birth cannot be in the future!'))
            return super().clean()

        owners = RestaurantOwners.objects.values()
        username = cleaned_data.get('username')
        for owner in owners:
            if owner['username_id'] == username:
                self.add_error('username', ValidationError('The username is already an owner!'))
                return super().clean()


        for employee in Employees.objects.values():
            if employee['username_id'] == username:
                self.add_error('username', ValidationError('This username is already an employee!\nEmployees can not be owners!'))
                return super().clean()

        return super().clean()



class AddEmployeeForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    address = forms.CharField(label="Address", max_length=500)
    bdate = forms.DateField(label="Birthdate", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    taxID = forms.CharField(label="TaxID", max_length=40)
    hired = forms.DateField(label="Hired", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    experience = forms.IntegerField(label='Experience as Employee')
    salary = forms.IntegerField(label='Salary in USD')

    def clean(self):
        cleaned_data = super().clean()
        bdate = cleaned_data.get('bdate')
        if bdate > date.today():
            self.add_error('bdate', ValidationError('The date of birth can not be in the future.'))
            return super().clean()

        username = cleaned_data.get('username')
        for employee in Employees.objects.values():
            if employee['username_id'] == username:
                self.add_error('username', ValidationError('This username is already an employee!'))
                return super().clean()

        owners = RestaurantOwners.objects.values()
        for owner in owners:
            if owner['username_id'] == username:
                self.add_error('username', ValidationError('The username is already an owner!'))

        taxID = cleaned_data.get('taxID')
        for employee in Employees.objects.values():
            if employee['taxid'] == taxID:
                self.add_error('taxID', ValidationError('This taxID already exists!'))
                return super().clean()




class AddPilotForm(forms.Form):
    licenseID = forms.CharField(label='LicenseID', max_length=40)
    experience = forms.IntegerField(label='Experience as Pilot')

    def clean(self):
        # the licenseID must be unique
        cleaned_data = super().clean()
        id = cleaned_data.get('licenseID')
        # id = self.cleaned_data["licenseID"]
        exists = False
        for pilot in Pilots.objects.values():
            if (pilot['licenseid'] == id):
                exists = True

        if(exists):
            self.add_error('licenseID', ValidationError('This licenseID already exists!'))

        return super().clean()


class UsernameForm(forms.Form):
    username = forms.CharField(max_length=40)


class DroneForm(forms.Form):
    entity_id = forms.CharField(max_length=40)
    entity_tag = forms.IntegerField()


class RefuelDrone(forms.Form):
    fuel = forms.IntegerField(label='Fuel',
                              validators=[
                                  MinValueValidator(limit_value=0, message='Fuel cannot be negative.')
                              ])


class JoinSwarmDrone(forms.Form):
    leader_tag = forms.IntegerField(label='Leader Tag')

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        self.tag = kwargs.pop('tag', None)
        super(JoinSwarmDrone, self).__init__(*args, **kwargs)

    def clean(self):
        leader_tag = int(self.data['leader_tag'])

        #  leader drone should be a different drone
        if (leader_tag == self.tag):
            self.add_error('leader_tag', ValidationError('Leader Tag must be different'))
            return super().clean()

        # the leader drone should be valid
        exists = False
        for drone in Drones.objects.values():
            if (drone['id_id'] == self.id and drone['tag'] == leader_tag):
                exists = True

                # pilot should be valid 
                if (drone['flown_by_id'] == None):
                    self.add_error('leader_tag', ValidationError('Leader Drone must be directly controlled'))
                    return super().clean()

                location_leader = drone['hover_id']

            if (drone['id_id'] == self.id and drone['tag'] == self.tag):
                location_drone = drone['hover_id']

        if (exists == False):
            self.add_error('leader_tag', ValidationError('Invalid Leader Tag'))
            return super().clean()
        # drones must be at same location 
        if (location_drone != location_leader):
            self.add_error('leader_tag', ValidationError('Drones are at different locations'))
            return super().clean()
        return super().clean()


class TakeoverDrone(forms.Form):
    username = forms.CharField(label='Pilot Username', max_length=40)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        self.tag = kwargs.pop('tag', None)
        super(TakeoverDrone, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.data['username']
        exists = False
        for pilot in Pilots.objects.values():
            if (pilot['username_id'] == username):
                exists = True

        # Valid Pilot
        if (exists == False):
            self.add_error('username', ValidationError('Username doesnt match with any pilot'))
            return super().clean()

        # Works for same Service
        works_for_service = False
        for employment in WorkFor.objects.values():
            if (employment['username_id'] == username and employment['id_id'] == self.id):
                works_for_service = True

        if (works_for_service == False):
            self.add_error('username', ValidationError('Doesnt work for same service'))
            return super().clean()

        # check if manager 
        is_manager = False
        for service in DeliveryServices.objects.values():
            if (service['manager_id'] == username):
                is_manager = True
        if (is_manager == True):
            self.add_error('username', ValidationError('Failed - Is a manager'))
            return super().clean()

        return super().clean()


class AddDrone(forms.Form):
    id = DisplayChoiceField(
        label='Service ID',
        queryset=DeliveryServices.objects.only('id'),
        key='id',
        empty_label=None
    )
    tag = forms.IntegerField(label='Tag')
    fuel = forms.IntegerField(label='Fuel')
    capacity = forms.IntegerField(label='Capacity')
    sales = forms.IntegerField(label='Sales')
    pilot = forms.CharField(label='Pilot ID', max_length=40)

    def clean(self):
        id = self.data['id']
        tag = int(self.data['tag'])
        fuel = int(self.data['fuel'])
        capacity = int(self.data['capacity'])
        username = self.data['pilot']

        already_exists = False
        for drone in Drones.objects.values():
            if (drone['id_id'] == id and drone['tag'] == tag):
                already_exists = True

        if (already_exists == True):
            self.add_error('tag', ValidationError('Drone with this tag already exists'))
            return super().clean()

        pilot_exists = False
        for pilot in Pilots.objects.values():
            if (pilot['username_id'] == username):
                pilot_exists = True

        # Valid Pilot
        if (pilot_exists == False):
            self.add_error('pilot', ValidationError('Pilot Id doesnt match with any pilot'))
            return super().clean()

        # works for same service
        works_for_service = False
        for employment in WorkFor.objects.values():
            if (employment['username_id'] == username and employment['id_id'] == id):
                works_for_service = True

        if (works_for_service == False):
            self.add_error('pilot', ValidationError('Doesnt work for same service'))
            return super().clean()

        # check if manager 
        is_manager = False
        for service in DeliveryServices.objects.values():
            if (service['manager_id'] == username):
                is_manager = True
        if (is_manager == True):
            self.add_error('pilot', ValidationError('Failed - Is a manager'))
            return super().clean()

        if (fuel < 0):
            self.add_error('fuel', ValidationError('Fuel should be >= 0'))
            return super().clean()

        if (capacity < 0):
            self.add_error('capacity', ValidationError('Capacity should be >= 0'))
            return super().clean()

        return super().clean()


class FlyDrone(forms.Form):
    destination = DisplayChoiceField(
        label='destination',
        queryset=Locations.objects.only('label'),
        key='label',
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        self.tag = kwargs.pop('tag', None)
        super(FlyDrone, self).__init__(*args, **kwargs)

    def clean(self):
        destination = self.data['destination']

        for drone in Drones.objects.values():
            if (drone['id_id'] == self.id and drone['tag'] == self.tag):
                location = drone['hover_id']

        if (destination == location):
            self.add_error('destination', ValidationError('Already at that location'))
            return super().clean()

        return super().clean()


class LoadDrone(forms.Form):
    barcode = DisplayChoiceField(
        label='Ingridient Barcode',
        queryset=Ingredients.objects.only('barcode'),
        key='barcode',
        empty_label=None
    )

    quantity = forms.IntegerField(label='Quantity')
    price = forms.IntegerField(label='Price')

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        self.tag = kwargs.pop('tag', None)
        super(LoadDrone, self).__init__(*args, **kwargs)

    def clean(self):
        quantity = int(self.data['quantity'])
        price = int(self.data['price'])

        if (quantity <= 0):
            self.add_error('quantity', ValidationError('Quantity should be > 0'))

        for drone in Drones.objects.values():
            if (drone['id_id'] == self.id and drone['tag'] == self.tag):
                capacity = drone['capacity']

        curr_quantity = 0
        for payload in Payload.objects.values():
            if (payload['id_id'] == self.id and payload['tag_id'] == self.tag):
                curr_quantity += payload['quantity']

        if (curr_quantity + quantity > capacity):
            self.add_error('quantity', ValidationError('Execeeds drone capacity'))
        
        if (price <= 0):
            self.add_error('price', ValidationError('Price should be > 0'))
            return super().clean()

        return super().clean()

class IngridientForm(forms.Form):
    entity_barcode = forms.CharField(max_length=40)

class AddIngridientForm(forms.Form):
    barcode = forms.CharField(label='Barcode', max_length=40)
    name = forms.CharField(label='Name', max_length=100)
    weight = forms.IntegerField(label='Weight')

    def clean(self):
        barcode = self.data['barcode']
        weight = int(self.data['weight'])
        for ingredient in Ingredients.objects.values():
            if (ingredient['barcode'] == barcode):
                self.add_error('barcode', ValidationError('Barcode already exists'))

        if (weight <= 0):
            print(weight)
            self.add_error('weight', ValidationError('Weight should be > 0'))

        return super().clean()
