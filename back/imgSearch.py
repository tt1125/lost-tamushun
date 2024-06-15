# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(imgSearch) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging

imgSearch = func.Blueprint()


@imgSearch.route(route="imgSearch", auth_level=func.AuthLevel.ANONYMOUS)
def imgSearch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    prompt = req.params.get('prompt')

    if prompt:
        return func.HttpResponse(f"Hello, {prompt}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "parameter 'prompt' is required.",
             status_code=400
        )
    
    
    