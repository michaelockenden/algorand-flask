from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.future.transaction import PaymentTxn

from config import get_account


def algod_client():
    """Initialise and return an algod client"""
    return get_account()


def create_account():
    """Create account and return its mnemonic"""
    private_key, address = account.generate_account()
    return mnemonic.from_private_key(private_key)


def send_transaction(sender, quantity, receiver, note, sk):
    """Create and sign a transaction. Quantity is assumed to be in algorands"""

    quantity = int(quantity * microalgos_to_algos_ratio)
    params = algod_client().suggested_params()
    note = note.encode()
    try:
        unsigned_txn = PaymentTxn(sender, params, receiver, quantity, None, note)
        print("success")
    except Exception as err:
        print(err)
        return False
    signed_txn = unsigned_txn.sign(sk)
    txid = algod_client().send_transaction(signed_txn)

    # wait for confirmation
    try:
        wait_for_confirmation(algod_client(), txid, 4)
        return True
    except Exception as err:
        print(err)
        return False


# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))
