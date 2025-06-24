from common.sql_truncate_common import truncate_table
from common.sql_insert_common import insert_csv_to_sql

def truncate_table_and_insert(req):
    csv_file_name = '/tmp/csv/rscgrf_get_azure_network_interfaces.csv'
    sql_server = 'ssdomsqlserver01.database.windows.net'
    database_name = 'ssdomsqldatabase01'
    schema_name = 'azinvt'
    table_name = 'rscgrf_get_azure_network_interfaces'
    # テーブルをtruncateする
    result = truncate_table(req, sql_server, database_name, table_name, schema_name)
    #returnで返ってきたstatusとmessageを受け取る
    if result['status'] == 'error':
        return {
            "status": "error",
            "message": result['message']
        }
    else:
        print(result['message'])
        # CSVファイルをSQL Databaseにインポートする
        result = insert_csv_to_sql(req, csv_file_name, sql_server, database_name, table_name, schema_name)
    # returnで返ってきたstatusとmessageを受け取る
    if result['status'] == 'error':
        return {
            "status": "error",
            "message": result['message']
        }
    else:
        print(result['message'])
    # 成功した場合のメッセージを返す 
    return {
        "status": "success",
        "message": f"Table {schema_name}.{table_name} was truncated and data from {csv_file_name} has been inserted."
    }