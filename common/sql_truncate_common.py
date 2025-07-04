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
     try:
         cursor.execute(sql)
         conn.commit()
         return {
             "status": "success",
             "message": f"Table {schema_name}.{table_name} has been truncated."
         }
     except Exception as e:
         conn.rollback()
         return {
             "status": "error",
             "message": str(e)
         }
     finally:
         cursor.close()
         conn.close()