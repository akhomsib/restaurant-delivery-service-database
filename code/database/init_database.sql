-- Restaurant Delivery Service Database
-- Database Schema
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

drop database if exists restaurant_supply_express;
create database if not exists restaurant_supply_express;
use restaurant_supply_express;
-- -----------------------------------------------
-- table structures
-- -----------------------------------------------

create table users (
username varchar(40) not null,
first_name varchar(100) not null,
last_name varchar(100) not null,
address varchar(500) not null,
birthdate date not null,
primary key (username)
) engine = innodb;

create table employees (
username varchar(40) not null,
taxID varchar(40) not null,
hired date not null,
experience integer not null,
salary integer not null,
primary key (username),
unique key (taxID)
) engine = innodb;

create table restaurant_owners (
username varchar(40) not null,
primary key (username)
) engine = innodb;

create table pilots (
username varchar(40) not null,
licenseID varchar(40) not null,
experience integer not null,
primary key (username),
unique key (licenseID)
) engine = innodb;

create table workers (
username varchar(40) not null,
primary key (username)
) engine = innodb;

create table ingredients (
barcode varchar(40) not null,
iname varchar(100) not null,
weight integer not null,
primary key (barcode)
) engine = innodb;

create table locations (
label varchar(40) not null,
x_coord integer not null,
y_coord integer not null,
space integer not null,
primary key (label)
) engine = innodb;

create table restaurants (
long_name varchar(40) not null,
rating integer not null,
spent integer not null,
location varchar(40) not null,
funded_by varchar(40) default null,
primary key (long_name)
) engine = innodb;

create table delivery_services (
id varchar(40) not null,
long_name varchar(100) not null,
home_base varchar(40) not null,
manager varchar(40) not null,
primary key (id),
unique key (manager)
) engine = innodb;

create table drones (
id varchar(40) not null,
tag integer not null,
fuel integer not null,
capacity integer not null,
sales integer not null,
flown_by varchar(40) default null,
swarm_id varchar(40) default null,
swarm_tag integer default null,
hover varchar(40) not null,
primary key (id, tag)
) engine = innodb;

create table payload (
id varchar(40) not null,
tag integer not null,
barcode varchar(40) not null,
quantity integer not null,
price integer not null,
primary key (id, tag, barcode)
) engine = innodb;

create table work_for (
username varchar(40) not null,
id varchar(40) not null,
primary key (username, id)
) engine = innodb;

-- -----------------------------------------------
-- referential structures
-- -----------------------------------------------

alter table employees add constraint fk1 foreign key (username) references users (username)
	on update cascade on delete cascade;
alter table restaurant_owners add constraint fk2 foreign key (username)
	references users (username) on update cascade on delete cascade;
alter table pilots add constraint fk3 foreign key (username) references employees (username)
	on update cascade on delete cascade;
alter table workers add constraint fk4 foreign key (username) references employees (username)
	on update cascade on delete cascade;
alter table restaurants add constraint fk10 foreign key (location) references locations (label)
	on update cascade;
alter table restaurants add constraint fk12 foreign key (funded_by)
	references restaurant_owners (username);
alter table delivery_services add constraint fk11 foreign key (home_base)
	references locations (label) on update cascade;
alter table delivery_services add constraint fk15 foreign key (manager)
	references workers (username);
alter table drones add constraint fk5 foreign key (id) references delivery_services (id);
alter table drones add constraint fk13 foreign key (flown_by) references pilots (username);
alter table drones add constraint fk14 foreign key (swarm_id, swarm_tag)
	references drones (id, tag) on update cascade on delete cascade;
alter table drones add constraint fk16 foreign key (hover) references locations (label)
	on update cascade;
alter table payload add constraint fk6 foreign key (id, tag) references drones (id, tag);
alter table payload add constraint fk7 foreign key (barcode) references ingredients (barcode);
alter table work_for add constraint fk8 foreign key (username) references employees (username);
alter table work_for add constraint fk9 foreign key (id) references delivery_services (id);

-- -----------------------------------------------
-- table data
-- -----------------------------------------------

insert into users values
('jstone5', 'Jared', 'Stone', '101 Five Finger Way', '1961-01-06'),
('sprince6', 'Sarah', 'Prince', '22 Peachtree Street', '1968-06-15'),
('awilson5', 'Aaron', 'Wilson', '220 Peachtree Street', '1963-11-11'),
('lrodriguez5', 'Lina', 'Rodriguez', '360 Corkscrew Circle', '1975-04-02'),
('tmccall5', 'Trey', 'McCall', '360 Corkscrew Circle', '1973-03-19'),
('eross10', 'Erica', 'Ross', '22 Peachtree Street', '1975-04-02'),
('hstark16', 'Harmon', 'Stark', '53 Tanker Top Lane', '1971-10-27'),
('echarles19', 'Ella', 'Charles', '22 Peachtree Street', '1974-05-06'),
('csoares8', 'Claire', 'Soares', '706 Living Stone Way', '1965-09-03'),
('agarcia7', 'Alejandro', 'Garcia', '710 Living Water Drive', '1966-10-29'),
('bsummers4', 'Brie', 'Summers', '5105 Dragon Star Circle', '1976-02-09'),
('cjordan5', 'Clark', 'Jordan', '77 Infinite Stars Road', '1966-06-05'),
('fprefontaine6', 'Ford', 'Prefontaine', '10 Hitch Hikers Lane', '1961-01-28'),
('mrobot1', 'Mister', 'Robot', '10 Autonomy Trace', '1988-11-02'),
('mrobot2', 'Mister', 'Robot', '10 Clone Me Circle', '1988-11-02'),
('ckann5', 'Carrot', 'Kann', '64 Knights Square Trail', '1972-09-01'),
('rlopez6', 'Radish', 'Lopez', '8 Queens Route', '1999-09-03');

insert into employees values
('awilson5', '111-11-1111', '2020-03-15', 9, 46000),
('lrodriguez5', '222-22-2222', '2019-04-15', 20, 58000),
('tmccall5', '333-33-3333', '2018-10-17', 29, 33000),
('eross10', '444-44-4444', '2020-04-17', 10, 61000),
('hstark16', '555-55-5555', '2018-07-23', 20, 59000),
('echarles19', '777-77-7777', '2021-01-02', 3, 27000),
('csoares8', '888-88-8888', '2019-02-25', 26, 57000),
('agarcia7', '999-99-9999', '2019-03-17', 24, 41000),
('bsummers4', '000-00-0000', '2018-12-06', 17, 35000),
('fprefontaine6', '121-21-2121', '2020-04-19', 5, 20000),
('mrobot1', '101-01-0101', '2015-05-27', 8, 38000),
('mrobot2', '010-10-1010', '2015-05-27', 8, 38000),
('ckann5', '640-81-2357', '2019-08-03', 27, 46000),
('rlopez6', '123-58-1321', '2017-02-05', 51, 64000);

insert into restaurant_owners values
('jstone5'), ('sprince6'), ('cjordan5');

insert into pilots values
('awilson5', '314159', 41), ('lrodriguez5', '287182', 67),
('tmccall5', '181633', 10), ('agarcia7', '610623', 38),
('bsummers4', '411911', 35), ('fprefontaine6', '657483', 2),
('echarles19', '236001', 10), ('csoares8', '343563', 7),
('mrobot1', '101010', 18), ('rlopez6', '235711', 58);

insert into workers values
('tmccall5'), ('eross10'), ('hstark16'), ('echarles19'),
('csoares8'), ('mrobot2'), ('ckann5');

insert into ingredients values
('pr_3C6A9R', 'prosciutto', 6), ('ss_2D4E6L', 'saffron', 3),
('hs_5E7L23M', 'truffles', 3), ('clc_4T9U25X', 'caviar', 5),
('ap_9T25E36L', 'foie gras', 4), ('bv_4U5L7M', 'balsamic vinegar', 4);

insert into locations values
('plaza', 5, 12, 20), ('midtown', 1, 4, 3), ('highpoint', 7, 0, 2),
('southside', 3, -6, 3), ('mercedes', 1, 1, 2), ('avalon', 2, 16, 5),
('airport', -2, -9, 4), ('buckhead', 3, 8, 4);

insert into restaurants values
('Lure', 5, 20, 'midtown', 'jstone5'), ('Ecco', 3, 0, 'buckhead', 'jstone5'),
('South City Kitchen', 5, 30, 'midtown', 'jstone5'), ('Tre Vele', 4, 10, 'plaza', null),
('Fogo de Chao', 4, 30, 'buckhead', null), ('Hearth', 4, 0, 'avalon', null),
('Il Giallo', 4, 10, 'mercedes', 'sprince6'), ('Bishoku', 5, 10, 'plaza', null),
('Casi Cielo', 5, 30, 'plaza', null), ('Micks', 2, 0, 'southside', null);

insert into delivery_services values
('osf', 'On Safari Foods', 'southside', 'eross10'),
('hf', 'Herban Feast', 'southside', 'hstark16'),
('rr', 'Ravishing Radish', 'avalon', 'echarles19');

insert into drones values
('osf', 1, 100, 9, 0, 'awilson5', null, null, 'airport'),
('hf', 1, 100, 6, 0, 'fprefontaine6', null, null, 'southside'),
('hf', 5, 27, 7, 100, 'fprefontaine6', null, null, 'buckhead'),
('hf', 8, 100, 8, 0, 'bsummers4', null, null, 'southside'),
('hf', 16, 17, 5, 40, 'fprefontaine6', null, null, 'buckhead'),
('rr', 3, 100, 5, 50, 'agarcia7', null, null, 'avalon'),
('rr', 7, 53, 5, 100, 'agarcia7', null, null, 'avalon'),
('rr', 8, 100, 6, 0, 'agarcia7', null, null, 'highpoint');

insert into drones values
('osf', 2, 75, 7, 0, null, 'osf', 1, 'airport'),
('hf', 11, 25, 10, 0, null, 'hf', 5, 'buckhead'),
('rr', 11, 90, 6, 0, null, 'rr', 8, 'highpoint');

insert into payload values
('osf', 1, 'pr_3C6A9R', 5, 20),
('osf', 1, 'ss_2D4E6L', 3, 23),
('osf', 2, 'hs_5E7L23M', 7, 14),
('hf', 1, 'ss_2D4E6L', 6, 27),
('hf', 5, 'hs_5E7L23M', 4, 17),
('hf', 5, 'clc_4T9U25X', 1, 30),
('hf', 8, 'pr_3C6A9R', 4, 18),
('hf', 11, 'ss_2D4E6L', 3, 19),
('rr', 3, 'hs_5E7L23M', 2, 15),
('rr', 3, 'clc_4T9U25X', 2, 28);

insert into work_for values
('eross10', 'osf'), ('hstark16', 'hf'), ('echarles19', 'rr'),
('tmccall5', 'hf'), ('awilson5', 'osf'), ('fprefontaine6', 'hf'),
('bsummers4', 'hf'), ('agarcia7', 'rr'), ('mrobot1', 'osf'),
('mrobot1', 'rr'), ('ckann5', 'osf'), ('rlopez6', 'rr');


-- Restaurant Delivery Service Database
-- Stored Procedures
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

use restaurant_supply_express;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [1] add_owner()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new owner.  A new owner must have a unique
username.  Also, the new owner is not allowed to be an employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_owner;
delimiter //
create procedure add_owner (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date)
sp_main: begin
    -- ensure new owner has a unique username
    if(ip_username in (select username from employees) or ip_username in (select username from restaurant_owners))
		then leave sp_main; end if;
    if(ip_username not in (select username from users))
	then insert into users values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate); end if;
	
    insert into restaurant_owners values (ip_username);
end //
delimiter ;

-- [custom] remove_owner())
-- -----------------------------------------------------------------------------
/* This stored procedure deletes a owner. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_owner;
delimiter //
create procedure remove_owner (in ip_username varchar(40))
sp_main: begin
	-- ensure the owner exists
    if not exists (select * from restaurant_owners where ip_username = restaurant_owners.username) then leave sp_main; end if;
    -- ensure the owner doesn't own a restaurant
	if exists (select * from restaurants where ip_username = restaurants.funded_by) then leave sp_main; end if;

	delete from restaurant_owners where ip_username = restaurant_owners.username;

end //
delimiter ;


-- [2] add_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new employee without any designated pilot or
worker roles.  A new employee must have a unique username unique tax identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_employee;
delimiter //
create procedure add_employee (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date,
    in ip_taxID varchar(40), in ip_hired date, in ip_employee_experience integer,
    in ip_salary integer)
sp_main: begin
	if(ip_username in (select username from employees))
		then leave sp_main; end if;
	if(ip_taxID in (select taxID from employees))
		then leave sp_main; end if;
	if(ip_username not in (select username from users))
		then insert into users values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
		end if;
    insert into employees values (ip_username, ip_taxID, ip_hired, ip_employee_experience, ip_salary);
    -- ensure new owner has a unique username
    -- ensure new employee has a unique tax identifier
end //
delimiter ;


-- [3] add_pilot_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the pilot role to an existing employee.  The
employee/new pilot must have a unique license identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_pilot_role;
delimiter //
create procedure add_pilot_role (in ip_username varchar(40), in ip_licenseID varchar(40),
	in ip_pilot_experience integer)
sp_main: begin
    -- ensure new employee exists
	if not exists (select * from employees where ip_username = employees.username) then leave sp_main; end if;
    -- ensure new pilot has a unique license identifier
	if exists (select * from pilots where ip_licenseID = pilots.licenseID) then leave sp_main; end if;
	insert into pilots values (ip_username, ip_licenseID, ip_pilot_experience);
end //
delimiter ;


-- [4] add_worker_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the worker role to an existing employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_worker_role;
delimiter //
create procedure add_worker_role (in ip_username varchar(40))
sp_main: begin
    -- ensure new employee exists
    if (select count(*) from employees where employees.username = ip_username) = 0
    then leave sp_main; end if;

    insert into workers values (ip_username);
end //
delimiter ;


-- [5] add_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new ingredient.  A new ingredient must have a
unique barcode. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_ingredient;
delimiter //
create procedure add_ingredient (in ip_barcode varchar(40), in ip_iname varchar(100),
	in ip_weight integer)
sp_main: begin
	-- ensure new ingredient doesn't already exist
	if exists (select * from ingredients where ip_barcode = ingredients.barcode) then leave sp_main; end if;
	insert into ingredients values (ip_barcode, ip_iname, ip_weight);
end //
delimiter ;


-- [6] add_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new drone.  A new drone must be assigned
to a valid delivery service and must have a unique tag.  Also, it must be flown
by a valid pilot initially (i.e., pilot works for the same service), but the pilot
can switch the drone to working as part of a swarm later. And the drone's starting
location will always be the delivery service's home base by default. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_drone;
delimiter //
create procedure add_drone (in ip_id varchar(40), in ip_tag integer, in ip_fuel integer,
	in ip_capacity integer, in ip_sales integer, in ip_flown_by varchar(40))
sp_main: begin

	-- ensure new drone doesn't already exist
	if exists (select * from drones where tag=ip_tag and id=ip_id) then leave sp_main; end if;

    -- ensure that the delivery service exists
	if not exists (select * from delivery_services where id = ip_id) then leave sp_main; end if;

    -- ensure that a valid pilot will control the drone
	if not exists (select * from pilots where username = ip_flown_by) then leave sp_main; end if;
    if not exists (select * from work_for where username = ip_flown_by and id = ip_id) then leave sp_main; end if;

	insert into drones values (ip_id, ip_tag, ip_fuel, ip_capacity, ip_sales, ip_flown_by, null, null, (select home_base from delivery_services where id=ip_id));

end //
delimiter ;

-- [7] add_restaurant()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new restaurant.  A new restaurant must have a
unique (long) name and must exist at a valid location, and have a valid rating.
And a resturant is initially "independent" (i.e., no owner), but will be assigned
an owner later for funding purposes. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_restaurant;
delimiter //
create procedure add_restaurant (in ip_long_name varchar(40), in ip_rating integer,
	in ip_spent integer, in ip_location varchar(40))
sp_main: begin
	-- ensure new restaurant doesn't already exist
    if (select count(*) from restaurants where long_name = ip_long_name) > 0
    then leave sp_main; end if;
    -- ensure that the location is valid
    if ip_location not in (select label from locations)
    then leave sp_main; end if;
    -- ensure that the rating is valid (i.e., between 1 and 5 inclusively)
    if ip_rating not between 1 and 5
    then leave sp_main; end if;

    insert into restaurants values (ip_long_name, ip_rating, ip_spent, ip_location, NULL);
end //
delimiter ;


-- [8] add_service()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new delivery service.  A new service must have
a unique identifier, along with a valid home base and manager. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_service;
delimiter //
create procedure add_service (in ip_id varchar(40), in ip_long_name varchar(100),
	in ip_home_base varchar(40), in ip_manager varchar(40))
sp_main: begin
	-- ensure new delivery service doesn't already exist
    if ip_id in (select id from delivery_services)
    then leave sp_main; end if;
    -- ensure that the home base location is valid
    if ip_home_base not in (select label from locations)
    then leave sp_main; end if;
    -- ensure that the manager is valid
    if ip_manager not in (select username from workers)
    then leave sp_main; end if;
    if (select count(*) from delivery_services where manager = ip_manager) > 0
    then leave sp_main; end if;
	insert into delivery_services values (ip_id, ip_long_name, ip_home_base, ip_manager);
	insert into work_for values (ip_manager, ip_id);
end //
delimiter ;

-- [custom] remove_service()
-- -----------------------------------------------------------------------------
/* This stored procedure deletes a service. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_service;
delimiter //
create procedure remove_service (in ip_id varchar(40))
sp_main: begin
	-- ensure the service exists
    if not exists (select * from delivery_services where ip_id = delivery_services.id) then leave sp_main; end if;
    -- ensure the id is not in drones
    if exists (select * from drones where ip_id = drones.id) then leave sp_main; end if;

    delete from work_for where ip_id = work_for.id;
	delete from delivery_services where ip_id = id;

end //
delimiter ;

-- [9] add_location()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new location that becomes a new valid drone
destination.  A new location must have a unique combination of coordinates.  We
could allow for "aliased locations", but this might cause more confusion that
it's worth for our relatively simple system. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_location;
delimiter //
create procedure add_location (in ip_label varchar(40), in ip_x_coord integer,
	in ip_y_coord integer, in ip_space integer)
sp_main: begin
	-- ensure new location doesn't already exist
    if ip_label in (select label from locations)
    then leave sp_main; end if;
    -- ensure that the coordinate combination is distinct
    if (select count(*) from locations where x_coord = ip_x_coord and y_coord = ip_y_coord) > 0
    then leave sp_main; end if;

	insert into locations values (ip_label, ip_x_coord, ip_y_coord, ip_space);

end //
delimiter ;

-- [custom] remove_location()
-- -----------------------------------------------------------------------------
/* This stored procedure deletes a location. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_location;
delimiter //
create procedure remove_location (in ip_label varchar(40))
sp_main: begin
	-- ensure the location exists
    if not exists (select * from locations where ip_label = locations.label) then leave sp_main; end if;
    -- ensure the location is not in restaurants
    if exists (select * from restaurants where ip_label = restaurants.location) then leave sp_main; end if;
	-- ensure the location is not in drones
    if exists (select * from drones where ip_label = drones.hover) then leave sp_main; end if;
	-- ensure the location is not in delivery_services
    if exists (select * from delivery_services where ip_label = delivery_services.home_base) then leave sp_main; end if;

	delete from locations where ip_label = label;

end //
delimiter ;

-- [10] start_funding()
-- -----------------------------------------------------------------------------
/* This stored procedure opens a channel for a restaurant owner to provide funds
to a restaurant. If a different owner is already providing funds, then the current
owner is replaced with the new owner.  The owner and restaurant must be valid. */
-- -----------------------------------------------------------------------------
drop procedure if exists start_funding;
delimiter //
create procedure start_funding (in ip_owner varchar(40), in ip_long_name varchar(40))
sp_main: begin
	-- ensure the owner and restaurant are valid
    if(ip_owner not in (select username from restaurant_owners))
		then leave sp_main; end if;
	if(ip_long_name not in (select long_name from restaurants))
		then leave sp_main; end if;

    update restaurants set funded_by = ip_owner where long_name = ip_long_name;
end //
delimiter ;


-- [11] hire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure hires an employee to work for a delivery service.
Employees can be combinations of workers and pilots. If an employee is actively
controlling drones or serving as manager for a different service, then they are
not eligible to be hired.  Otherwise, the hiring is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists hire_employee;
delimiter //
create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee hasn't already been hired
    if(ip_username in (select username from work_for where id = ip_id))
		then leave sp_main; end if;
	-- ensure that the employee and delivery service are valid
	if(ip_username not in (select username from employees) or ip_id not in (select id from delivery_services))
		then leave sp_main; end if;
    -- ensure that the employee isn't a manager for another service
    if(ip_username in (select manager from delivery_services where id != ip_id))
		then leave sp_main; end if;
	-- ensure that the employee isn't actively controlling drones for another service
    if(ip_username in (select flown_by from drones where id != ip_id))
		then leave sp_main; end if;
	insert into work_for values (ip_username, ip_id);
end //
delimiter ;


-- [12] fire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure fires an employee who is currently working for a delivery
service.  The only restrictions are that the employee must not be: [1] actively
controlling one or more drones; or, [2] serving as a manager for the service.
Otherwise, the firing is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists fire_employee;
delimiter //
create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
    if(ip_username not in (select username from work_for where id = ip_id))
		then leave sp_main; end if;
    -- ensure that the employee isn't an active manager
    if(ip_username in (select manager from delivery_services where id = ip_id))
		then leave sp_main; end if;
	-- ensure that the employee isn't controlling any drones
    if(ip_username in (select flown_by from drones))
		then leave sp_main; end if;

	delete from work_for where id = ip_id and username = ip_username;
end //
delimiter ;


-- [13] manage_service()
-- -----------------------------------------------------------------------------
/* This stored procedure appoints an employee who is currently hired by a delivery
service as the new manager for that service.  The only restrictions are that: [1]
the employee must not be working for any other delivery service; and, [2] the
employee can't be flying drones at the time.  Otherwise, the appointment to manager
is permitted.  The current manager is simply replaced.  And the employee must be
granted the worker role if they don't have it already. */
-- -----------------------------------------------------------------------------
drop procedure if exists manage_service;
delimiter //
create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
    if (select count(*) from work_for where username = ip_username and id = ip_id) = 0
    then leave sp_main; end if;
	-- ensure that the employee is not flying any drones
    if (select count(*) from drones where flown_by = ip_username) > 0
    then leave sp_main; end if;
    -- ensure that the employee isn't working for any other services
    if (select count(*) from work_for where username = ip_username and id != ip_id) > 0
    then leave sp_main; end if;
    -- add the worker role if necessary
    if ip_username not in (select username from workers)
    then insert into workers values (ip_username); end if;

	update delivery_services set manager = ip_username where id = ip_id;
end //
delimiter ;


-- [14] takeover_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a valid pilot to take control of a lead drone owned
by the same delivery service, whether it's a "lone drone" or the leader of a swarm.
The current controller of the drone is simply relieved of those duties. And this
should only be executed if a "leader drone" is selected. */
-- -----------------------------------------------------------------------------
drop procedure if exists takeover_drone;
delimiter //
create procedure takeover_drone (in ip_username varchar(40), in ip_id varchar(40),
	in ip_tag integer)
sp_main: begin
	-- ensure that the employee is currently working for the service
	if not exists (select * from work_for where ip_username = work_for.username and ip_id = work_for.id) then leave sp_main; end if;
	-- ensure that the selected drone is owned by the same service and is a leader and not follower
	if not exists (select * from drones where ip_id = drones.id and ip_tag = drones.tag and drones.swarm_tag is NULL and drones.swarm_id is NULL) then leave sp_main; end if;
	-- ensure that the employee isn't a manager
	if exists (select * from delivery_services where ip_username = delivery_services.manager) then leave sp_main; end if;
    -- ensure that the employee is a valid pilot
	if not exists (select * from pilots where ip_username = pilots.username) then leave sp_main; end if;

	update drones set flown_by = ip_username where ip_id = drones.id and ip_tag = drones.tag;

end //
delimiter ;

-- [15] join_swarm()
-- -----------------------------------------------------------------------------
/* This stored procedure takes a drone that is currently being directly controlled
by a pilot and has it join a swarm (i.e., group of drones) led by a different
directly controlled drone. A drone that is joining a swarm connot be leading a
different swarm at this time.  Also, the drones must be at the same location, but
they can be controlled by different pilots. */
-- -----------------------------------------------------------------------------
drop procedure if exists join_swarm;
delimiter //
create procedure join_swarm (in ip_id varchar(40), in ip_tag integer,
	in ip_swarm_leader_tag integer)
sp_main: begin
	-- ensure that the drone joining the swarm is valid and owned by the service
	if (ip_id is null) then leave sp_main; end if;
	if not exists (select * from drones where tag=ip_tag and id=ip_id) then leave sp_main; end if;

	-- ensure that the swarm leader is a different drone
	if (ip_tag = ip_swarm_leader_tag) then leave sp_main; end if;

    -- ensure that the drone joining the swarm is not already leading a swarm
	if (ip_tag in (select swarm_tag from drones where swarm_id = ip_id)) then leave sp_main; end if;

	-- ensure that the swarm leader drone is directly controlled
	if ((select flown_by from drones where tag = ip_swarm_leader_tag and id=ip_id) is null) then leave sp_main; end if;

	-- -- ensure that the drones are at the same location
	if ((select hover from drones where tag=ip_tag and id=ip_id) != (select hover from drones where tag=ip_swarm_leader_tag and id=ip_id)) then leave sp_main; end if;

	update drones set swarm_tag = ip_swarm_leader_tag, swarm_id = ip_id, flown_by = null where ip_id = drones.id and ip_tag = drones.tag;
end //
delimiter ;

-- [16] leave_swarm()
-- -----------------------------------------------------------------------------
/* This stored procedure takes a drone that is currently in a swarm and returns
it to being directly controlled by the same pilot who's controlling the swarm. */
-- -----------------------------------------------------------------------------
drop procedure if exists leave_swarm;
delimiter //
create procedure leave_swarm (in ip_id varchar(40), in ip_swarm_tag integer)
sp_main: begin

	DECLARE leader_id varchar(40);
	DECLARE leader_tag integer;
	DECLARE pilot varchar(40);

	if not exists (select * from drones where tag=ip_swarm_tag and id=ip_id) then leave sp_main; end if;

	SET leader_id = (select swarm_id from drones where tag=ip_swarm_tag and id=ip_id);
	SET leader_tag = (select swarm_tag from drones where tag=ip_swarm_tag and id=ip_id);
	SET pilot = (select flown_by from drones where id=leader_id and tag = leader_tag);

	-- ensure that the selected drone is owned by the service and flying in a swarm
	if (ip_id is null) then leave sp_main; end if;
	if leader_id is null then leave sp_main; end if;
	if leader_tag is null then leave sp_main; end if;

	update drones set flown_by = pilot where ip_id = drones.id and ip_swarm_tag = drones.tag;
	update drones set swarm_tag = null, swarm_id = null where ip_id = drones.id and ip_swarm_tag = drones.tag;



end //
delimiter ;

-- [17] load_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add some quantity of fixed-size packages of
a specific ingredient to a drone's payload so that we can sell them for some
specific price to other restaurants.  The drone can only be loaded if it's located
at its delivery service's home base, and the drone must have enough capacity to
carry the increased number of items.

The change/delta quantity value must be positive, and must be added to the quantity
of the ingredient already loaded onto the drone as applicable.  And if the ingredient
already exists on the drone, then the existing price must not be changed. */
-- -----------------------------------------------------------------------------
drop procedure if exists load_drone;
delimiter //
create procedure load_drone (in ip_id varchar(40), in ip_tag integer, in ip_barcode varchar(40),
	in ip_more_packages integer, in ip_price integer)
sp_main: begin

	DECLARE home varchar(40);
	DECLARE curr_quantity integer;

	-- ensure that the drone being loaded is owned by the service
	if not exists (select * from drones where tag=ip_tag and id=ip_id) then leave sp_main; end if;
	if (ip_id is null) then leave sp_main; end if;

	SET home = (select home_base from delivery_services where id = ip_id);
	SET curr_quantity = (select sum(quantity) from payload where id = ip_id and tag = ip_tag);


	-- ensure that the ingredient is valid
	if not exists (select * from ingredients where barcode = ip_barcode) then leave sp_main; end if;

    -- ensure that the drone is located at the service home base
	if ((select hover from drones where id = ip_id and tag = ip_tag) != home) then leave sp_main; end if;

	-- ensure that the quantity of new packages is greater than zero
	if (ip_more_packages <= 0) then leave sp_main; end if;

	-- ensure that the drone has sufficient capacity to carry the new packages
	if (curr_quantity + ip_more_packages > (select capacity from drones where id = ip_id and tag = ip_tag)) then leave sp_main; end if;

	-- add more of the ingredient to the drone
	-- if ingridient alrady exists on the drone, then add quantity 
    if exists (select * from payload where barcode = ip_barcode and id = ip_id and tag = ip_tag) then
        update payload set quantity = quantity + ip_more_packages where id = ip_id and tag = ip_tag and barcode = ip_barcode;  leave sp_main; end if;

	insert into payload values (ip_id, ip_tag, ip_barcode, ip_more_packages, ip_price);

end //
delimiter ;

-- [18] refuel_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add more fuel to a drone. The drone can only
be refueled if it's located at the delivery service's home base. */
-- -----------------------------------------------------------------------------
drop procedure if exists refuel_drone;
delimiter //
create procedure refuel_drone (in ip_id varchar(40), in ip_tag integer, in ip_more_fuel integer)
sp_main: begin

	DECLARE home varchar(40);

	-- ensure that the drone being switched is valid and owned by the service
	if not exists (select * from drones where tag=ip_tag and id=ip_id) then leave sp_main; end if;
	if (ip_id is null) then leave sp_main; end if;


	SET home = (select home_base from delivery_services where id = ip_id);


    -- ensure that the drone is located at the service home base
	if ((select hover from drones where id = ip_id and tag = ip_tag) != home) then leave sp_main; end if;

	update drones set fuel = ip_more_fuel+fuel where ip_id = drones.id and ip_tag = drones.tag;

end //
delimiter ;

-- [19] fly_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to move a single or swarm of drones to a new
location (i.e., destination). The main constraints on the drone(s) being able to
move to a new location are fuel and space.  A drone can only move to a destination
if it has enough fuel to reach the destination and still move from the destination
back to home base.  And a drone can only move to a destination if there's enough
space remaining at the destination.  For swarms, the flight directions will always
be given to the lead drone, but the swarm must always stay together. */
-- -----------------------------------------------------------------------------
drop function if exists fuel_required;
delimiter //
create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40))
	returns integer reads sql data
begin
	if (ip_departure = ip_arrival) then return 0;
    else return (select 1 + truncate(sqrt(power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)), 0) as fuel
		from (select x_coord, y_coord from locations where label = ip_departure) as departure,
        (select x_coord, y_coord from locations where label = ip_arrival) as arrival);
	end if;
end //
delimiter ;

drop procedure if exists fly_drone;
delimiter //
create procedure fly_drone (in ip_id varchar(40), in ip_tag integer, in ip_destination varchar(40))
sp_main: begin



	DECLARE home varchar(40);
	DECLARE curr_location varchar(40);
	DECLARE fuel_needed integer;
	DECLARE space_left integer;
	DECLARE follower_count integer;
	DECLARE curr_tag integer;
    DECLARE max_tag integer;
	DECLARE curr_fuel integer;

	if not exists (select * from drones where tag=ip_tag and id=ip_id) then leave sp_main; end if;

	SET home = (select home_base from delivery_services where id = ip_id);
	SET curr_location = (select hover from drones where id = ip_id and tag = ip_tag);
	SET space_left = (select space from locations where label = ip_destination);
	SET fuel_needed = fuel_required(curr_location, ip_destination) + fuel_required(ip_destination, home);
	SET follower_count = (select count(*) from drones where swarm_id = ip_id and swarm_tag = ip_tag);


	-- -- ensure that the lead drone being flown is directly controlled and owned by the service
	if (ip_id is null) then leave sp_main; end if;
	if ((select flown_by from drones where id = ip_id and tag = ip_tag) is null) then select '2'; leave sp_main; end if;

	-- -- ensure that the destination is a valid location
	if not exists (select * from locations where label = ip_destination) then select '3'; leave sp_main; end if;

    -- -- ensure that the drone isn't already at the location
	if (curr_location = ip_destination) then select '4'; leave sp_main; end if;

    -- -- ensure that the drone/swarm has enough fuel to reach the destination and (then) home base
	-- checking for lead/lone drone
	SET curr_fuel = (select fuel from drones where tag = ip_tag and id = ip_id);
	if (curr_fuel < fuel_needed) then select '5'; leave sp_main; end if;

	-- checking for followers
	SET curr_tag = (select min(tag) FROM drones where swarm_id = ip_id and swarm_tag = ip_tag) ;
	SET max_tag = (select max(tag) FROM drones where swarm_id = ip_id and swarm_tag = ip_tag);

	while (curr_tag is not null and curr_tag <= max_tag) do
		SET curr_fuel = (select fuel from drones where tag = curr_tag and swarm_id = ip_id and swarm_tag = ip_tag);
		if (curr_fuel < fuel_needed) then select '6'; leave sp_main; end if;
		SET curr_tag = (select min(tag) FROM drones WHERE tag > curr_tag and swarm_id = ip_id and swarm_tag = ip_tag);
	end while;

	-- -- ensure that the drone/swarm has enough space at the destination for the flight
	if (space_left < follower_count + 1) then select '7'; leave sp_main; end if;

	update drones set hover = ip_destination where ip_id = drones.id and ip_tag = drones.tag;
	update drones set hover = ip_destination where swarm_id = ip_id and swarm_tag = ip_tag;

	update drones set fuel = (fuel - fuel_required(curr_location, ip_destination)) where tag = ip_tag and id = ip_id;

	SET curr_tag = (select min(tag) FROM drones where swarm_id = ip_id and swarm_tag = ip_tag) ;
	SET max_tag = (select max(tag) FROM drones where swarm_id = ip_id and swarm_tag = ip_tag);

	WHILE (curr_tag is not null and curr_tag <= max_tag) do
		update drones set fuel = (fuel - fuel_required(curr_location, ip_destination)) where tag = curr_tag and id = ip_id;
		SET curr_tag = (select min(tag) FROM drones WHERE tag > curr_tag and swarm_id = ip_id and swarm_tag = ip_tag);
	end while;


end //
delimiter ;

-- [20] purchase_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a restaurant to purchase ingredients from a drone
at its current location.  The drone must have the desired quantity of the ingredient
being purchased.  And the restaurant must have enough money to purchase the
ingredients.  If the transaction is otherwise valid, then the drone and restaurant
information must be changed appropriately.  Finally, we need to ensure that all
quantities in the payload table (post transaction) are greater than zero. */
-- -----------------------------------------------------------------------------
drop procedure if exists purchase_ingredient;
delimiter //
create procedure purchase_ingredient (in ip_long_name varchar(40), in ip_id varchar(40),
	in ip_tag integer, in ip_barcode varchar(40), in ip_quantity integer)
sp_main: begin
	-- ensure that the restaurant is valid
    if not exists (select * from restaurants where ip_long_name = restaurants.long_name) then leave sp_main; end if;
    -- ensure that the drone is valid and exists at the resturant's location
    if not exists (select * from drones join restaurants on hover = location where ip_id = drones.id and ip_tag = drones.tag) then leave sp_main; end if;
	-- ensure that the drone has enough of the requested ingredient
    if not exists (select * from payload where ip_id = payload.id and ip_tag = payload.tag and ip_barcode = payload.barcode and payload.quantity >= ip_quantity) then leave sp_main; end if;
    -- update the drone's payload
    update payload set quantity = quantity - ip_quantity where ip_id = payload.id and ip_tag = payload.tag and payload.barcode = ip_barcode;
    -- update the monies spent and gained for the drone and restaurant
    update drones set sales = sales + (select price * ip_quantity from payload where ip_id = payload.id and ip_tag = payload.tag and ip_barcode = payload.barcode) where ip_id = drones.id and ip_tag = drones.tag;
	update restaurants set spent = spent + (select price * ip_quantity from payload where ip_id = payload.id and ip_tag = payload.tag and ip_barcode = payload.barcode) where ip_long_name = restaurants.long_name;
    -- ensure all quantities in the payload table are greater than zero
    delete from payload where quantity <= 0;
end //
delimiter ;


-- [21] remove_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure removes an ingredient from the system.  The removal can
occur if, and only if, the ingredient is not being carried by any drones. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_ingredient;
delimiter //
create procedure remove_ingredient (in ip_barcode varchar(40))
sp_main: begin
	-- ensure that the ingredient exists
	if not exists (select * from ingredients where ip_barcode = ingredients.barcode) then leave sp_main; end if;
    -- ensure that the ingredient is not being carried by any drones
    if exists (select * from payload where ip_barcode = payload.barcode) then leave sp_main; end if;
    delete from ingredients where ip_barcode = ingredients.barcode;
end //
delimiter ;


-- [22] remove_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a drone from the system.  The removal can
occur if, and only if, the drone is not carrying any ingredients, and if it is
not leading a swarm. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_drone;
delimiter //
create procedure remove_drone (in ip_id varchar(40), in ip_tag integer)
sp_main: begin
	-- ensure that the drone exists
	if not exists (select * from drones where tag=ip_tag and id=ip_id) then leave sp_main; end if;
	if (ip_id is null) then leave sp_main; end if;

    -- ensure that the drone is not carrying any ingredients
	if ((select sum(quantity) from payload where id = ip_id and tag = ip_tag) != 0) then leave sp_main; end if;

	-- ensure that the drone is not leading a swarm
	if exists (select * from drones where swarm_id = ip_id and swarm_tag = ip_tag) then leave sp_main; end if;

	DELETE FROM drones where tag=ip_tag and id=ip_id;
	DELETE FROM payload where tag=ip_tag and id=ip_id;

end //
delimiter ;

-- [23] remove_pilot_role()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a pilot from the system.  The removal can
occur if, and only if, the pilot is not controlling any drones.  Also, if the
pilot also has a worker role, then the worker information must be maintained;
otherwise, the pilot's information must be completely removed from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_pilot_role;
delimiter //
create procedure remove_pilot_role (in ip_username varchar(40))
sp_main: begin
	-- ensure that the pilot exists
    if not exists (select * from pilots where ip_username = pilots.username) then leave sp_main; end if;
    -- ensure that the pilot is not controlling any drones
    if exists (select * from drones where flown_by = ip_username) then leave sp_main; end if;
    -- remove all remaining information unless the pilot is also a worker
    delete from pilots where ip_username = pilots.username;
    if exists (select * from workers where ip_username = workers.username) then leave sp_main; end if;
	delete from work_for where username = ip_username;
	delete from employees where ip_username = employees.username;
    delete from users where ip_username = users.username;
end //
delimiter ;


-- [24] display_owner_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an owner.
For each owner, it includes the owner's information, along with the number of
restaurants for which they provide funds and the number of different places where
those restaurants are located.  It also includes the highest and lowest ratings
for each of those restaurants, as well as the total amount of debt based on the
monies spent purchasing ingredients by all of those restaurants. And if an owner
doesn't fund any restaurants then display zeros for the highs, lows and debt. */
-- -----------------------------------------------------------------------------
create or replace view display_owner_view as
select ro.username, u.first_name, u.last_name, u.address,
count(re.long_name) as num_restaurants,
count(distinct re.location) as num_places, coalesce(max(re.rating),0) as highs,
coalesce(min(re.rating),0) as lows, coalesce(sum(re.spent),0) as debt from restaurant_owners as ro
left join users as u on u.username = ro.username
left join restaurants as re on ro.username = re.funded_by
group by ro.username;


-- [25] display_employee_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an employee.
For each employee, it includes the username, tax identifier, hiring date and
experience level, along with the license identifer and piloting experience (if
applicable), and a 'yes' or 'no' depending on the manager status of the employee. */
-- -----------------------------------------------------------------------------

create or replace view display_employee_view as
select e.username, e.taxID, e.salary, e.hired, e.experience as employee_experience,
 ifnull(p.licenseID, 'n/a') as licenseID, ifnull(p.experience, 'n/a') as piloting_experience,
	case when d.manager = e.username
		then 'Yes'
		else 'No'
	end as manager_status
from employees as e
left join pilots as p on e.username = p.username
left join delivery_services as d on e.username = d.manager;


-- [26] display_pilot_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a pilot.
For each pilot, it includes the username, licenseID and piloting experience, along
with the number of drones that they are controlling. */
-- -----------------------------------------------------------------------------
create or replace view display_pilot_view as
	select username, licenseID, experience, count(hover) as num_drones, count(distinct(hover)) as num_locations
		from pilots left outer join
			(
				select * from drones
				union all
				select a.* from drones a, drones b where a.id = b.swarm_id and a.tag = b.swarm_tag
            ) as double_drones
    on username = flown_by group by username;


-- [27] display_location_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a location.
For each location, it includes the label, x- and y- coordinates, along with the
number of restaurants, delivery services and drones at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_location_view as
select l.label, l.x_coord, l.y_coord, no_of_restaurants, no_of_services, no_of_drones
from locations l
natural join (select label, count(location) as no_of_restaurants from locations lr left outer join restaurants on lr.label = restaurants.location group by lr.label) as temp1
natural join (select label, count(home_base) as no_of_services from locations ls left outer join delivery_services on ls.label = delivery_services.home_base group by ls.label) as temp2
natural join (select label, count(hover) as no_of_drones from locations ld left outer join drones on ld.label = drones.hover group by ld.label) as temp3
group by l.label;

-- [28] display_ingredient_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of the ingredients.
For each ingredient that is being carried by at least one drone, it includes a list of
the various locations where it can be purchased, along with the total number of packages
that can be purchased and the lowest and highest prices at which the ingredient is being
sold at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_ingredient_view as
	-- select iname as 'ingredient_name', hover as 'location', quantity as 'amount_available', price as 'low_price', price as 'high_price' from ingredients natural join payload natural join drones order by ingredient_name, location;
	select tmp1.name as ingredient_name, tmp1.h1 as location, tmp2.amount_available, tmp2.low_price, tmp2.high_price 
	from (select i.barcode as b1, i.iname as name, d.hover as h1 from ingredients i 
	join payload p on p.barcode = i.barcode 
	join drones d on d.id = p.id and p.tag = d.tag group by i.barcode, i.iname, d.hover) as tmp1 
	join (select d1.hover as h2, p1.barcode as b2, sum(quantity) as amount_available, min(price) as low_price, max(price) as high_price from payload p1 join drones d1 on p1.id = d1.id and p1.tag = d1.tag group by d1.hover, barcode) as tmp2
	on tmp1.b1 = tmp2.b2 and tmp1.h1 = tmp2.h2;
	
-- [29] display_service_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a delivery
service.  It includes the identifier, name, home base location and manager for the
service, along with the total sales from the drones.  It must also include the number
of unique ingredients along with the total cost and weight of those ingredients being
carried by the drones. */
-- -----------------------------------------------------------------------------
create or replace view display_service_view as
select s.id, long_name, home_base, manager, total_sales, num_ingredients, total_cost, total_weight
from delivery_services s
left outer join (select id, sum(sales) as total_sales from drones group by id) as d on s.id = d.id
left outer join (select id, count(distinct(p.barcode)) as num_ingredients, sum(quantity*price) as total_cost, sum(weight*quantity) as total_weight from (payload p left outer join ingredients i on p.barcode = i.barcode) group by id) as pi on s.id = pi.id
group by s.id;

/* Returns the usernames of all workers who can be selected as managers for new services */
create or replace view available_as_manager_view as
	select username from workers where username not in (select manager from delivery_services) and username not in (select username from work_for);

/* Returns a list of usernames that can serve as manager for every service */
create or replace view valid_managers_view as
	-- select username, id from work_for as wf where
    -- username not in (select manager from delivery_services) and
    -- username in (select * from workers) and
    -- username not in (select username from work_for as ts where wf.username = ts.username and wf.id != ts.id);
	select username, id from work_for as wf where
    username not in (select manager from delivery_services) and
    username in (select username from employees) and
	username not in (select flown_by from drones where flown_by is not null) and
    username not in (select username from work_for as ts where wf.username = ts.username and wf.id != ts.id);

/* Restaurant View... Just in case I need to add or remove something. */
create or replace view display_restaurant_view as
	select long_name, rating, spent, location, funded_by from restaurants;

/* Returns the id of all services that can be deleted without throwing an error */
create or replace view deletable_services_view as
	select id from delivery_services where id not in (select id from drones);

create or replace view work_for_view as
	select wf.username, wf.id, ifnull(wf.username = ds.manager and wf.id = ds.id, 0) as is_manager, count(dr.flown_by) as drones_flown_for from work_for as wf left outer join delivery_services as ds on ds.manager = wf.username left outer join drones as dr on wf.username = dr.flown_by group by wf.username, wf.id;

/* Returns the usernames of all employees who can be hired and fired */
create or replace view hireable_employees_view as
	select username from employees where username not in (select manager as username from delivery_services where manager is not null union select flown_by as username from drones where flown_by is not null);

-- select * from display_owner_view;
-- select * from display_employee_view;
-- select * from display_pilot_view;
-- select * from display_location_view;
-- select * from display_ingredient_view;
-- select * from display_service_view;
-- select * from available_as_manager_view;
-- select * from deletable_services_view;
-- select * from work_for_view;
-- select * from hireable_employees_view;
-- select * from valid_managers_view;
-- select * from payload;
