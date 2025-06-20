# Azure Log Analyticsを使用して、指定されたKQLで情報を取得し、JSON と CSV ファイルに保存する。
# Parameters:
#   kql_file_name: KQLクエリを含むファイルの名前
#   json_file_name: 結果を保存するJSONファイルの名前
#   csv_file_name: 結果を保存するCSVファイルの名前
#   workspace_id: Log Analytics ワークスペースの ID

import json
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

def lgacommon(req, kql_file_name, json_file_name, csv_file_name, workspace_id):
    # KQL クエリをファイルから読み込む
    with open(kql_file_name, 'r') as f:
        kql_query = f.read()

    # 認証とクライアント作成
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    # クエリ実行
    response = client.query_workspace(
        workspace_id=workspace_id,
        query=kql_query,
        timespan=None
    )

    # クエリ実行
    if response.status == LogsQueryStatus.SUCCESS:
        for table in response.tables:
            columns = table.columns
            rows = table.rows
            df = pd.DataFrame(rows, columns=columns)
            # JSON 保存
            with open(json_file_name, 'w') as f:
                json.dump(df.to_dict(orient='records'), f, indent=2)
            # CSV 保存
            df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')

        response_data = {
            "json_file": json_file_name,
            "csv_file": csv_file_name,
            "data_count": len(df)
        }
        # HTTPステータスコード200を返す
        return {
            "status": 200,
            "body": json.dumps(response_data, ensure_ascii=False)
        }
    #エラーが発生した場合の処理。HTTPステータスコード500を返す。
    else:
        response_data = {
            "error": str(response.status)
        }
        return {
            "status": 500,
            "body": json.dumps(response_data, ensure_ascii=False)
        }