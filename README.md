# eth_approval_detection
A simple script to detect all approvals of a public address. \
This script uses a mix of web3py and http requests to etherscan API to achieve quick results.

### Usage
```python3
python my_approvals.py [-h] --address ADDRESS
```

## Testing
For manual testing, comparisons can be done between the output of: \
`python my_approvals.py --address 0x6354c9fb232dc6f7527b4fb51683c07397dfdb4b` \
to the output of [etherscan's similar feature](https://etherscan.io/tokenapprovalchecker?search=0x6354c9fb232dc6f7527b4fb51683c07397dfdb4b&filter=).
