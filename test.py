from web3 import Web3
from web3.auto import w3


def test_1():
    print(w3.isConnected())
    print(w3.eth.get_block('last'))


test_1()
