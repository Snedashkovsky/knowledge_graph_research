import json
from pprint import pprint
from cyber_sdk.key.mnemonic import MnemonicKey
from cyber_sdk.client.lcd.api.tx import CreateTxOptions
from cyber_sdk.core.graph import MsgCyberlink

from config import WALLET_SEED, bostrom_lcd_client


def create_cls(link_candidates: list, account_seed: str = WALLET_SEED, print_message: bool = False) -> json:
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
            gas=str(200_000 + 40_000 * len(link_candidates))
        )
    )

    _result = json.loads(bostrom_lcd_client.tx.broadcast(_tx).to_json())
    if print_message:
        pprint(_result)
    return _result
