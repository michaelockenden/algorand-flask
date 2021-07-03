from flask import Blueprint, render_template, redirect, url_for
from algosdk import mnemonic

from config import get_account
from .forms import SendForm

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/')
def index():
    algod_client, passphrase = get_account()
    address = mnemonic.to_public_key(passphrase)
    account_info = algod_client.account_info(address)
    balance = account_info.get('amount') / 1000000
    return render_template('index.html', balance=balance, address=address)


@main_bp.route('/send', methods=['GET', 'POST'])
def send():
    form = SendForm()
    if form.validate_on_submit():
        return redirect(url_for('main_bp.index'))

    # show the form, it wasn't submitted
    return render_template('send.html', form=form)
