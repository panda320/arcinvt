import azure.functions as func
import json
import logging

# /tmpにディレクトリが存在しない場合は作成
import os
if not os.path.exists('/tmp/json'):
    os.makedirs('/tmp/json')
if not os.path.exists('/tmp/csv'):
    os.makedirs('/tmp/csv')

from azure.functions import HttpRequest, HttpResponse

# hadlersのインポート
from handlers.rscgrf_get_azure_virtual_machines import rscazvmget
from handlers.rscgrf_get_azure_network_interfaces import rscazniget
from handlers.rscgrf_get_hybrid_compute_machines import rschbcmget
from handlers.logana_get_install_software import lgainstget
from handlers.sql_refresh_azure_virtual_machines import truncate_table_and_insert as truncate_table_and_insert_vm
from handlers.sql_refresh_azure_network_interfaces import truncate_table_and_insert as truncate_table_and_insert_nif
from handlers.sql_refresh_hybrid_compute_machines import truncate_table_and_insert as truncate_table_and_insert_hyb
from handlers.sql_refresh_install_software import truncate_table_and_insert as truncate_table_and_insert_softinst

app = func.FunctionApp()

# Define the routes for the Azure Functions
@app.route(route="rscgrf_get_azure_virtual_machines", auth_level=func.AuthLevel.FUNCTION)
def rscgrf_get_azure_virtual_machines(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for Azure Virtual Machines.')
    try:
        response = rscazvmget(req)
        return HttpResponse(
            response['body'],
            status_code=response['status'],
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="rscgrf_get_azure_network_interfaces", auth_level=func.AuthLevel.FUNCTION)
def rscgrf_get_azure_network_interfaces(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for Azure Network Interfaces.') 
    try:
        response = rscazniget(req)
        return HttpResponse(
            response['body'],
            status_code=response['status'],
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="rscgrf_get_hybrid_compute_machines", auth_level=func.AuthLevel.FUNCTION)
def rscgrf_get_hybrid_compute_machines(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for Hybrid Compute Machines.')
    try:
        response = rschbcmget(req)
        return HttpResponse(
            response['body'],
            status_code=response['status'],
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="logana_get_install_software", auth_level=func.AuthLevel.FUNCTION)
def logana_get_install_software(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for Log Analytics - Get Install Software.')
    try:
        response = lgainstget(req)
        return HttpResponse(
            response['body'],
            status_code=response['status'],
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="sql_refresh_azure_virtual_machines", auth_level=func.AuthLevel.FUNCTION)
def sql_refresh_azure_virtual_machines(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for SQL Refresh Azure Virtual Machines.')
    try:
        response = truncate_table_and_insert_vm(req)
        if response['status'] == 'success':
            return HttpResponse(
                json.dumps({"200": response['message']}),
                status_code=200,
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="sql_refresh_azure_network_interfaces", auth_level=func.AuthLevel.FUNCTION)
def sql_refresh_azure_network_interfaces(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for SQL Refresh Azure Network Interfaces.')
    try:
        response = truncate_table_and_insert_nif(req)
        if response['status'] == 'success':
            return HttpResponse(
                json.dumps({"200": response['message']}),
                status_code=200,
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="sql_refresh_hybrid_compute_machines", auth_level=func.AuthLevel.FUNCTION)
def sql_refresh_hybrid_compute_machines(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for SQL Refresh Hybrid Compute Machines.')
    try:
        response = truncate_table_and_insert_hyb(req)
        if response['status'] == 'success':
            return HttpResponse(
                json.dumps({"200": response['message']}),
                status_code=200,
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="sql_refresh_install_software", auth_level=func.AuthLevel.FUNCTION)
def sql_refresh_install_software(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for SQL Refresh Install Software.')
    try:
        response = truncate_table_and_insert_softinst(req)
        if response['status'] == 'success':
            return HttpResponse(
                json.dumps({"200": response['message']}),
                status_code=200,
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    