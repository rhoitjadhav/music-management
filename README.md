# Music Management System
Music management system allows user to play, stream, share, upload songs based on the title, artist and album of the song

## Installation
`install.sh` will install all dependencies required to run this application which includes python 3, pip, sqlite database and other required packages which is defined in `requirements.txt`. Additionally it will ask you for the permission to install the pacakges

```
$ ./install.sh
```

## Requirements
Python 3 and pip will be installed via `install.sh` file which is covered in **Installation** section. In ubuntu 18.04 python 3 is built-in package which is already installed in the system

- Ubuntu 18.04
- Python 3.6
- pip 
- Sqlite3 Database

## Run application
In order to run the flask development server execute following command which will starts the server on `http://0.0.0.0:5000`

```
$ ./run.sh
``` 

## Project Structure Overview
The application consists of 5 directories and 6 files along with README.md and .gitignore
- config -> All the application configuration variables are placed in `config.json` file 
- models -> Database connection interface module where Database class contains CRUD functions to querying the database
- routes -> APIs are defined in this module for this application all the APIs are defined in `songs.py` file
- static: -> This folder contains CSS and JS files
- templates -> HTML templates are stored here which are used in views of the application
- app.py -> Entry point of the application
- util.py -> Utilities package module which contains random string generation function. Additionally it also contains copy/delete/rename files and folder depending on the use case of the application 
- install.sh -> This shell file will install all the packages and modules required to run the application
- run.sh -> Runs the flask server 
- schema.sql -> Sqlite Database schema file
- requirement.txt -> Python packages and dependencies file


## Security Measurements
In order to secure the application there are few measurements that need to be taken care of, such measurements are:

1. Token based authentication
    - It is the process where the user sends his credentials to the server, server will validate the user details and generate a token which is sent as response to the users, and user store the token in client side, so client do further HTTP call using this token which can be added to the header and server validates the token and send a response to the particular api request

2. Rate Limiter
    - It is the number of api calls an app or user can make within a given time period. If this limit is exceeded or if CPU or total time limits are exceeded the user will get an error and the request gets failed

3. SQL Injection
    - SQL Injection is an attack when we ask for a user to input something such as userid/username instead of typing this user gives an SQL statement that will run on database server

