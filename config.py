from clickhouse_driver import Client
from dotenv import dotenv_values
import ipfshttpclient
from multiaddr import Multiaddr
from cyber_sdk.client.lcd import LCDClient

CLICKHOUSE_HOST = dotenv_values(".env")['CLICKHOUSE_HOST']
CLICKHOUSE_COMPRESSION = dotenv_values(".env")['CLICKHOUSE_COMPRESSION']
clickhouse_client = Client(host=CLICKHOUSE_HOST)
clickhouse_execute = clickhouse_client.execute

IPFS_HOST = dotenv_values(".env")['IPFS_HOST']
ipfs_client = ipfshttpclient.connect(addr=Multiaddr(IPFS_HOST))

CYBERLINK_CREATION_QUERY = dotenv_values(".env")['CYBERLINK_CREATION_QUERY']

CYBER_ACCOUNT = dotenv_values(".env")['CYBER_ACCOUNT']
CYBER_ACCOUNT_NAME = dotenv_values(".env")['CYBER_ACCOUNT_NAME']
WALLET_ADDRESS = dotenv_values('.env')['WALLET_ADDRESS']
WALLET_SEED = dotenv_values('.env')['WALLET_SEED']

BASH_TIMEOUT = 20

GRAPHQL_URL = 'https://index.euler-6.cybernode.ai/v1/graphql'

bostrom_lcd_client = LCDClient(
    url="https://lcd.bostrom.cybernode.ai/",
    chain_id="bostrom",
)
