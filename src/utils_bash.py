from subprocess import Popen, PIPE
import logging
import json
from typing import Optional

from config import CYBERLINK_CREATION_QUERY, BASH_TIMEOUT


def execute_bash(bash_command: str, shell: bool = False,
                 timeout: Optional[int] = BASH_TIMEOUT) -> tuple[Optional[str], Optional[str]]:
    if len(bash_command.split('"')) == 1:
        _bash_command_list = bash_command.split()
    elif len(bash_command.split('"')) == 2:
        _bash_command_list = \
            bash_command.split('"')[0].split() + \
            [bash_command.split('"')[1]]
    elif len(bash_command.split('"')) > 2:
        _bash_command_list = \
            bash_command.split('"')[0].split() + \
            [bash_command.split('"')[1]] + \
            [item for items in bash_command.split('"')[2:] for item in items.split()]
    else:
        return None, f'Cannot split bash command {bash_command}'
    popen_process = Popen([bash_command], stdout=PIPE, shell=shell, text=True) \
        if shell else Popen(_bash_command_list, stdout=PIPE)
    return popen_process.communicate(timeout=timeout)


def get_json_from_bash_query(bash_command: str, shell: bool = False,
                             timeout: Optional[int] = 15) -> Optional[dict]:
    _res, _ = execute_bash(bash_command, shell=shell, timeout=timeout)
    if _res:
        return json.loads(_res.decode('utf8').replace("'", '"'))
    return


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
