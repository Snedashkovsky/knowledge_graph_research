from clickhouse_driver import Client

CLICKHOUSE_HOST = 'localhost'
COMPRESSION = 'lz4'
client = Client(host=CLICKHOUSE_HOST)
execute = client.execute
