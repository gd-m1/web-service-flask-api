# web-service-flask-api

This is a simple web api built with python3 and Flask-RESTful.  
It has 4 methods GET and POST for interacting with a SQlite database.

## Requirements:
* Python 3.9+
* Flask
* Flask-RESTful
* Flask-SQLAlchemy
* marshmallow

## Install
* Create your virtual environment and install the project requirements:
```
pip install -r requirements.txt
```
* Download and install [Postman](https://www.postman.com/).  
* To create a new db file open Python shell in a command-line from the app directory, and enter the following:
```python
from flaskapi import db

db.create_all()
```
* Add some data to your db with population_script_for_db.py. This script grabs fake names and emails from an external API (sign up and subscription required). Go to [Fake Data Person API](https://rapidapi.com/yusufmustu/api/fake-data-person/), get your free API key and place it in settings.py or in your environment variables.
```
python population_script_for_db.py
```

## Run
- Run the application:
```
python run.py
```

## Description
#### GET User /api/users

Returns two fields:  
- total_count - total amount of filtered elements  
- items - paginated elements (offset, limit)  
Parameters:  
- offset - skips number of rows  
- limit - allows to retrieve just a portion of rows  
- order_by - constrains the result into a unique order (name, last_name, email)  
- id - filters by id  
- email - filters by email  
- name_substr - filters by name substring.  

##### Example

Using Postman:  
```
http://localhost:5000/api/users?order_by=name&name_substr=john&limit=1  
```
Using command-line:  
```python
import requests

requests.get('http://localhost:5000/api/users?order_by=name&name_substr=john&limit=1').json()
```
Result:
```json
{
    "items": [
        {
            "email": "johndoe@demo.com",
            "id": 15,
            "last_name": "Doe",
            "name": "John",
            "role": "author",
            "state": "active"
        }
    ],
    "total_count": [
        {
            "email": "johndoe@demo.com",
            "id": 15,
            "last_name": "Doe",
            "name": "John",
            "role": "author",
            "state": "active"
        }
    ]
}
```

#### POST User /api/users

Creates a new user.    
All fields are mandatory and validated with marshmallow.  
Parameters for request:  
- name  
- last_name  
- email  
- role (author or editor)  
- state (active, inactive, deleted)  

##### Example

When pass data with Postman:  
```json
{
    "name" : "John",
    "last_name": "Doe",
    "email": "johndoe@demo.com",
    "role": "author",
    "state": "active"
}
```
When pass data with command-line:  
```python
requests.post('http://localhost:5000/api/users', json={"name" : "John", "last_name": "Doe", "email": "johndoe@demo.com", "role": "author", "state": "active"}).json()
```

#### GET Post /api/posts

Returns two fields:  
- total_count - total amount of filtered elements  
- items - paginated elements (offset, limit)  
Parameters:  
- offset - skips number of rows  
- limit - allows to retrieve just a portion of rows  
- order_by - constrains the result into a unique order (name, last_name, email)  
- author - filters by author    

##### Example

Using Postman:  
```
http://localhost:5000/api/posts?order_by=email&limit=1&author=9
```

Using command-line:  
```python
import requests

requests.get('http://localhost:5000/api/posts?order_by=email&limit=1&author=9').json()
```
Result:
```json
{
    "items": [
        {
            "author": 9,
            "description": "Finally got my first shot of Moderna",
            "id": 10,
            "title": "Moderna"
        }
    ],
    "total_count": [
        {
            "author": 9,
            "description": "Finally got my first shot of Moderna",
            "id": 10,
            "title": "Moderna"
        }
    ]
}
```

#### POST Post /api/posts

Creates a new post.    
All fields are mandatory and validated with marshmallow.  
Parameters for request:  
- title  
- description  
- author - user id  

##### Example

When pass data with Postman:  
```json
{
    "title": "Test",
    "description": "My first post!",
    "author": 1
}
```
When pass data with command-line:  
```python
requests.post('http://localhost:5000/api/posts', json={"title": "Test", "description": "My first post!", "author": 1}).json()
```