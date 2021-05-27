from clickhouse_driver import Client
from dotenv import dotenv_values

CLICKHOUSE_HOST = dotenv_values(".env")['CLICKHOUSE_HOST']
CLICKHOUSE_COMPRESSION = dotenv_values(".env")['CLICKHOUSE_COMPRESSION']
client = Client(host=CLICKHOUSE_HOST, compression=CLICKHOUSE_COMPRESSION)
execute = client.execute

IPFS_HOST = dotenv_values(".env")['IPFS_HOST']

CYBERLINK_CREATION_QUERY = dotenv_values(".env")['CYBERLINK_CREATION_QUERY']

BASH_TIMEOUT = 20
