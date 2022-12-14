DROP SCHEMA IF EXISTS bike_rental;
CREATE SCHEMA bike_rental;
USE bike_rental;
DROP TABLE IF EXISTS users;

create table users
(
    user_id int(7) NOT NULL,
    f_name     varchar(30),
    l_name varchar(35),
    password varchar(128) NOT NULL,
    admin_role        bool,
    primary key (user_id),
    constraint u_users
    unique (user_id)
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
    bike_state	varchar(50) NOT NULL UNIQUE,
    primary key (bike_state)
);

DROP TABLE IF EXISTS bike_type;

create table bike_type
(
    bike_types	varchar(20) NOT NULL UNIQUE,
    primary key (bike_types)
);

DROP TABLE IF EXISTS bicycle;

create table bicycle
(
    bike_id       int auto_increment NOT NULL,
    bike_types     varchar(20),
    bike_state	  varchar(50) DEFAULT 'Available',
    phone_num     varchar(30),
    user_id		 int(7),
    building_name varchar(50),
    last_return_time TIME,
    primary key (bike_id),
    constraint fk_type
		foreign key (bike_types)
        REFERENCES bike_type(bike_types),
    constraint fk_state
		foreign key (bike_state)
        REFERENCES bike_status(bike_state),
    constraint fk_users
        foreign key (user_id)
        REFERENCES users(user_id)
		ON DELETE SET NULL,
	constraint fk_building
		foreign key (building_name)
		REFERENCES building(building_name)
		ON DELETE SET NULL
);