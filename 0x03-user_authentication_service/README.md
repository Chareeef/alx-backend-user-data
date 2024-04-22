# User Authentication Service

Welcome to the User Authentication Service project! 🎉 As passionate software engineering learners, we're excited to share our knowledge on how to build a robust authentication system using Flask. In this README, we'll cover everything you need to know to get started, from declaring API routes to handling cookies and returning various HTTP status codes.

## Declaring API Routes in Flask

In Flask, API routes are declared using the `@app.route()` decorator. Let's dive into a simple example:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Your login logic here
    return 'Login Successful', 200
```

In this example, we've defined a route `/login` that accepts POST requests and handles the login functionality.

## Getting and Setting Cookies

Cookies are essential for maintaining session state in web applications. In Flask, we can get and set cookies using the `request.cookies` and `response.set_cookie()` methods respectively. Here's how:

```python
from flask import request, make_response

@app.route('/set_cookie')
def set_cookie():
    resp = make_response('Cookie Set!')
    resp.set_cookie('user_id', '12345')
    return resp

@app.route('/get_cookie')
def get_cookie():
    user_id = request.cookies.get('user_id')
    return f'User ID: {user_id}'
```

In this example, we set a cookie named `user_id` with the value `12345` and retrieve it in another route.

## Retrieving Request Form Data

To retrieve form data from a request in Flask, we can use the `request.form` attribute. Here's how:

```python
from flask import request

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    # Your registration logic here
    return 'Registration Successful', 201
```

In this example, we retrieve the username and password from the request form submitted during registration.

## Returning Various HTTP Status Codes

HTTP status codes convey the outcome of an HTTP request. In Flask, we can return different status codes using the `return` statement. Here are a few examples:

```python
from flask import abort

@app.route('/resource/<int:resource_id>')
def get_resource(resource_id):
    if resource_id not in our_database:
        abort(404)  # Not Found
    return our_database[resource_id], 200  # OK
```

In this example, we return a 404 status code if the requested resource is not found in our database.

---

And now, armed with these powerful tools and knowledge, let's embark on an exhilarating journey to craft our very own User Authentication Service! With Flask as our trusty companion, SQLAlchemy as our robust ORM, and our newfound understanding of declaring API routes, managing cookies, retrieving form data, and returning various HTTP status codes, we're well-equipped to tackle any challenge that comes our way. Together, let's infuse our authentication service with creativity, efficiency, and security, ensuring that it not only meets but exceeds the expectations of our users. The adventure awaits, and the possibilities are endless. Let's cook our own User Authentication Service and make it a masterpiece! 🚀🔒
