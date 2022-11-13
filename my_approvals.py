# 1.
# Approval                       > An event that is logged when an approve function was successful.
# approve(spender, amount)       > Authorize transfers up to the given amount from the caller's tokens by the spender
# transfer(to, amount)           > Moves tokens from the caller's account to an address
# transferFrom(from, to, amount) > Moves tokens from one address to another address
#
# transferFrom moves tokens between 2 accounts, whereas transfer moves tokens from the sender to the recipient
# transferFrom will only work if the amount to transfer from the transfering account has been approved


# 2.
import web3

