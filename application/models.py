from algosdk import mnemonic
from algosdk.constants import microalgos_to_algos_ratio
from flask_login import UserMixin

from config import get_account, get_indexer
from .algod import send_transaction, create_asset
from .indexer import get_transactions, get_assets


class User(UserMixin):
    """User account model"""

    algod_client = get_account()
    indexer = get_indexer()

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
        """Returns user balance, in algos converted from microalgos"""
        account_info = self.algod_client.account_info(self.public_key)
        balance = account_info.get('amount') / microalgos_to_algos_ratio

        return balance

    def send(self, quantity, receiver, note):
        """Returns True for a succesful transaction. Quantity is given in algos"""
        return send_transaction(self.public_key, quantity, receiver, note, self.id)

    def create(
            self,
            asset_name,
            unit_name,
            total,
            decimals,
            default_frozen,
            url
    ):
        """Creates an asset, with the user as the creator"""
        return create_asset(
            self.public_key,
            asset_name,
            unit_name,
            total,
            decimals,
            default_frozen,
            url,
            self.id
        )

    def get_transactions(self):
        """Returns a list of the user's transactions"""
        return get_transactions(self.public_key)

    def get_assets(self):
        """Returns a list of the user's assets"""
        return get_assets(self.public_key)
