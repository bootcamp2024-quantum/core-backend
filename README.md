# core-backend
START APP WITH DOCKER:

Preparations:
 -
 - Change current directory:
 
        cd api

 - Migrate the DB:

        python manage.py makemigrations 
        python manage.py migrate


Start:
 -

 - Build and run

       sudo docker-compose up -d --build

Additional:

 - Drop all containers

        sudo docker-compose down -v --remove-orphans


 - Create superuser

       sudo docker-compose exec api python manage.py createsuperuser

 - Show logs 

       sudo docker logs atlas_api
       sudo docker logs atlas_db

 - Load all needed packages

       poetry install

 - Add new package

       poetry add <package_name>