# About 
This is a project triggered from the completion of the Flask Mega Tutorial by Miguel Grinberg. 

The project is simple: a web-app that users can use to get inspiration on what to do on a rainy day, in Dublin. Users can also suggest activities. 

The aim of the project is for me to test my new-learnt Flask skills. 

# Features
- Authentication
    - User registration 
    - User password reset 
    - User login
    - User logout
- Public
    - 7-day weather forecast
    - Display of the 5-latest activities posted
- Members
    - Lists of activities
    - Filter through activities, by location
    - Users can suggest activities
    - User can edit and delete activities they have posted
    - Users can edit their profile
    - users can save and remove activities for later
    - Users can see their 'save for later list'
    - Users can see the activities they have posted
- Administration
    - User management: list users, edit users, delete users, make user admin
    - activity management: list, edit, delete, moderate / publish all activities




# Screenshots
![index page](app/static/index.jpg)

# Tech stack
- Flask
- MySQL
- Bootstrap

# Requirements
Install requirements with 
```
pip install -r requirements.txt
```

# Environment Variables
To run this project, you will need to add the following environment variables to your .env file:

- MAIL_SERVER
- MAIL_PORT
- MAIL_USE_TLS
- MAIL_USERNAME
- MAIL_PASSWORD

# Notes
## To update the database
```
>>> flask db migrate -m "comment"
>>> flask db upgrade
```

## To add to the database
```
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit()
```

## Query the database
```
# return all users
>>> users = User.query.all()
>>> users
[<User john>, <User susan>]
>>> for u in users:
...     print(u.id, u.username)
...
```

```
# get all posts written by a user
>>> u = User.query.get(1)
>>> u
<User john>
>>> activities = u.activities.all()
>>> activities
```

``` 
# print post author and body for all posts
>>> activities = Activity.query.all()
>>> for p in activities:
...     print(p.id, p.author.username, p.body)
...
```

```
# erase all users and activities
>>> users = User.query.all()
>>> for u in users:
...     db.session.delete(u)
...
>>> activities = Activity.query.all()
>>> for p in activities:
...     db.session.delete(p)
...
>>> db.session.commit()
```

# flask shell
flask shell

# To run the app:
flask run 

# Contact 
toie -at- duck -dot- com


# Roadmap
- [x] anonymize config for GitHub
- [x] Weather forecast: simple 7 day forecast
- [x] Location should be a drop down 
- [x] Redo location by using database table
- [x] Setup bookmarking system (save for later) // save for later working 
- [x] Form filling for activity does not take into account formatting  
- [x] Activity page: description of the activity, along with all the relevant info (map, pricing, contact details, expiration)
- [x] Style forms 
- [x] Admin user 
    - [x] for user management
        - [x] see all profiles
        - [x] edit all users profiles
        - [x] make user admin
        - [x] delete user and attached posts (and bookmarked items by said user)
    - [x] For post management
        - [x] edit any activity 
        - [x] delete any activity 
    - [x] moderation of posts before they go live
- [x] Filters: to filter through the ideas, based on the location
- [ ] Make live
- [ ] Check email works 

# Activate the environment
- On Windows: venv\Scripts\activate
- On Linux: source venv/bin/activate



