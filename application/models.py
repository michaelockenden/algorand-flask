from flask_login import UserMixin
from algosdk import account, mnemonic
from algosdk.constants import microalgos_to_algos_ratio

from config import get_account, get_indexer
from .algod import send_transaction
from .indexer import get_transactions


class User(UserMixin):
    """User account model."""

    algod_client = get_account()[0]
    indexer = get_indexer()

    def __init__(self, passphrase):
        self.passphrase = passphrase

    @property
    def id(self):
        return mnemonic.to_private_key(self.passphrase)

    @property
    def public_key(self):
        return mnemonic.to_public_key(self.passphrase)

    def get_balance(self):
        account_info = self.algod_client.account_info(self.public_key)
        balance = account_info.get('amount') / microalgos_to_algos_ratio

        return balance

    def send(self, quantity, receiver, note):
        return send_transaction(self.public_key, quantity, receiver, note, self.id)

    def get_transactions(self):
        return get_transactions(self.public_key)
