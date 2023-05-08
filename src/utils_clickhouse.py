from pandas import DataFrame
from os import system

from config import clickhouse_execute


def load_from_ch_to_df(sql_query, columns=None):
    return DataFrame(clickhouse_execute(sql_query), columns=columns)


def upload_to_ch(file_name, dir_url=None, transformation=True, gz=False, file_type='nt',
                 target_table='knowledge_graph_raw'):
    file_url = dir_url + file_name if dir_url else file_name
    if file_type == 'csv':
        insert_query = '''INSERT INTO {0}
                   SELECT
                        '{1}',
                        subject,
                        predicate,
                        object
                   FROM input('index String, subject String, predicate String, object String')
                   FORMAT CSV
                '''.format(target_table, file_name)
    elif file_type == 'nt' and transformation and gz:
        insert_query = '''INSERT INTO {0}
                   SELECT
                        '{1}',
                        subject,
                        object = '' OR object is Null? Null: predicate,
                        object = '' OR object is Null? predicate: object
                   FROM (
                        SELECT
                            replace(subject_, 'http://', '') as subject,
                            replace(predicate_, 'http://', '') as predicate,
                            replace(object_, 'http://', '') as object
                        FROM input('subject_ String, predicate_ String, object_ String') )
                        FORMAT Regexp
                        SETTINGS format_regexp='[<|\"|_](.+?)[\s][<|\"|_](.+?)[\s][<|\"|_](.+?)[\s\.]', 
                        format_regexp_escaping_rule='Escaped'
                '''.format(target_table, file_name)
    elif file_type == 'nt' and transformation:
        insert_query = '''INSERT INTO {0}
                   SELECT
                        '{1}',
                        subject,
                        object = '' OR object is Null? Null: predicate,
                        object = '' OR object is Null? predicate: object
                   FROM (
                        SELECT
                            replace(subject_, 'http://', '') as subject,
                            replace(predicate_, 'http://', '') as predicate,
                            replace(object_, 'http://', '') as object
                        FROM input('subject_ String, predicate_ String, object_ String') )
                        FORMAT Regexp
                        SETTINGS format_regexp='[<|\\"](.+?)[>|\\"] [<|\\"](.+?)[>|\\"] [<|\\"](.+?)[>|\\"]\s\.', 
                        format_regexp_escaping_rule='Escaped'
                '''.format(target_table, file_name)

    elif file_name[-2:] == 'nt':
        insert_query = '''INSERT INTO knowledge_graph_raw
                   SELECT
                        '{0}',
                        subject_,
                        object_ = '' OR object_ is Null? Null: predicate_,
                        object_ = '' OR object_ is Null? predicate_: object_
                   FROM input('subject_ String, predicate_ String, object_ String')
                        FORMAT Regexp
                        SETTINGS format_regexp='([<|\\"].+?[>|\\"])\s([<|\\"].+?[>|\\"])\s([<|\\"].+?[>|\\"])\s\.', 
                        format_regexp_escaping_rule='Escaped'
                '''.format(file_name)
    else:
        print('Unsupported file type')
        return
    insert_query = insert_query.replace('\n', '')

    bash_command = '''cat {0} | clickhouse-client --query "{1}" '''.format(file_url, insert_query)
    if gz:
        bash_command = 'z' + bash_command
    result = system(bash_command)
    if result == 0:
        print(f'{file_name} successfully uploaded')
    else:
        print(f'{file_name} not uploaded, error code {result}')
