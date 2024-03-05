from dataclasses import dataclass
from argparse import ArgumentParser
from eth_typing import Address
from web3 import Web3

NODE_PROVIDER = 'https://eth-mainnet.g.alchemy.com/v2/7s0nlb02rkkhdjj6su89JmyHVFgsm6kW'
APPROVAL_SIGNATURE = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'
ERC20_APPROVAL_TOPICS_COUNT = 3


@dataclass
class Approval:
    token: str
    amount: str


def get_eoa_address() -> str:
    parser = ArgumentParser()
    parser.add_argument('-a', '--address', type=str, help='EOA address', required=True)
    return parser.parse_args().address


class ApprovalScanner:
    w3: Web3

    def __init__(self, w3: Web3):
        self.w3 = w3

    def _get_transaction(self, eoa: Address) -> None:
        self.w3.eth.get_transaction_count(eoa)

    @staticmethod
    def _align_eoa(eoa: str) -> str:
        leading_zeros = '0' * 24
        return f'0x{leading_zeros}{eoa[2:]}'

    def _get_contract_name(self, address: str) -> str:
        abi = [{"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view", "type": "function"},
               {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view", "type": "function"}]
        contract = self.w3.eth.contract(address, abi=abi)
        return contract.functions.name().call()

    def get_approvals(self, eoa: str) -> list[Approval]:
        raw_approvals = self.w3.eth.get_logs({
            'fromBlock': 'earliest',
            'toBlock': 'latest',
            'topics': [
                APPROVAL_SIGNATURE,
                self._align_eoa(eoa)
            ],
        })

        # The approval signature matches not just the ERC20 approval, but also other approvals,
        # which contain an extra topic. We filter out those approvals.
        raw_approvals = [approval for approval in raw_approvals if
                         len(approval['topics']) == ERC20_APPROVAL_TOPICS_COUNT]

        return [
            Approval(
                token=self._get_contract_name(approval['address']),
                amount=approval['data'].hex()
            )
            for approval in raw_approvals
        ]


def main() -> None:
    w3 = Web3(Web3.HTTPProvider(NODE_PROVIDER))
    eoa = get_eoa_address()
    approval_scanner = ApprovalScanner(w3)

    approvals = approval_scanner.get_approvals(eoa)
    for approval in approvals:
        print(f'approval on {approval.token} on amount of {approval.amount}')


if __name__ == '__main__':
    main()
