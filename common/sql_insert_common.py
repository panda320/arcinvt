# 指定されたcsvファイルをAzure SQL Databaseにインポートするための関数
# Parameters:
#   csv_file_name: インポートするCSVファイルのパス
#   SQL Server名: Azure SQLのサーバー名
#   database_name: データベース名
#   table_name: データを挿入するテーブル名
#   schema_name: スキーマ名
#   ODBC Driver 18 for SQL Serverが必要
import pyodbc
import csv

#ODBC Driver
odbc_driver = 'ODBC Driver 18 for SQL Server'

def insert_csv_to_sql(req, csv_file_name, sql_server, database_name, table_name, schema_name):
     conn_str = f'DRIVER={{{odbc_driver}}};SERVER={sql_server};DATABASE={database_name};Authentication=ActiveDirectoryMsi;'
     conn = pyodbc.connect(conn_str)
     cursor = conn.cursor()
     cursor.fast_executemany = True
     with open(csv_file_name, 'r', encoding='utf-8') as f:
         reader = csv.reader(f)
         columns = next(reader)
         placeholders = ','.join(['?'] * len(columns))
         sql = f"INSERT INTO {schema_name}.{table_name} VALUES ({placeholders})"
         data = list(reader)
         cursor.executemany(sql, data)
         conn.commit()
     cursor.close()
     conn.close()

'''
#insert_csv_to_sqlの実行test
csv_file_name = '/tmp/csv/rscgrf_get_hybrid_compute_machines.csv'
sql_server = 'ssdomsqlserver01.database.windows.net'
database_name = 'ssdomsqldatabase01'
table_name = 'rscgrf_get_hybrid_compute_machines'
schema_name = 'azinvt'
#insert_csv_to_sql(csv_file_name, sql_server, database_name, table_name, schema_name)
'''