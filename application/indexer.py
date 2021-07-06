from algosdk.constants import microalgos_to_algos_ratio

from .algod import get_address
from config import get_indexer


def get_transactions(address):
    myindexer = get_indexer()

    response = myindexer.search_transactions_by_address(address)
    txns = []
    for txn in response["transactions"]:
        txn = txn["payment-transaction"]
        txn["amount"] = (txn["amount"] / microalgos_to_algos_ratio)
        txns.append(txn)
    return txns
