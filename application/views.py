from flask import Blueprint, render_template, redirect, url_for
from algosdk import mnemonic

from config import get_account
from .forms import SendForm
from .algod import get_balance, send_transaction

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/')
def index():
    balance = get_balance()
    return render_template('index.html', balance=balance)


@main_bp.route('/send', methods=['GET', 'POST'])
def send():
    form = SendForm()
    if form.validate_on_submit():
        send_transaction(int(form.quantity.data), form.receiver.data, form.note.data)
        return redirect(url_for('main_bp.index'))

    # show the form, it wasn't submitted
    return render_template('send.html', form=form)
