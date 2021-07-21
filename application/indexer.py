from algosdk.constants import microalgos_to_algos_ratio
from algosdk.v2client import indexer


def myindexer():
    """Initialise and return an indexer"""

    algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    # FIXME: Put your API key in
    algod_token = "YOUR API KEY GOES HERE"

    headers = {
        "X-API-Key": algod_token,
    }

    return indexer.IndexerClient("", algod_address, headers)


def get_transactions(address):
    """Returns a list of transactions related to the given address"""

    response = myindexer().search_transactions(address=address)
    txns = []
    for txn in response["transactions"]:
        try:
            sender = txn["sender"]
            fee = txn["fee"]
            txn = txn["payment-transaction"]
            amount = txn["amount"]
            if sender == address:
                # if the current account is the sender, add fee and display transaction as negative
                amount += fee
                amount *= -1
                other_address = txn["receiver"]
            else:
                other_address = sender
            amount /= microalgos_to_algos_ratio
            txns.append({"amount": amount, "address": other_address})
        except KeyError:
            continue
    return txns


def get_assets(address):
    """Returns a list of assets that have been created by the given address"""

    response = myindexer().search_assets(creator=address)
    assets = response["assets"]
    return assets
