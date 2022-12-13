INSERT INTO bike_status(bike_state) VALUES ('Unavailable');
INSERT INTO bike_status(bike_state) VALUES ('Available');
INSERT INTO bike_status(bike_state) VALUES ('Awaiting Approval');
INSERT INTO bike_status(bike_state) VALUES ('Awaiting Return Approval');
INSERT INTO bike_status(bike_state) VALUES ('Currently Rented');

INSERT INTO bike_type(bike_types) VALUES ('Fitness Bike');
INSERT INTO bike_type(bike_types) VALUES ('BMX Bike');
INSERT INTO bike_type(bike_types) VALUES ('Road Bike');
INSERT INTO bike_type(bike_types) VALUES ('Utility Bike');

INSERT INTO building(building_name) VALUES ('Adithayathorn Building');
INSERT INTO building(building_name,location) VALUES ('Old Building','WHEREVER');
INSERT INTO building(building_name,location) VALUES ('MLC Building','WHEREVER');

INSERT INTO bicycle(bike_types,building_name) VALUES('BMX Bike','Adithayathorn Building');
INSERT INTO bicycle(bike_types,bike_state,building_name) VALUES('Fitness Bike','Unavailable','Adithayathorn Building');
INSERT INTO bicycle(bike_types,bike_state,building_name) VALUES('Road Bike','Currently Rented','Old Building');
INSERT INTO bicycle(bike_types,building_name,last_return_time) VALUES('BMX Bike','Adithayathorn Building','12:50:12');
