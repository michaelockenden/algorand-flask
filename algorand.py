import json
from time import sleep

from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import PaymentTxn

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "UBgPas5b2gjVodZbSFFQ64YgnT5P6hN5i4JyE76i"
headers = {
    "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)

status = algod_client.status()
print(json.dumps(status, indent=4))

try:
    params = algod_client.suggested_params()
    print(json.dumps(vars(params), indent=4))
except Exception as e:
    print(e)


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))


passphrase = "noble alter base great hammer alarm gallery reject jeans trial title approve fitness until cigar shine domain burger honey tent clinic crop metal absent reflect"

private_key = mnemonic.to_private_key(passphrase)
my_address = mnemonic.to_public_key(passphrase)
print("My address: {}".format(my_address))

account_info = algod_client.account_info(my_address)
print("Account balance: {} microAlgos".format(account_info.get('amount')))

params = algod_client.suggested_params()
# comment out the next two (2) lines to use suggested fees
params.flat_fee = True
params.fee = 1000
receiver = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"
note = "Hello World".encode()

unsigned_txn = PaymentTxn(my_address, params, receiver, 1000000, None, note)

signed_txn = unsigned_txn.sign(mnemonic.to_private_key(passphrase))
txid = algod_client.send_transaction(signed_txn)
print("Successfully sent transaction with txID: {}".format(txid))


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
    start_round = client.status()["last-round"] + 1;
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


import base64

# wait for confirmation
try:
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
except Exception as err:
    print(err)

print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
print("Decoded note: {}".format(base64.b64decode(
    confirmed_txn["txn"]["txn"]["note"]).decode()))

account_info = algod_client.account_info(my_address)
print("Account balance: {} microAlgos".format(account_info.get('amount')))

