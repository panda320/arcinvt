# Azure Log Analytics を使用して、インストールされたソフトウェアの情報を取得し、JSON と CSV ファイルに保存する。
from common.logana_get_common import lgacommon

def lgainstget(req):
    #　KQLファイル名
    kql_file_name = 'kql/logana_get_install_software.kql'

    # JSONファイル名、CSVファイル名
    json_file_name = '/tmp/json/logana_get_install_software.json'
    csv_file_name = '/tmp/csv/logana_get_install_software.csv'

    # Log Analytics ワークスペース ID
    workspace_id = '961d27e0-6fbb-46b1-b205-ca5f255fc4b2'

    # logana_get_common.pyを呼び出す
    return lgacommon(req ,kql_file_name, json_file_name, csv_file_name, workspace_id)