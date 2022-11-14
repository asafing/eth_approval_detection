# 1.
# Approval                       > An event that is logged when an approve function was successful.
# approve(spender, amount)       > Authorize transfers up to the given amount from the caller's tokens by the spender
# transfer(to, amount)           > Moves tokens from the caller's account to an address
# transferFrom(from, to, amount) > Moves tokens from one address to another address
#
# transferFrom moves tokens between 2 accounts, whereas transfer moves tokens from the sender to the recipient
# transferFrom will only work if the amount to transfer from the transferring account has been approved by the caller
# of the approve(..) function
#
#
# 2.
import json

import requests
from typing import List

from web3 import Web3
from web3.contract import ConciseContract, Contract
import argparse


class EthConnecionError(Exception):
    pass


alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/EzCaMUftsyJk3sDarB8-hbnirCK4G1TE"


def print_approval(contract: Contract, data: str) -> None:
    amount = '∞' if data == '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' else int(data, 16)
    if amount != '∞':
        amount *= 10**(-contract.decimals())
    print(f"approval on {contract.name()} on amount of {amount}")


def print_approvals(approval_transactions: List[dict], w3: Web3) -> None:
    eip20_abi = json.load(open('abi.json'))
    for approval in approval_transactions:
        receipt = w3.eth.get_transaction_receipt(approval['hash'])
        token_contract = w3.eth.contract(Web3.toChecksumAddress(approval['to']), abi=eip20_abi,
                                         ContractFactoryClass=ConciseContract)
        for log in receipt.logs:
            print_approval(token_contract, log.data)


def get_address_approvals(address: str) -> List[dict]:
    acc_transactions_req = "https://api.etherscan.io/api?" \
                           "module=account&" \
                           "action=txlist&" \
                           f"address={address}&" \
                           "sort=asc&" \
                           "apikey=FREVNA4UCC6VZ9VA8CQ99FQREKDVRZK9BN"

    resp = requests.get(acc_transactions_req)
    approval_transactions = []
    for val in json.loads(resp.text)["result"]:
        if val.get('functionName') and val['functionName'][:7] == 'approve':
            approval_transactions.append(val)
    return approval_transactions


def detect_approvals(address: str) -> None:
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    if not w3.isConnected():
        raise EthConnecionError(f"Connection to {alchemy_url} failed - try again later.")

    approval_transactions = get_address_approvals(address)
    print_approvals(approval_transactions, w3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", help="a public address to check approvals for", type=str)
    args = parser.parse_args()
    detect_approvals(args.address)


if __name__ == "__main__":
    main()
