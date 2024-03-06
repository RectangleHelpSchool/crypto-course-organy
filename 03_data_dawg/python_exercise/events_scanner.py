from web3 import Web3

NODE_PROVIDER = 'https://eth-mainnet.g.alchemy.com/v2/7s0nlb02rkkhdjj6su89JmyHVFgsm6kW'
APPROVAL_SIGNATURE = Web3.keccak(text='Approval(address,address,uint256)').hex()
TRANSFER_SIGNATURE = Web3.keccak(text='Transfer(address,address,uint256)').hex()
ERC20_APPROVAL_TOPICS_COUNT = 3

NAMED_CONTRACT_ABI = [
    {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}],
     "stateMutability": "view", "type": "function"}
]

TOPIC_SIZE_BYTES = 32


class ERC20EventScanner:
    w3: Web3

    def __init__(self, w3: Web3):
        self.w3 = w3

    @staticmethod
    def _align_eoa(eoa: str) -> str:
        eoa = eoa.replace('0x', '')
        eoa = eoa.rjust(TOPIC_SIZE_BYTES * 2, '0')
        return f'0x{eoa}'

    def get_approvals(
            self,
            approver: str | None = None,
            spender: str | None = None,
            contract: str | None = None,
            start_block: int | str = 'earliest',
            end_block: int | str = 'latest'
    ) -> list:
        events_filter = {
            'fromBlock': start_block,
            'toBlock': end_block,
            'topics': [
                APPROVAL_SIGNATURE,
                self._align_eoa(approver) if approver else None,
                self._align_eoa(spender) if spender else None
            ]
        }
        if contract:
            events_filter['address'] = contract

        approvals = self.w3.eth.get_logs(events_filter)
        return [approval for approval in approvals if
                len(approval['topics']) == ERC20_APPROVAL_TOPICS_COUNT]

    def get_transfers(
            self,
            contract: str | None = None,
            from_address: str | None = None,
            to_address: str | None = None,
            start_block: int | str = 'earliest',
            end_block: int | str = 'latest'
    ) -> list:
        events_filter = {
            'fromBlock': start_block,
            'toBlock': end_block,
            'topics': [
                TRANSFER_SIGNATURE,
                self._align_eoa(from_address) if from_address else None,
                self._align_eoa(to_address) if to_address else None
            ]
        }

        if contract:
            events_filter['address'] = contract

        return self.w3.eth.get_logs(events_filter)
