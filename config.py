from algosdk.v2client import algod
from algosdk.v2client import indexer
from dotenv import dotenv_values


def get_account():
    env = dotenv_values(".env")

    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = env["API_KEY"]
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    return algod_client


def get_indexer():
    env = dotenv_values(".env")

    algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    algod_token = env["API_KEY"]

    headers = {
        "X-API-Key": algod_token,
    }

    indexer_client = indexer.IndexerClient("", algod_address, headers)

    return indexer_client
