# core-backend

Before the start:
 - 

Please, make sure that you have a .env in the root folder. Feel free to specify values of environmental variables
as you wish, but make sure that your .env file structured like .env.example.

Start app with Docker:
 -

Firstly, you need to have Docker installed in your system. 
If you haven't installed Docker yet, visit https://docs.docker.com/get-docker/ .

Secondly, make sure to run commands below as a root user!
You can use `sudo su` command to enter root mode.
(Otherwise, you will receive 

    permission denied while trying to connect to the Docker daemon socket at 
    unix:///var/run/docker.sock: Get "http://...": dial unix /var/run/docker.sock: 
    connect: permission denied


Commands:

 - Build images and run application (use at the first setup to build app's images)

       make build_and_run

 - Run application

       make run_app

Additional:
 - 

 - Drop all containers

        make drop_all_containers

 - Create superuser

       make make_super_user

 - Show logs 

       docker logs api
       docker logs db


Database Migration:
 -

 - Make migrations of the DB:

        make make_migrate

 - Migrate the DB

        make run_migrate



Poetry:
 - 
In this project used poetry environment, more info at https://python-poetry.org/

Commands below will help you ensure that all needed packages are installed in your local environment 
(and you won`t receive any import-related highlights in the IDE).

 - Load all needed packages

       poetry install

 - Add new package

       poetry add <package_name>


For more commands inspect Makefile.
