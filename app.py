from flask import Flask, render_template, request, redirect, flash
from algosdk.v2client import algod
from algosdk import account, mnemonic

import json

from util import get_account

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    algod_client, passphrase = get_account()
    address = mnemonic.to_public_key(passphrase)
    account_info = algod_client.account_info(address)
    balance = account_info.get('amount') / 1000000
    return render_template('index.html', balance=balance, address=address)


@app.route('/send', methods=['POST'])
def send():
    flash(request.form)
    return redirect('/')
