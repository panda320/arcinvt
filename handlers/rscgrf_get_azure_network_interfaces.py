import json
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

def rscazniget(req):
    """
    Azure Resource Graph を使用して、Azure Network Interfaces の情報を取得し、JSON と CSV ファイルに保存する。
    """
    # JSONファイル名、CSVファイル名
    json_file_name = '/tmp/json/rscgrf_get_azure_network_interfaces.json'
    csv_file_name = '/tmp/csv/rscgrf_get_azure_network_interfaces.csv'
    
    # Resource Type、実行クエリ定義
    resource_type = 'microsoft.network/networkinterfaces'
    query = f"Resources | where type == '{resource_type}'"
    
    # サブスクリプション ID を指定（複数可）
    subscriptions = [
        "6e054861-6086-4cb9-9ebb-3ee2ad50a04f",
        "656fc812-2dc4-4124-978c-6c3d70c63ca4",
        "8f6373c8-1684-4965-b4b4-2a64e6d41d3b"
    ]

    # JSONファイルのとCSVファイルの初期化
    with open(json_file_name, 'w') as f:
        f.write('')
    with open(csv_file_name, 'w') as f:
        f.write('')

    # 認証（マネージド ID を使用）
    credential = DefaultAzureCredential()
    client = ResourceGraphClient(credential)

    # クエリの実行
    request = QueryRequest(subscriptions=subscriptions, query=query)
    response = client.resources(request)

    # JSONファイルに保存
    with open(json_file_name, 'w') as f:
        json.dump(response.data, f, indent=2)

    # pandas で整形
    df = pd.json_normalize(response.data)

    # CSVファイルに保存
    df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')

    # レスポンスの生成
    response_data = {
        "message": "Azure Network Interfaces data retrieved successfully.",
        "json_file": json_file_name,
        "csv_file": csv_file_name,
        "data_count": len(df)
    }  
    return {
        "status": 200,
        "body": json.dumps(response_data, ensure_ascii=False)
    }
