# About 
This is a project triggered from the completion of the Flask Mega Tutorial by Miguel Grinberg. 

The project is simple: a web-app that users can use to get inspiration on what to do on a rainy day, in Dublin AND suggest activities. 

The aim of the project is for me to test my new-learnt Flask skills. 

# Screenshots
![index page](app/static/index.jpg)

# Tech stack
- Flask
- MySQL
- Bootstrap

# Environment Variables
To run this project, you will need to add the following environment variables to your .env file:

MAIL_SERVER
MAIL_PORT
MAIL_USE_TLS
MAIL_USERNAME
MAIL_PASSWORD

# Getting started
## Prerequisites
TBC


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
- [ ] check email works 
- [ ] setup bookmarking system
- [ ] admin for moderation of posts. 
- [ ] form filling for activity does not take into account the <br> 
- [ ] location should be a drop down
- [ ] anonymize config

# Activate the environment
- On Windows: venv\Scripts\activate
- On Linux: source venv/bin/activate



