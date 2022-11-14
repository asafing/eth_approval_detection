from web3 import Web3
import web3._utils.filters as filters
import asyncio
import requests
import json

from web3.contract import ConciseContract


async def get_block_chunk_logs(w3, address, chunk: int):
    print(w3.eth.get_logs({"fromBlock": 0, "toBlock": 9999999, "address": address}))


def test_1():
    alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/EzCaMUftsyJk3sDarB8-hbnirCK4G1TE"
    address = "0x005e20fcf757b55d6e27dea9ba4f90c0b03ef852"
    acc_transactions_req = "https://api.etherscan.io/api?" \
        "module=account&" \
        "action=txlist&" \
        f"address={address}&" \
        "sort=asc&" \
        "apikey=FREVNA4UCC6VZ9VA8CQ99FQREKDVRZK9BN"

    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    if not w3.isConnected():
        raise EthConnecionError(f"Connection to {alchemy_url} failed - try again later.")

    resp = requests.get(acc_transactions_req)
    approval_transactions = []
    for val in json.loads(resp.text)["result"]:
        if val.get('functionName') and val['functionName'][:7] == 'approve':
            approval_transactions.append(val)

    for approval in approval_transactions:
        get_contract_abi_req = "https://api.etherscan.io/api" \
                               "?module=contract" \
                               "&action=getabi" \
                               f"&address={approval['to']}" \
                               "&apikey=FREVNA4UCC6VZ9VA8CQ99FQREKDVRZK9BN"
        abi = json.loads(requests.get(get_contract_abi_req).text)["result"]
        receipt = w3.eth.get_transaction_receipt(approval['hash'])
        token_contract = w3.eth.contract(Web3.toChecksumAddress(approval['to']), abi=abi,
                                         ContractFactoryClass=ConciseContract)
        for log in receipt.logs:
            val = '∞' if '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' else int(log.data, 16)
            name = token_contract.name()
            print(f"approval on {name} on amount of {val}")


test_1()
