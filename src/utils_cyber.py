import json
from pprint import pprint
from cyber_sdk.key.mnemonic import MnemonicKey
from cyber_sdk.client.lcd.api.tx import CreateTxOptions
from cyber_sdk.core.graph import MsgCyberlink

from config import WALLET_SEED, bostrom_lcd_client


def create_cls(link_candidates: list, account_seed: str = WALLET_SEED, print_message: bool = False,
               min_gas_per_tx: int = 200_000, gas_per_link: int = 40_000, max_gas_per_tx: int = 24_000_000) -> json:
    _key = MnemonicKey(
        mnemonic=account_seed
    )
    _wallet = bostrom_lcd_client.wallet(key=_key)
    _wallet.account_number_and_sequence()

    _msgs = [MsgCyberlink(
        _wallet.key.acc_address,
        link_candidate[0],
        link_candidate[1]
    ) for link_candidate in link_candidates]

    _tx = _wallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=_msgs,
            gas_prices="0boot",
            gas=str(min(min_gas_per_tx + gas_per_link * len(link_candidates), max_gas_per_tx))
        )
    )

    _result = json.loads(bostrom_lcd_client.tx.broadcast(_tx).to_json())
    if print_message:
        pprint(_result)
    return _result
