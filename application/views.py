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
    balance = current_user.get_balance()
    return render_template('index.html', balance=balance)


@main_bp.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    form = SendForm()
    if form.validate_on_submit():
        current_user.send(form.quantity.data, form.receiver.data, form.note.data)
        return redirect(url_for('main_bp.index'))

    # show the form, it wasn't submitted
    return render_template('send.html', form=form)


@main_bp.route('/transactions')
@login_required
def transactions():
    txns = current_user.get_transactions()

    return render_template('transactions.html', txns=txns)


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
