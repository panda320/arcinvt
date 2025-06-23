from common.sql_truncate_common import truncate_table
from common.sql_insert_common import insert_csv_to_sql

def truncate_table_and_insert(req):
    csv_file_name = '/tmp/csv/rscgrf_get_hybrid_compute_machines.csv'
    sql_server = 'ssdomsqlserver01.database.windows.net'
    database_name = 'ssdomsqldatabase01'
    table_name = 'rscgrf_get_hybrid_compute_machines'
    schema_name = 'azinvt'
    # テーブルをtruncateする
    truncate_table(req, sql_server, database_name, table_name, schema_name)
    
    # CSVファイルをSQL Databaseにインポートする
    insert_csv_to_sql(req, csv_file_name, sql_server, database_name, table_name, schema_name)
    
    return {
        "status": "success",
        "message": f"Data from {csv_file_name} has been inserted into {schema_name}.{table_name}."
    }