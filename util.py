from dotenv import dotenv_values
from algosdk.v2client import algod
from algosdk import account, mnemonic


def get_account():
    env = dotenv_values(".env")

    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = env["API_KEY"]
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)
    passphrase = env["MNEMONIC"]

    return algod_client, passphrase
