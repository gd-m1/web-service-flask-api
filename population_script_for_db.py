import random
import requests
from flaskapi import db
from flaskapi.models import User, Post
import settings

roles = ('author', 'editor')
states = ('active', 'inactive', 'deleted')
titles = ('Pfizer', 'Moderna', 'AstraZeneca', 'Sputnik V', 'Johnson & Johnson')

url = "https://fake-data-person.p.rapidapi.com/api/Persons/Get"

headers = {
    'x-rapidapi-host': "fake-data-person.p.rapidapi.com",
    'x-rapidapi-key': settings.x_rapidapi_key
}

for id in range(1, 26):
    response = requests.request("GET", url, headers=headers, params={'id': f'{id}'})
    name = response.json()['firstName']
    last_name = response.json()['lastName']
    email = response.json()['emailAddress']
    role = random.choice(roles)
    state = random.choice(states)

    user = User(name=name, last_name=last_name, email=email, role=role, state=state)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        raise e

for author in range(1, 26):
    title = random.choice(titles)
    description = f'Finally got my first shot of {title}'

    post = Post(title=title, description=description, author=author)
    try:
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        raise e
