from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.constants import microalgos_to_algos_ratio
from algosdk.future.transaction import PaymentTxn

from config import get_account


def algod_client():
    return get_account()[0]


def create_account():
    private_key, address = account.generate_account()
    return mnemonic.from_private_key(private_key)


def get_balance():
    algod_client, passphrase = get_account()
    address = mnemonic.to_public_key(passphrase)
    account_info = algod_client.account_info(address)
    balance = account_info.get('amount') / microalgos_to_algos_ratio

    return balance


def get_address():
    algod_client, passphrase = get_account()
    address = mnemonic.to_public_key(passphrase)

    return address


def send_transaction(sender, quantity, receiver, note, sk):

    quantity = int(quantity * microalgos_to_algos_ratio)
    params = algod_client().suggested_params()
    note = note.encode()
    unsigned_txn = PaymentTxn(sender, params, receiver, quantity, None, note)
    signed_txn = unsigned_txn.sign(sk)
    txid = algod_client().send_transaction(signed_txn)

    # wait for confirmation
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)


# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
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


if __name__ == "__main__":
    address = mnemonic.to_public_key("alter alter base great hammer alarm gallery reject jeans trial title approve fitness until cigar shine domain burger honey tent clinic crop metal absent reflect")
    print(address)