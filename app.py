from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import dotenv_values
from algosdk import account, mnemonic

from util import get_account
from forms import SendForm

app = Flask(__name__)
env = dotenv_values(".env")
app.config['SECRET_KEY'] = env['SECRET_KEY']


@app.route('/')
def index():
    algod_client, passphrase = get_account()
    address = mnemonic.to_public_key(passphrase)
    account_info = algod_client.account_info(address)
    balance = account_info.get('amount') / 1000000
    return render_template('index.html', balance=balance, address=address)


@app.route('/send', methods=['GET', 'POST'])
def send():
    form = SendForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('send.html', form=form)
