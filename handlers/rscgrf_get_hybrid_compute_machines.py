#Azure Resource Graph を使用して、Hybrid Compute Machines の情報を取得し、JSON と CSV ファイルに保存する。
from common.rscgrf_get_common import rsccommon

def rschbcmget(req):
    # JSONファイル名、CSVファイル名
    json_file_name = '/tmp/json/rscgrf_get_hybrid_compute_machines.json'
    csv_file_name = '/tmp/csv/rscgrf_get_hybrid_compute_machines.csv'
    
    # Resource Type
    resource_type = 'microsoft.hybridcompute/machines'

    # rscgrf_get_common.pyを呼び出す
    return rsccommon(req, json_file_name, csv_file_name, resource_type)
