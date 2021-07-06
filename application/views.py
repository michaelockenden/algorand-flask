from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user

from .forms import SendForm

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


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
    if form.validate_on_submit():
        success = current_user.send(form.quantity.data, form.receiver.data, form.note.data)
        print(success)
        return render_template('success.html', success=success)

    # show the form, it wasn't submitted
    return render_template('send.html', form=form)


@main_bp.route('/transactions')
@login_required
def transactions():
    """Displays all transactions from the user"""
    txns = current_user.get_transactions()

    return render_template('transactions.html', txns=txns)


@main_bp.route('/mnemonic')
@login_required
def mnemonic():
    """Displays the recovery passphrase"""
    passphrase = current_user.passphrase
    return render_template('mnemonic.html', passphrase=passphrase)


@main_bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
