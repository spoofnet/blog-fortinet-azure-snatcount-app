import logging
import json
import datetime

import azure.functions as func

def main(req: func.HttpRequest, message: func.Out[str]) -> func.HttpResponse:
    # Capture to log for debug purposes
    logging.info(req.get_body())
    # Extract Fortinet "clash" value from "dia debug"  output
    snat_clash = str(req.get_body().splitlines()[3]).split("clash=")[1][:-1]

    # Generate unique row key and add SNAT Clash as row
    data = {
        "Value": snat_clash,
        "PartitionKey": "1",
        "RowKey": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # Add as new record in Azure Tables via Function Binding
    message.set(json.dumps(data))
    return func.HttpResponse(snat_clash)