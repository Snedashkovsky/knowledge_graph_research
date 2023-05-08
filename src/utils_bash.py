import logging
from typing import Optional
from cyberutils.bash import execute_bash

from config import CYBERLINK_CREATION_QUERY


def extract_from_console(console_output, keys) -> list[list]:
    console_output = [item.replace(' ', '').split(':') for item in str(console_output).split('\\n')]
    return [[item[0], item[1].split('\\')[0]] for item in console_output if item[0] in keys]


def create_cyberlink(account_name, from_hash, to_hash,
                     query=CYBERLINK_CREATION_QUERY) -> [Optional[str], Optional[str]]:
    try:
        output, error_execute_bash = execute_bash(f'{query} {account_name} {from_hash} {to_hash}')
        if error_execute_bash:
            logging.error(
                f"cyberLink was not created. Account {account_name}, from {from_hash}, to {to_hash}. "
                f"Error {error_execute_bash}")
            return None, error_execute_bash
        rawlog = extract_from_console(output, ['rawlog'])[0][1]
        if rawlog == 'not enough personal bandwidth'.replace(' ', ''):
            logging.info(
                f"cyberLink was not created. Account {account_name}, from {from_hash}, to {to_hash}. Not enough "
                f"personal bandwidth")
            return None, 'not enough personal bandwidth'
        tx_hash = extract_from_console(output, ['txhash'])[0][1]
        logging.info(
            f"cyberLink was created. Account {account_name}, from {from_hash}, to {to_hash}. tx {tx_hash}")
        return tx_hash, None
    except Exception as error_parsing:
        logging.error(
            f"cyberLink was not created. Account {account_name}, from {from_hash}, to {to_hash}. Error {error_parsing}")
        return None, error_parsing


def test_create_cyberlink():
    tx_hash, _ = create_cyberlink('', '', '', query='cat ./tests/create_cyberlink_test')
    assert tx_hash == 'C97489299E9FE23FDE5F85AF85C076D869648577A9EE914E5A0332A6C515DE46'
