[![Build Status](https://travis-ci.org/brayovsky/yolo.svg?branch=develop)](https://travis-ci.org/brayovsky/yolo)

# yolo
Yolo is an app that provides an API for storing and managing bucketlists and a user interface for doing the same.

The building blocks are:

* Python 3 - Flask microframework
* Docopts

## Setting Up for Development
* Prepare directory for project code and virtualenv:

        $ mkdir -p ~/yolo
        $ cd ~/yolo
        
* Prepare virtual environment

        $ virtualenv --python=python3 venv
        $ source venv/bin/activate
        
* Check out project code:

        $ git clone https://github.com/brayovsky/yolo.git
        
* Install requirements into virtualenv:

        $ pip install -r yolo/requirements.txt
        
 * Create the database for the project. You can use whichever database you prefer e.g postgres, mysql etc.
 
 * Add the type of database and it's uri you have created as an environment variables `YOLO_DB` and `YOLO_DATABASE_URL` respectively.
 
 * Add a secret key for the flask app as an environment variable named `YOLO_SECRET_KEY`.
 
 * Run database migrations.
     
        $ python manage.py db init
        $ python manage.py db migrate
        
 * Run the application.
 
        $ python manage.py runserver
        
  The app should run normally at `127.0.0.1:5000`.
  
  To manually create database tables, run:
  
        $ python manage.py create_database
        
  and to remove the tables run:
  
        $ python manage.py drop_database
        
        
 ## API
 
 The API endpoints are:
* `POST /auth/login` - Log in
* `POST /auth/register` - Register
* `POST /bucketlists/` - Create bucketlist
* `GET /bucketlists/` - Retrieve bucketlists
* `GET /bucketlists/<id>` - Retrieve a specific bucketlist
* `PUT /bucketlists/<id>` - Edit a bucketlist
* `DELETE /bucketlists/<id>` - Delete a bucketlist
* `POST /bucketlists/<id>/items/` - Create items in a bucketlist
* `PUT /bucketlists/<id>/items/<item_id>` - Edit an item in a bucketlist
* `DELETE /bucketlists/<id>/items/<item_id>` - Delete an item in a bucketlist
 
