# An Algorand Application built using Flask

This project features a demo wallet using Flask and the Algorand Python SDK. It is capable creating and logging into an
account and sending and viewing transactions.

## Warning

This project has not been audited and should not be used in a production environment.

This project has also been built and tested using the Algorand TestNet. If using the MainNet, please ensure all API keys
and passphrases are kept hidden.

I recommend using `python-dotenv` and a `.env` file to avoid accidentally committing any sensitive information.

## Setup

To setup you should create a Python 3 virtual environment and then clone this repository. The packages can then be installed
with:

`pip install -r requirements.txt`

In order to access the algorand network, the easiest way to get started is by creating an account
at https://developer.purestake.io/login. 
The API keys referenced in this project (in files `indexer.py` and `algod.py` should be replaced with your own.
Do note that the number of requests available with this method is limited and sometimes lead to errors if you make too many requests.

To run the repository, simply run `wsgi.py`.