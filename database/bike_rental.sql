DROP SCHEMA IF EXISTS bike_rental;
CREATE SCHEMA bike_rental;
USE bike_rental;
DROP TABLE IF EXISTS users;

create table users
(
    user_id       int auto_increment,
    f_name     varchar(30),
    l_name varchar(35),
    studentID int(7) NOT NULL,
    password varchar(128) NOT NULL,
    admin_role        bool,
    primary key (user_id),
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

DROP TABLE IF EXISTS bicycle;

create table bicycle
(
    bike_id       int auto_increment,
    bike_type     varchar(20),
    bike_state	  varchar(20) NOT NULL,
    phone_num     varchar(30) NOT NULL,
    rating		  int,
    user_id		 int,
    building_name varchar(50),
    primary key (bike_id),
    constraint fk_users
        foreign key (user_id)
        REFERENCES users(user_id)
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