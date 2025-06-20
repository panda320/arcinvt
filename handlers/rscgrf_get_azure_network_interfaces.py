#Azure Resource Graph を使用して、Azure Network Interfaces の情報を取得し、JSON と CSV ファイルに保存する。
from common.rscgrf_get_common import rsccommon

def rscazniget(req):
    # JSONファイル名、CSVファイル名
    json_file_name = '/tmp/json/rscgrf_get_azure_network_interfaces.json'
    csv_file_name = '/tmp/csv/rscgrf_get_azure_network_interfaces.csv'
    
    # Resource Type
    resource_type = 'microsoft.network/networkinterfaces'

    # rscgrf_get_common.pyを呼び出す
    return rsccommon(req, json_file_name, csv_file_name, resource_type)

