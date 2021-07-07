# Creating a demo wallet using Flask

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
    app.config["SECRET_KEY"] = "put any long random string here"
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

Now we should start thinking about getting account information. To do this, we can use the algod client.

Create a new file called `algod.py` inside the `your_application_name` directory.

```python
from algosdk import account, mnemonic
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client import algod

def algod_client():
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "YOUR API KEY GOES HERE"
    headers = {
        "X-API-Key": algod_token,
    }

    return algod.AlgodClient(algod_token, algod_address, headers)

def create_account():
    private_key, address = account.generate_account()
    return mnemonic.from_private_key(private_key)

def get_balance(address):
    account_info = algod_client().account_info(address)
    balance = account_info.get('amount') / microalgos_to_algos_ratio

    return balance
```

This method uses Purestake.io to connect to the algod client. Afer putting in your API key, 
run `passphrase = create_account()` to generate a TestNet account and save the passphrase. Make sure you store this somewhere because we'll be using it a lot before implementing a login system.

Note that we made a helper function to return the algod client whenever. From now on, we'll be calling this function to use the client, so be sure to `algod_client()` and not `algod_client`.

Now we can get the balance of our new account by running `balance = get_balance(mnemonic.to_public_key(passphrase))`. We need to convert the account passphrase into its public key - the address - in order to check the balance.

Note that by default, balance is stored in microAlgos, which is 0.000001 Algos, the unit a wallet would normally display.

You can add more algorand to your account on the TestNet using the [Algorand Dispenser](https://bank.testnet.algorand.network/). 

Let's now bring this value onto our Flask app.

Add the following to `views.py`:

```python
...
from .algod import get_balance
...

def index():
    balance = get_balance("INPUT YOUR TESTNET ADDRESS HERE")
    return render_template('index.html', balance=balance)
```

`index.html`:

```python
{% extends 'layout.html' %}

{% block content %}
<h1>Algorand Balance</h1>
<h1>{{ balance }}</h1>
{% endblock %}
```

Now using `flask run` will display the user's balance


# Sending transactions with the Algod Client

Now that we have a working account balance, the next step should be to implement a way to send some algorands back.
Here we'll also be working with `Flask-WTF` to create forms for these transactions.

We can start by creating a new file `forms.py` inside of `your_application_name`:

```python
from algosdk.constants import address_len, note_max_length
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import InputRequired, Optional, Length, NumberRange

class SendForm(FlaskForm):
    """Form for creating a transaction"""
    quantity = DecimalField(
        'Quantity',
        validators=[InputRequired(), NumberRange(min=0)],
        render_kw={"placeholder": "Quantity to Send"}
    )
    receiver = StringField(
        'Receiver',
        validators=[InputRequired(), Length(min=address_len, max=address_len)],
        render_kw={"placeholder": "Receiver Address"}
    )
    note = StringField(
        'Note',
        validators=[Optional(), Length(max=note_max_length)],
        render_kw={"placeholder": "Note"})
    submit = SubmitField('Send')
```

This provides the some of the parameters neccesary for sending a transaction. WTForms, which is included with Flask-WTF, provides several validators to make our lives easier.
This means we can prevent errors when know will fail before calling the algod client.
`algosdk.constants` gives us the values we need to validate our form.

Under `views.py`, we can add a new route:

```python
from .forms import SendForm

@main_bp.route('/send', methods=['GET', 'POST'])
def send():
    """Provides a form to create and send a transaction"""
    form = SendForm()
    address = "INPUT YOUR TESTNET ADDRESS HERE" # use mnemonic.to_public_key(passphrase)
    sk = "INPUT YOUR PRIVATE KEY HERE" # use mnemonic.to_private_key(passphrase)
    if form.validate_on_submit():
        success = send_txn(address, form.quantity.data, form.receiver.data, form.note.data, sk)
        return render_template('success.html', success=success)

    # show the form, it wasn't submitted
    return render_template('send.html', form=form, address=address)
```

We can add two new HTML files now. Both make use of our previous `layout.html`.

`send.html`

```html
{% extends 'layout.html' %}

{% block content %}
<h1>Send Algorand</h1>
<form action="{{ url_for('main_bp.send') }}" method="post">
    {{ form.csrf_token }}

    {{ form.quantity.label }}
    <br>
    {{ form.quantity }}
    <br>
    {% if form.quantity.errors %}
        <h3>{{ form.quantity.errors[0] }}</h3>
    {% endif %}
    <br>
    {{ form.receiver.label }}
    <br>
    {{ form.receiver }}
    <br>
    {% if form.receiver.errors %}
        <h3>{{ form.receiver.errors[0] }}</h3>
    {% endif %}
    <br>
    {{ form.note.label }}
    <br>
    {{ form.note }}
    <br>
    {% if form.note.errors %}
        <h3>{{ form.note.errors[0] }}</h3>
    {% endif %}
    <br>
    {{ form.submit }}
</form>
<h1>Receive Algorand</h1>
<h2>Your address is:</h2>
<h4>{{ address }}</h4>
{% endblock %}
```

`success.html`

```html
{% extends 'layout.html' %}

{% block content %}
{% if success %}
<h1>Transaction Success</h1>
{% else %}
<h1>Transaction Failed</h1>
{% endif %}
{% endblock %}
```

Here is the CSS I like to use for forms:

```css
input {
    width: 280px;
    padding: 12px;
    margin-bottom: 12px;
    border-radius: 6px;
    border: 2px solid grey;
    box-sizing: content-box;
}

input[type=submit] {
    font-size: 16px;
    font-weight: bold;
    border: 3px solid black;
    border-radius: 6px;
    width: 120px;
    background-color: white;
    color: black;
}

input[type=submit]:hover {
    background-color: darkslategrey;
    color: white;
    cursor: pointer;
}
```

Now if you do `flask run` and add `/send` to the address bar, your page should look like this:

![form](form.png)

You can also add a link from your index with `<h2><a href="{{ url_for('main_bp.send') }}">Send/Receive</a></h2>`

Notice if you try to click submit you will just get an error. We still need to implement actually sending the algorand using the algod client.

We can add to `algod.py`

```python
from algosdk.future.transaction import PaymentTxn

...


def send_transaction(sender, quantity, receiver, note, sk):
    """Create and sign a transaction. Quantity is assumed to be in algorands, not microalgos"""

    quantity = int(quantity * microalgos_to_algos_ratio)
    params = algod_client().suggested_params()
    note = note.encode()
    try:
        unsigned_txn = PaymentTxn(sender, params, receiver, quantity, None, note)
    except Exception as err:
        print(err)
        return False
    signed_txn = unsigned_txn.sign(sk)
    try:
        txid = algod_client().send_transaction(signed_txn)
    except Exception as err:
        print(err)
        return False

    # wait for confirmation
    try:
        wait_for_confirmation(txid, 4)
        return True
    except Exception as err:
        print(err)
        return False


# utility for waiting on a transaction confirmation
def wait_for_confirmation(transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """

    start_round = algod_client().status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = algod_client().pending_transaction_info(transaction_id)
        except Exception as err:
            print(err)
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        algod_client().status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))
```

Now add `from .algod import send_txn` to `views.py`.

You can now test out sending algorand back to the dispenser with the address GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A.
Make sure you have enough funds or the transaction will fail.

# Implementing a Login System with Flask-Login

Before we get too far, we need to structure our code to allow some kind of Login System. Flask-Login can handle the finer details, and we can start by first creating a User class.

Create a new file `models.py` inside of `your_application_name`:

```python
from algosdk import mnemonic
from flask_login import UserMixin

from .algod import get_balance, send_txn

class User(UserMixin):
    """User account model"""

    def __init__(self, passphrase):
        """Creates a user using the 25-word mnemonic"""
        self.passphrase = passphrase

    @property
    def id(self):
        """Returns private key from mnemonic"""
        return mnemonic.to_private_key(self.passphrase)

    @property
    def public_key(self):
        """Returns public key from mnemonic. This is the same as the user's address"""
        return mnemonic.to_public_key(self.passphrase)

    def get_balance(self):
        """Returns user balance, in algos"""
        return get_balance(self.public_key)

    def send(self, quantity, receiver, note):
        """Returns True for a succesful transaction. Quantity is given in algos"""
        return send_txn(self.public_key, quantity, receiver, note, self.id)

```

Normally, when creating a User class, we would also use a database to store account details.
However, this isn't as important when working with blockchain technology.

From inputting a passphrase, we can find the user's public key (address) and private key. We called the private key the user ID so that it will work with some Flask-Login features. 

Notice the functions `get_balance` and `send`, we'll soon be calling these from `views.py` so we no longer need to pass in our address every time.

Next let's quickly create the form will be using to sign in.

```forms.py```
```python
class LoginForm(FlaskForm):
    """Form for logging into an account"""
    passphrase = StringField('25-word Passphrase', validators=[InputRequired()])
    submit = SubmitField('Login')
```

Along with the corresponding HTML.

```login.html```
```html
{% extends 'layout.html' %}

{% block content %}
<h1>Login</h1>
<form action="{{ url_for('auth_bp.login') }}" method="post">
    {{ form.csrf_token }}

    {{ form.passphrase.label }}
    <br>
    {{ form.passphrase }}
    <br><br>
    {{ form.submit }}
</form>
{% with messages = get_flashed_messages() %}
{% if messages %}
<h2>Passphrase not found</h2>
{% else %}
<br><br><br>
{% endif %}
{% endwith %}
<br>
<h2><a href="{{ url_for('auth_bp.signup') }}">Create a Wallet</a></h2>
{% endblock %}
```

Now we can create a new file called `auth.py`. This file will function similarly to `views.py` but it will only handle routes related to user authentication.

```python
from algosdk import mnemonic
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user

from .algod import create_account
from .forms import LoginForm
from .models import User

login_manager = LoginManager()

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Default login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User(passphrase=form.passphrase.data)
            login_user(user)
            return redirect(url_for('main_bp.index'))
        except Exception as err:
            flash(err)
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
```

We are now using a new blueprint, `auth_bp`. This will need to be added to `__init__.py`.

```python
from flask import Flask

from . import auth
from . import views


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "put any long random string here"

    auth.login_manager.init_app(app)

    app.register_blueprint(views.main_bp)
    app.register_blueprint(auth.auth_bp)

    return app
```

The secret key is used to encrpyt browser cookies, making it especially important for storing user information.

Now, we can use Flask-Login to set routes as `login_required`, meaning they can't be accessed without an account. Also, the `current_user` instance is used to retrieve information about the signed in user. Let's now add these into our `views.py`.

```python
from flask_login import login_required, current_user

...

@main_bp.route('/')
@login_required
def index():
    """Main page, displays balance"""
    balance = current_user.get_balance()
    return render_template('index.html', balance=balance)


@main_bp.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    """Provides a form to create and send a transaction"""
    form = SendForm()
    address = current_user.public_key
    if form.validate_on_submit():
        success = current_user.send(form.quantity.data, form.receiver.data, form.note.data)
        return render_template('success.html', success=success)

    # show the form, it wasn't submitted
    return render_template('send.html', form=form, address=address)
```

Before any of this code can run, we need to add two functions to `auth.py`.

```python
@login_manager.user_loader
def load_user(user_id):
    """User load logic"""
    return User(mnemonic.from_private_key(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to login page"""
    return redirect(url_for('auth_bp.login'))
```

`load_user` gathers a user from a given ID. We named the private key our User ID, so here we get a User from a given private key.


`unauthorized` redirects you to the login page if you haven't signed in.

Now finally, try running the code. You should see a login page - put in your passphrase to sign in.
![login](login.png)

## Navigation Bar

Now that we can sign in, we should provide an easy way to sign out. Here I provide the CSS and HTML I used for a navigation bar.

`nav.html`

```python
<nav class="topnav">
    <a href="{{ url_for('main_bp.index') }}" {% if request.path==url_for('main_bp.index') %} class="active"{% endif %}>Balance</a>
    <a href="{{ url_for('main_bp.send') }}" {% if request.path==url_for('main_bp.send') %} class="active"{% endif %}>Send/Receive</a>
    {% if current_user.is_authenticated %}
    <a class="logout" href="{{ url_for('main_bp.logout') }}"> Logout </a>
    {% endif %}
</nav>
```

```css
.topnav {
    background-color: whitesmoke;
    padding: 20px;
    text-align: center;
}

/* Style the links inside the navigation bar */
.topnav a {
    color: black;
    padding: 10px;
    padding-left: 20px;
    padding-right: 20px;
    text-decoration: none;
    border-radius: 6px;
    font-size: 18px;
}

/* Change the color of links on hover */
.topnav a:hover {
    background-color: lightgrey;
    color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
    background-color: darkslategrey;
    color: white;
}

.topnav a.logout {
    background-color: lightcoral;
    color: white;
}
```

You will need to include the nav bar in `layout.html`. 
This can be done by `{% include 'nav.html' %}`.

The logout route also should be defined in `views.py`. 
This route uses `redirect()` to go back to the login page.

```python
from flask import redirect, url_for
from flask_login import logout_user

@main_bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
```

![navbar](navbar.png)

We can now remove our send/receive link from the index.

## Account Creation

We can also add a sign up button, and generate an account in the website. In `auth.py`, add the following:

```python
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Generates a user account and shows its passphrase"""
    passphrase = create_account()
    user = User(passphrase=passphrase)
    login_user(user)
    return render_template('mnemonic.html', passphrase=passphrase)
```

Here we use our earlier function from `algod.py` to generate an account and its passphrase.
Add this link `<h2><a href="{{ url_for('auth_bp.signup') }}">Create a Wallet</a></h2>` to `login.html` to access this route.

However we also need to create `mnemonic.html` this page will display the mnemonic of the created account.

```html
{% extends 'layout.html' %}

{% block content %}
<h1>Your Account Recovery Phrase:</h1>
<br>
<h2>{{ passphrase }}</h2>
<h2>Note this down and keep it secret!</h2>
{% endblock %}
```

I also added a route to this mnemonic from `views.py`. This route instead uses the current account.

```python
@main_bp.route('/mnemonic')
@login_required
def mnemonic():
    """Displays the recovery passphrase"""
    passphrase = current_user.passphrase
    return render_template('mnemonic.html', passphrase=passphrase)
```

Put `<h2><a href="{{ url_for('main_bp.mnemonic') }}">View Recovery Passphrase</a></h2>` on `index.html`

Now, we finished our login system for the website. 
You can now login using a passphrase or create an account and you can then logout when finished.


# Displaying Transactions using the Indexer

