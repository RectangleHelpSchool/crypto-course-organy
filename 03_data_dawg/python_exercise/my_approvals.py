from argparse import ArgumentParser
from dataclasses import dataclass
from typing import cast

from eth_typing import Address
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

from events_scanner import ERC20EventScanner

NODE_PROVIDER = 'https://eth-mainnet.g.alchemy.com/v2/7s0nlb02rkkhdjj6su89JmyHVFgsm6kW'


@dataclass
class Approval:
    token: str
    amount: str


def get_eoa_address() -> str:
    parser = ArgumentParser()
    parser.add_argument('-a', '--address', type=str, help='EOA address', required=True)
    return parser.parse_args().address


class ApprovalScanner:
    _w3: Web3
    _event_scanner: ERC20EventScanner

    def __init__(self, w3: Web3):
        self._w3 = w3
        self._event_scanner = ERC20EventScanner(w3)

    def _get_contract_name(self, address: str) -> str:
        contract = self._w3.eth.contract(cast(Address, address), abi=NAMED_CONTRACT_ABI)
        try:
            return contract.functions.name().call()
        except BadFunctionCallOutput:
            return 'Unknown'

    def get_approvals(self, eoa: str) -> list[Approval]:
        raw_approvals = self._event_scanner.get_approvals(approver=eoa)

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
