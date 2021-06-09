from time import sleep
from tqdm.notebook import tqdm

from src.utils_bash import create_cyberlink
from config import CYBER_ACCOUNT_NAME


def create_cl(account_name, from_hash, to_hash, print_message):
    cyberlink_hash, cyberlink_error = \
        create_cyberlink(
            account_name=account_name,
            from_hash=from_hash,
            to_hash=to_hash)
    if cyberlink_error:
        print(f'CyberLink from {from_hash} to {to_hash} was not created, error: {cyberlink_error}')
    elif cyberlink_hash and print_message:
        print(f'CyberLink from {from_hash} to {to_hash} created')


def create_cls(link_candidates, sleep_time=0, print_message=False, account_name=CYBER_ACCOUNT_NAME):
    for link_candidate in tqdm(link_candidates):
        sleep(sleep_time)
        create_cl(account_name=account_name,
                  from_hash=link_candidate[0],
                  to_hash=link_candidate[1],
                  print_message=print_message)
