# Creating a simple wallet using Flask

In this project we'll go through the steps of putting together a basic Algorand wallet website using Flask.

This wallet will feature:
- Logging in with a 25-word mnemonic
- Creating an account
- Sending transactions
- Viewing all sent/received transactions
- Creating and displaying assets


# Introduction and Setup

Flask is most well known for being able to quickly put together websites, however it is capable of more robust features.
We'll take acheive this by also using Flask-WTF and Flask-Login.

Along with the Python Algorand SDK, our requirements file should look like this:

```text
flask
flask-login
flask-wtf
py-algorand-sdk
```

I also highly recommend using `python-dotenv` to store sensitive information and avoid commiting them to a public repository. Flask also has inbuilt functionality with `python-dotenv`, allowing Flask environment variables to be automatically stored in any `.env` file. However, in this solution I'll put the values in the code, which you can replace.

In order to access the algorand nextwork, you need to be running a node. You can do this yourself but it might be easier to grab an API key from a third party, such as at https://developer.purestake.io/login.

You will need to use a virtual environment to correctly use Flask. This can be done as follows (these commands use Windows):

- Create a directory for your project
- Inside your project directory, type in `py -m venv venv`
- Activate your virtual environment with `.\venv\Scripts\activate`

# Creating the initial Flask application

To begin, first create a file structure as shown:
```bash
└── your_project_name/
    ├── venv/
    ├── your_application_name/
    │    ├── __init__.py
    │    └── views.py
    └── requirements.txt
    └── wsgi.py
```

`requirements.txt` should be filled with the requriements mentioned earlier. This can then be installed with `pip install -r requirements.txt`. Make sure your virtual environment is activated.

The remaining files should be filled out as such:

`__init__.py`:
```python
from flask import Flask

from . import views

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.main_bp)
    return app
```

`views.py`:
```python
from flask import Blueprint

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/')
def index():
    return "Algorand Balance"
```

`wsgi.py`:
```python
from your_application_name import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

This can be run with `flask run`. It is important to note that `flask run` will by default look for a file called `wsgi.py` so don't rename it.

If you haven't used Flask before, this may seem initimidating, and if you have used Flask, you probably know that the same outcome can be acheived with a single `app.py`, written as:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Algorand Balance"
```

The reason we've structured it like this is for a lot more flexiblity. As we start adding more features, a single `app.py` will quickly become overcrowded and hard to use. What we've done is used a Flask Blueprint to seperate components.

Now you might be wondering about the static and template folders mentioned in `views.py`. These are to store the project's CSS and HTML, respectively. We can add these folder as so:

```bash
└── your_project_name/
    ├── venv/
    ├── your_application_name/
    │   ├── static/
    │   │   └── css/
    │   ├── templates/
    │   ├── __init__.py
    │   └── views.py
    ├── requirements.txt
    └── wsgi.py
```

Now create `style.css` inside `css` and `layout.html` inside `templates`.

`style.css`
```css
body {
    margin: 0;
    font-family: helvetica;
    color: black;
}

.container {
    display: flex;
    justify-content: center;
}
.content {
    text-align: center;
    padding: 15px;
    margin: 40px;
    border-radius: 24px;
    background-color: whitesmoke;
    width: 60%;
    position: absolute;
    padding-bottom: 48px;
}
```

`layout.html`
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    <title>Wallet</title>
</head>
<body>
<div class="container">
    <div class="content">
        {% block content %} {% endblock %}
    </div>
</div>
</body>
</html>
```

Flask contains Jinja2, which we can use to add logic to HTML using the curly braces. We can create the `index.html` file which extends from this layout.

`index.html`
```html
{% extends 'layout.html' %}

{% block content %}
<h1>Algorand Balance</h1>
{% endblock %}
```

How this works is that by extending from `layout.html`, the blocks in `index.html` replace the blocks in `layout.html`.

Now in order to display the new index page, we need to render it with Flask.
Replace `views.py` with:

```python
from flask import Blueprint, render_template

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/')
def index():
    return render_template('index.html')
```

Running `flask run` again should now give a page looking like this:

![initial_page](initial.png)

# Interacting with the Algod Client

