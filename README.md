# Bike Rental System for Mahidol University


### Team members:
- Thanesphol Leerungruang 6380628
- Karan Kumar 6380812
- Naphong Chadha 6380797

## Problem: 
Have you ever tried renting a bike within our campus? It can be annoying right as sometimes you have to wait for the guard then you have to spend time signing up on a sheet just to finally get the key

### Pain Points: 
- We aren’t able to check the availability of the bicycles without actually physically being there 
- We can’t choose which type of bicycle (e.g. Basket Bike, Road Bike, etc.) we want.
- We could get the bad quality bicycles through random picking which could make our cycling experience unsatisfactory
- Waiting for the guard to actually come and give the signup sheet can take a long time.
- Filling in the information everytime when renting the bike is too troublesome and a waste of time

## This has to stop!

### Our solution
 Develop some sort of online system where staffs of university could rent bike conveniently and all they have to do is just simply show up and take their bike away

### Domain: 
Students, Professors, University staffs and Guards who will be managing the bikes rental system which they usually do

### Stakeholders:
- Students
- Professors
- Guards
- University employees

### Roles and responsibilities of each group:
- Students, Professors and Employees: Log in into the system, book and check availability of bicycles on the system online without actually being there.
- Guards: Can check when someone has a booking so they can be ready at the bicycle retrieval place with the keys ready. Additionally they can confirm when someone shows up to pick up the bike or return the bike.

## Features we were able to implement

<b> Note: </b> Guards and normal users will see completely different webpage as they have different features and responsibility interacting with the webapp

- Guards
    - View all bicycles in the database and see their current status, which building they are in and additional info of the user who if its being rented
    - Approve renting when a users request to rent the bike
    - Approve bicycle has been returned
    - Delete bicycle from the database
    - Add a new bicycle to the database
    - Filter the bicycle database by bicycle type, building and their status
- Users (Students and Staff)
    - Obviously creating accounts and being able to login and logout without any issues
    - Users are redirected into the home page when they login
    - The homepage contains the different buildings that they can rent bicycles at in MUIC
    - Users can then go to the renting page either through the navbar of by clicking on the buildings in the home page
    - In the renting page, the users can see all the bicycles and all their info like the bike type and which building they are in
    - The currently rented bikes only contains an ETA time as to when it will be returned in the case that you have a favourite bike!
    - Our UI is also extremely user friendly when renting a cycle and returning the cycle, since they only have to provide their phone number and an ETA return time before being granted permission to rent the cycle

# Database Design 

## E-R Diagram

![er_diagram](/static/IMG_1658A08AABEE-1.jpeg)

This design is what we were able to implement for our database

## Remark testing the website:

The sql files `bike_rental.sql` contains the script that makes our schema while `data.sql` contains the script to preload data into the database. 

Admin cannot be created however we will create one for you to test it with these credentials

```
id: 1234567
password: admin1
```

To test as a user who rents the bike please register the account yourself. 


We hope you enjoy and please be fair on the evaluation :)

