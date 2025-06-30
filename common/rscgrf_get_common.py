# Azure Resource Graph を使用して、指定されたリソースタイプの情報を取得し、JSON と CSV ファイルに保存する。
# Parameters:
#   req: HTTP リクエストオブジェクト
#   json_file_name: 保存する JSON ファイルのパス
#   csv_file_name: 保存する CSV ファイルのパス
#   resource_type: 取得する Azure リソースのタイプ（例: 'microsoft.compute/virtualmachines'）

import json
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

def rsccommon(req, json_file_name, csv_file_name, resource_type):
    try:
        #KQLクエリの定義
        query = f"Resources | where type == '{resource_type}'"
        # Azure サブスクリプションのリスト
        subscriptions = [
            "6e054861-6086-4cb9-9ebb-3ee2ad50a04f",
            "656fc812-2dc4-4124-978c-6c3d70c63ca4",
            "8f6373c8-1684-4965-b4b4-2a64e6d41d3b"
        ]

        # JSONファイルとCSVファイルの初期化
        with open(json_file_name, 'w') as f:
            f.write('')
        with open(csv_file_name, 'w') as f:
            f.write('')

        # Azureへの認証情報取得
        credential = DefaultAzureCredential()
        # Resource Graph APIにアクセスするためのクライアント（操作用オブジェクト）を作成
        client = ResourceGraphClient(credential)
        #検索対象のサブスクリプションとクエリ（KQL）を指定して、リクエストオブジェクトを作成
        request = QueryRequest(subscriptions=subscriptions, query=query)
        # Resource Graph APIを呼び出して、リソース情報を取得
        response = client.resources(request)

        # 取得したリソース情報をJSONファイルに保存
        with open(json_file_name, 'w') as f:
            json.dump(response.data, f, indent=2)

        # 取得したリソース情報をCSVファイルに保存
        # JSONの0階層目までをCSV化
        df = pd.json_normalize(response.data, max_level=0)
        # 各列をチェックし、dict や list の場合は json.dumps() でダブルクォート形式に
        for col in df.columns:
            df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)
        # CSVファイルに保存
        df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')

        # レスポンスデータの作成
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
    except Exception as e:
        response_data = {
            "error": str(e)
        }
        return {
            "status": 500,
            "body": json.dumps(response_data, ensure_ascii=False)
        }