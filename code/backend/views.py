from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .forms import *
from .procedures import *
from .models import *


# Create your views here.

def home_view(request):
    template = loader.get_template('restaurant_supply_express/home.html')
    context = {'current_page': 'Home'}
    return HttpResponse(template.render(context, request))


def locations_view(request):
    locations = display_location_view.objects.values()
    add_form = AddLocationForm()
    remove_form = RemoveEntityForm()

    if request.method == 'POST':
        if 'add' in request.POST:
            add_form = AddLocationForm(request.POST)
            if add_form.is_valid():
                label = add_form.cleaned_data['label']
                x_coord = add_form.cleaned_data['x_coord']
                y_coord = add_form.cleaned_data['y_coord']
                space = add_form.cleaned_data['space']
                add_location(label, x_coord, y_coord, space)
                return redirect('locations')
        elif 'remove' in request.POST:
            remove_form = RemoveEntityForm(request.POST)
            if remove_form.is_valid():
                label = remove_form.cleaned_data['entity_id']
                remove_location(label)
                return redirect('locations')
    for location in locations:
        location['cant_delete'] = \
            location['no_of_restaurants'] + location['no_of_services'] + location['no_of_drones'] != 0

    template = loader.get_template('restaurant_supply_express/locations.html')
    context = {'current_page': 'Locations', 'locations': locations, 'remove_form': remove_form, 'add_form': add_form}
    return HttpResponse(template.render(context, request))


def services_view(request):
    services = display_service_view.objects.values()
    deleteable_services = deletable_services_view.objects.values()
    deleteable_services_ids = []
    for deleteable_service in deleteable_services:
        deleteable_services_ids.append(deleteable_service['id'])
    add_form = AddServiceForm()
    remove_form = RemoveEntityForm()
    manage_form = ManageServiceForm()
    if request.method == 'POST':
        if 'add' in request.POST:
            add_form = AddServiceForm(request.POST)
            if add_form.is_valid():
                service_id = add_form.cleaned_data['id']
                long_name = add_form.cleaned_data['long_name']
                home_base = add_form.cleaned_data['home_base']
                manager = add_form.cleaned_data['manager']
                add_service(service_id, long_name, home_base, manager)
                return redirect('services')
        elif 'remove' in request.POST:
            remove_form = RemoveEntityForm(request.POST)
            if remove_form.is_valid():
                service_id = remove_form.cleaned_data['entity_id']
                remove_service(service_id)
                return redirect('services')
        elif 'manage' in request.POST:
            manage_form = ManageServiceForm(request.POST)
            if manage_form.is_valid():
                manager = manage_form.cleaned_data['manager']
                service_id = manage_form.cleaned_data['id']
                manage_service(manager, service_id)
                return redirect('services')

    for service in services:
        service['cant_delete'] = service['id'] not in deleteable_services_ids

    template = loader.get_template('restaurant_supply_express/services.html')
    context = {
        'current_page': 'Services',
        'services': services,
        'remove_form': remove_form,
        'add_form': add_form,
        'manage_form': manage_form,
    }
    return HttpResponse(template.render(context, request))

def restaurants_view(request):
    restaurants = display_restaurant_view.objects.values()
    add_form = AddRestaurantForm()
    purchase_form = PurchaseIngredientForm()
    if request.method == 'POST':
        if 'add' in request.POST:
            add_form = AddRestaurantForm(request.POST)
            if add_form.is_valid():
                long_name = add_form.cleaned_data['long_name']
                rating = add_form.cleaned_data['rating']
                spent = add_form.cleaned_data['spent']
                location = add_form.cleaned_data['location']
                add_restaurant(long_name, rating, spent, location)
                return redirect('restaurants')
        elif 'purchase' in request.POST:
            purchase_form = PurchaseIngredientForm(request.POST)
            if purchase_form.is_valid():
                long_name = purchase_form.cleaned_data['long_name']
                service_id = purchase_form.cleaned_data['id']
                tag = purchase_form.cleaned_data['tag']
                barcode = purchase_form.cleaned_data['barcode']
                quantity = purchase_form.cleaned_data['quantity']
                purchase_ingredient(long_name, service_id, tag, barcode, quantity)
                return redirect('restaurants')

    template = loader.get_template('restaurant_supply_express/restaurants.html')
    context = {
        'current_page': 'Restaurants',
        'restaurants': restaurants,
        'add_form': add_form,
        'purchase_form': purchase_form,
    }
    return HttpResponse(template.render(context, request))

def employments_view(request):
    employments = work_for_view.objects.values()
    add_form = HireEmployeeForm()
    remove_form = RemoveEntityForm()

    if request.method == 'POST':
        if 'add' in request.POST:
            add_form = HireEmployeeForm(request.POST)
            if add_form.is_valid():
                username = add_form.cleaned_data['username']
                service_id = add_form.cleaned_data['id']
                hire_employee(username, service_id)
                return redirect('employments')
        elif 'remove' in request.POST:
            remove_form = RemoveEntityForm(request.POST)
            if remove_form.is_valid():
                entity_id = remove_form.cleaned_data['entity_id']
                username, service_id = entity_id.split(',')
                fire_employee(username, service_id)
                return redirect('employments')
    for employment in employments:
        employment['cant_delete'] = employment['is_manager'] or employment['drones_flown_for'] > 0

    template = loader.get_template('restaurant_supply_express/employments.html')
    context = {'current_page': 'Employments', 'employments': employments, 'remove_form': remove_form,
               'add_form': add_form}
    return HttpResponse(template.render(context, request))


def owner_view(request):
    owners = display_owner_view.objects.values()
    template = loader.get_template('restaurant_supply_express/owners.html')
    if request.method == "POST":
        if 'add_owner' in request.POST:
            add_form = AddOnwerForm(request.POST)
            remove_form = RemoveEntityForm()
            fund_form = FundForm()
            username_form = UsernameForm()
            if add_form.is_valid():
                username = add_form.cleaned_data['username']
                first_name = add_form.cleaned_data['first_name']
                last_name = add_form.cleaned_data['last_name']
                address = add_form.cleaned_data['address']
                bdate = add_form.cleaned_data['bdate']
                add_owner(username, first_name, last_name, address, bdate)
                return redirect('owners')

        elif 'remove_owner' in request.POST:
            add_form = AddOnwerForm()
            fund_form = FundForm()
            remove_form = RemoveEntityForm(request.POST)
            username_form = UsernameForm()
            if remove_form.is_valid():
                username = remove_form.cleaned_data['entity_id']
                remove_owner(username)
                return redirect('owners')

        elif 'fund_restaurant' in request.POST:
            add_form = AddOnwerForm()
            remove_form = RemoveEntityForm()
            fund_form = FundForm(request.POST)
            username_form = UsernameForm(request.POST)
            if username_form.is_valid():
                username = username_form.cleaned_data['username']
                if fund_form.is_valid():
                    long_name = fund_form.cleaned_data["long_name"]
                    start_funding(username, long_name)
                    return redirect('owners')
    else:
        add_form = AddOnwerForm()
        remove_form = RemoveEntityForm()
        fund_form = FundForm()
        username_form = UsernameForm()


    for owner in owners:
        owner['cant_delete'] = \
            owner['num_restaurants'] != 0

    context = {'current_page': 'Owners', 'owners': owners, 'add_form': add_form, 'remove_form': remove_form,'fund_form': fund_form, 'username_form' : username_form}
    return HttpResponse(template.render(context, request))


def employee_view(request):
    employees = display_employee_view.objects.values()
    template = loader.get_template('restaurant_supply_express/employees.html')

    if request.method == "POST":
        if 'add_employee' in request.POST:
            add_form = AddEmployeeForm(request.POST)
            remove_form = RemoveEntityForm()
            add_pilot_form = AddPilotForm()
            username_form = UsernameForm()
            if add_form.is_valid():
                username = add_form.cleaned_data['username']
                first_name = add_form.cleaned_data['first_name']
                last_name = add_form.cleaned_data['last_name']
                address = add_form.cleaned_data['address']
                bdate = add_form.cleaned_data['bdate']
                taxID = add_form.cleaned_data['taxID']
                hired = add_form.cleaned_data['hired']
                experience = add_form.cleaned_data['experience']
                salary = add_form.cleaned_data['salary']
                add_employee(username, first_name, last_name, address, bdate, taxID, hired, experience, salary)
                return redirect('employees')

        elif 'remove_employee' in request.POST:
            add_form = AddEmployeeForm()
            remove_form = RemoveEntityForm(request.POST)
            add_pilot_form = AddPilotForm()
            username_form = UsernameForm()
            if remove_form.is_valid():
                username = remove_form.cleaned_data['entity_id']
                fire_employee(username)
                return redirect('owners')
        
        elif 'add_pilot' in request.POST:
            add_form = AddEmployeeForm()
            remove_form = RemoveEntityForm()
            add_pilot_form = AddPilotForm(request.POST)
            username_form = UsernameForm(request.POST)
            if username_form.is_valid():
                username = username_form.cleaned_data["username"]
                if add_pilot_form.is_valid():
                    licenseID = add_pilot_form.cleaned_data['licenseID']
                    experience = add_pilot_form.cleaned_data['experience']
                    add_pilot_role(username, licenseID, experience)
                    return redirect('employees')
      
        elif 'add_worker' in request.POST:
            add_form = AddEmployeeForm()
            remove_form = RemoveEntityForm()
            add_pilot_form = AddPilotForm()
            username_form = UsernameForm(request.POST)
            if username_form.is_valid():
                username = username_form.cleaned_data["username"]
                add_worker_role(username)
                return redirect('employees')

        else:
            add_form = AddEmployeeForm()
            remove_form = RemoveEntityForm()
            add_pilot_form = AddPilotForm()
            username_form = UsernameForm()
    else:
        add_form = AddEmployeeForm()
        remove_form = RemoveEntityForm()
        add_pilot_form = AddPilotForm()
        username_form = UsernameForm()

    for employee in employees:
        employee['cant_add_pilot'] = \
            employee['licenseID'] != 'n/a'

    workers = Workers.objects.values()
    for employee in employees:
        employee['is_worker'] = False
        for worker in workers:
            if worker['username_id'] == employee['username']:
                employee['is_worker'] = True
                break


    context = {'current_page': 'Employees', 'employees': employees, 'add_form': add_form, 'add_pilot_form': add_pilot_form, 'username_form' : username_form}
    return HttpResponse(template.render(context, request))

def pilots_view(request):
    pilots = display_pilot_view.objects.values()
    template = loader.get_template('restaurant_supply_express/pilots.html')

    if request.method == "POST":
        username_form = UsernameForm(request.POST)
        if username_form.is_valid():
            username = username_form.cleaned_data["username"]
            remove_pilot_role(username)
            return redirect('pilots')
    else:
        username_form = UsernameForm()

    for pilot in pilots:
        pilot['cant_delete'] = \
            pilot['num_drones'] != 0



    context = {'current_page': 'Pilots', 'pilots': pilots, 'username_form' : username_form}
    return HttpResponse(template.render(context, request))

def drones_view(request):
    drones = Drones.objects.values()
    payload = Payload.objects.values()
    services = DeliveryServices.objects.values()
    error = 0

    if request.method == 'POST':
        if 'add_drone' in request.POST:
            add_form = AddDrone(request.POST)
            info_form = DroneForm()
            fuel_form = RefuelDrone()
            leader_form = JoinSwarmDrone()
            takeover_form = TakeoverDrone()
            fly_form = FlyDrone()
            load_form = LoadDrone()
            if add_form.is_valid():
                id = add_form.cleaned_data['id']
                tag = add_form.cleaned_data['tag']
                fuel = add_form.cleaned_data['fuel']
                capacity = add_form.cleaned_data['capacity']
                sales = add_form.cleaned_data['sales']
                pilot = add_form.cleaned_data['pilot']
                r = add_drone(id, tag, fuel, capacity, sales, pilot)
                return redirect('drones')


        elif 'remove_drone' in request.POST:
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            fuel_form = RefuelDrone()
            leader_form = JoinSwarmDrone()
            takeover_form = TakeoverDrone()
            fly_form = FlyDrone()
            load_form = LoadDrone()
            if info_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                remove_drone(id, tag)
                return redirect('drones')

        elif 'refuel_drone' in request.POST:
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            fuel_form = RefuelDrone(request.POST)
            leader_form = JoinSwarmDrone()
            takeover_form = TakeoverDrone()
            fly_form = FlyDrone()
            load_form = LoadDrone()
            if info_form.is_valid() and fuel_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                amount = fuel_form.cleaned_data['fuel']
                refuel_drone(id, tag, amount)
                return redirect('drones')

        elif 'leave_swarm' in request.POST:
            fuel_form = RefuelDrone()
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            leader_form = JoinSwarmDrone()
            takeover_form = TakeoverDrone()
            fly_form = FlyDrone()
            load_form = LoadDrone()
            if info_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                leave_swarm(id, tag)
                return redirect('drones')

        elif 'join_swarm' in request.POST:
            fuel_form = RefuelDrone()
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            takeover_form = TakeoverDrone()
            fly_form = FlyDrone()
            load_form = LoadDrone()
            if info_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                leader_form = JoinSwarmDrone(data=request.POST, id=id, tag=tag)
                if (leader_form.is_valid()):
                    leader_tag = leader_form.cleaned_data['leader_tag']
                    join_swarm(id,tag,leader_tag)
                    return redirect('drones')
        
        elif 'takeover_drone' in request.POST:
            fuel_form = RefuelDrone()
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            leader_form = JoinSwarmDrone()
            fly_form = FlyDrone()
            load_form = LoadDrone()
            if info_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                takeover_form = TakeoverDrone(data = request.POST,id = id,tag = tag)
                if (takeover_form.is_valid()):
                    username = takeover_form.cleaned_data['username']
                    takeover_drone(id,tag,username)
                    return redirect('drones')
        
        elif 'fly_drone' in request.POST:
            fuel_form = RefuelDrone()
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            leader_form = JoinSwarmDrone()
            takeover_form = TakeoverDrone()
            load_form = LoadDrone()
            if info_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                fly_form = FlyDrone(data = request.POST,id = id,tag = tag)
                if (fly_form.is_valid()):
                    destination = fly_form.cleaned_data['destination']
                    r = (fly_drone(id,tag,destination))
                    if (r==None):
                        error = 0
                        return redirect('drones')
                    else:
                        error = 1 
        elif 'load_drone' in request.POST:
            fuel_form = RefuelDrone()
            add_form = AddDrone()
            info_form = DroneForm(request.POST)
            leader_form = JoinSwarmDrone()
            takeover_form = TakeoverDrone()
            fly_form = FlyDrone()
            if info_form.is_valid():
                id = info_form.cleaned_data['entity_id']
                tag = info_form.cleaned_data['entity_tag']
                load_form = LoadDrone(data = request.POST,id = id,tag = tag)
                if (load_form.is_valid()):
                    barcode = load_form.cleaned_data['barcode']
                    quantity = load_form.cleaned_data['quantity']
                    price = load_form.cleaned_data['price']
                    load_drone(id, tag, barcode, quantity, price)
                    return redirect('drones')




    else:
        fuel_form = RefuelDrone()
        add_form = AddDrone()
        info_form = DroneForm()
        leader_form = JoinSwarmDrone()
        takeover_form = TakeoverDrone()
        fly_form = FlyDrone()
        load_form = LoadDrone()


    for drone in drones:
        total_load = 0
        drone['cant_delete'] = False
        drone['cant_join_swarm'] = False

        # only drones that are not carrying any ingredients can be removed
        for load in payload:
            if ((load['id_id'] == drone['id_id']) and (load['tag_id'] == drone['tag'])):
                total_load += load['quantity']
        if (total_load != 0):
            drone['cant_delete'] = True

        # leader drones can't be removed and can't join swarm
        for follower in drones:
            if ((drone['tag'] == follower['swarm_tag_id']) and (drone['id_id'] == follower['swarm_id'])):
                drone['cant_delete'] = True
                drone['cant_join_swarm'] = True

        # only drones at home base can be refuelled
        drone['cant_refuel'] = True
        for service in services:
            if (drone['id_id'] == service['id'] and drone['hover_id'] == service['home_base_id']):
                drone['cant_refuel'] = False

        drone['cant_leave_swarm'] = False
        drone['cant_takeover'] = True
        drone['cant_fly'] = True
        if (drone['swarm_tag_id'] == None and drone['swarm_id'] == None):
            drone['cant_leave_swarm'] = True
            drone['cant_takeover'] = False
            drone['cant_fly'] = False
        

    template = loader.get_template('restaurant_supply_express/drones.html')
    context = {'current_page': 'Drones', 'drones': drones, 'info_form' : info_form, 'fuel_form':fuel_form, 'leader_form':leader_form, 'takeover_form':takeover_form, 'add_form':add_form, 'fly_form':fly_form, 'error':error, 'load_form':load_form}
    return HttpResponse(template.render(context, request))


def payload_view(request):
    payloads = Payload.objects.values()
    template = loader.get_template('restaurant_supply_express/payload.html')
    context = {'current_page': 'Payload', 'payloads':payloads}
    return HttpResponse(template.render(context, request))

def ingredient_table_view(request):
    ingredients = Ingredients.objects.values()
    payloads = Payload.objects.values()

    if request.method == 'POST':
        if 'remove_ingredient' in request.POST:
            info_form = IngridientForm(request.POST)
            add_form = AddIngridientForm()
            if info_form.is_valid():
                barcode = info_form.cleaned_data['entity_barcode']
                remove_ingredient(barcode)
                return redirect('ingredient_table')

        elif 'add_ingredient' in request.POST:
            info_form = IngridientForm()
            add_form = AddIngridientForm(request.POST)
            if add_form.is_valid():
                barcode = add_form.cleaned_data['barcode']
                name = add_form.cleaned_data['name']
                weight = add_form.cleaned_data['weight']
                add_ingredient(barcode, name, weight)
                return redirect('ingredient_table')

    else:
        info_form = IngridientForm()
        add_form = AddIngridientForm()

    for ingredient in ingredients:
        ingredient['cant_delete'] = False
        for payload in payloads:
            if(payload['barcode_id'] == ingredient['barcode']):
                ingredient['cant_delete'] = True
    
    template = loader.get_template('restaurant_supply_express/ingredient_table.html')
    context = {'current_page': 'Ingredient Table', 'ingredients':ingredients, 'info_form':info_form, 'add_form':add_form}
    return HttpResponse(template.render(context, request))

def ingredient_view(request):
    template = loader.get_template('restaurant_supply_express/ingredient_view.html')
    context = {'current_page': 'Ingredient View', 'information': display_ingredient_view.objects.values()}
    return HttpResponse(template.render(context, request))

