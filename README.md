# core-backend
START APP WITH DOCKER:

Preparations:
 -

 - Migrate the DB:

        make make_migrate
        make run_migrate


Start:
 -

 - Build and run

       make build_and_run

 - Run

       make run_app

Additional:
 - 

 - Drop all containers

        make drop_all_containers

 - Create superuser

       make make_super_user

 - Show logs 

       sudo docker logs api
       sudo docker logs db

Poetry:
 - 

 - Load all needed packages

       poetry install

 - Add new package

       poetry add <package_name>


For more commands inspect Makefile
