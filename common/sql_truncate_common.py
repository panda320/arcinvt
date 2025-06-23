# 指定されたをAzure SQL Databaseのテーブルをtruncateするための関数
# Parameters:
#   SQL Server名: Azure SQLのサーバー名
#   database_name: データベース名
#   table_name: データを挿入するテーブル名
#   schema_name: スキーマ名
#   ODBC Driver 18 for SQL Serverが必要
import pyodbc

#ODBC Driver
odbc_driver = 'ODBC Driver 18 for SQL Server'

# 指定されたをAzure SQL Databaseのテーブルをtruncateするための関数
def truncate_table(req, sql_server, database_name, table_name, schema_name):
     conn_str = f'DRIVER={{{odbc_driver}}};SERVER={sql_server};DATABASE={database_name};Authentication=ActiveDirectoryMsi;'
     conn = pyodbc.connect(conn_str)
     cursor = conn.cursor()
     sql = f"TRUNCATE TABLE {schema_name}.{table_name}"
     cursor.execute(sql)
     conn.commit()
     cursor.close()
     conn.close()

'''
#truncate_tableの実行test
sql_server = 'ssdomsqlserver01.database.windows.net'
database_name = 'ssdomsqldatabase01'
table_name = 'rscgrf_get_hybrid_compute_machines'
schema_name = 'azinvt'
#truncate_table(sql_server, database_name, table_name, schema_name)
'''