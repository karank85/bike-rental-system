DROP SCHEMA IF EXISTS bike_rental;
CREATE SCHEMA bike_rental;
USE bike_rental;
DROP TABLE IF EXISTS users;

create table users
(
    studentID int(7) NOT NULL,
    f_name     varchar(30),
    l_name varchar(35),
    password varchar(128) NOT NULL,
    admin_role        bool,
    primary key (studentID),
    constraint u_users
    unique (studentID)
);

DROP TABLE IF EXISTS building;

create table building
(
    building_name varchar(50) NOT NULL,
    location varchar(255),
    primary key (building_name)
);

DROP TABLE IF EXISTS bike_status;

create table bike_status
(
	state_id int auto_increment NOT NULL,
    bike_state	varchar(50) NOT NULL UNIQUE DEFAULT 'Available',
    primary key (state_id)
);

DROP TABLE IF EXISTS bike_type;

create table bike_type
(
	type_id int auto_increment NOT NULL,
    bike_types	varchar(20) NOT NULL UNIQUE,
    primary key (type_id)
);

DROP TABLE IF EXISTS bicycle;

create table bicycle
(
    bike_id       int auto_increment NOT NULL,
    bike_types     varchar(20),
    bike_state	  varchar(20) DEFAULT 'Available',
    phone_num     varchar(30),
    rating		  int,
    studentID		 int(7),
    building_name varchar(50),
    primary key (bike_id),
    constraint fk_type
		foreign key (bike_types)
        REFERENCES bike_type(bike_types)
		ON DELETE SET NULL,
    constraint fk_state
		foreign key (bike_state)
        REFERENCES bike_status(bike_state)
		ON DELETE SET DEFAULT,
    constraint fk_users
        foreign key (studentID)
        REFERENCES users(studentID)
		ON DELETE SET NULL,
	constraint fk_building
		foreign key (building_name)
		REFERENCES building(building_name)
		ON DELETE SET NULL,
    constraint check_rating check (rating >= 0 AND rating <= 5)

);

DROP TABLE IF EXISTS guards;

create table guards
(
    guard_id       int auto_increment,
    f_name     varchar(30),
    l_name varchar(35),
    building_name	varchar(50),
    primary key (guard_id),
    constraint fk_buildings
	    foreign key (building_name)
	    REFERENCES building(building_name)
	    ON DELETE SET NULL
);

INSERT INTO bike_status(bike_state) VALUES ('Unavailable');
INSERT INTO bike_status(bike_state) VALUES ('Available');
INSERT INTO bike_status(bike_state) VALUES ('Awaiting Approval');
INSERT INTO bike_status(bike_state) VALUES ('Awaiting Return Approval');
INSERT INTO bike_status(bike_state) VALUES ('Currently Rented');

INSERT INTO bike_type(bike_types) VALUES ('Fitness Bike');
INSERT INTO bike_type(bike_types) VALUES ('BMX Bike');
INSERT INTO bike_type(bike_types) VALUES ('Road Bike');
INSERT INTO bike_type(bike_types) VALUES ('Utility Bike');