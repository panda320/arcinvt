import azure.functions as func
import datetime
import json
import logging

# /tmpにディレクトリが存在しない場合は作成
import os
if not os.path.exists('/tmp/json'):
    os.makedirs('/tmp/json')
if not os.path.exists('/tmp/csv'):
    os.makedirs('/tmp/csv')

from azure.functions import HttpRequest, HttpResponse
#from azure.functions.decorators import FunctionApp, http_output, http_trigger

from handlers.rscgrf_get_azure_virtual_machines import rscazvmget
from handlers.rscgrf_get_azure_network_interfaces import rscazniget
from handlers.rscgrf_get_hybrid_compute_machines import rschbcmget

app = func.FunctionApp()

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
