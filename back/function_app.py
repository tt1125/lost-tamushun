import azure.functions as func
from http_blueprint import default_template
from imgSearch import imgSearch
from imgRegistration import imgRegistration
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    print("http_triggerhogehoge")
    return default_template(req)
    
@app.route(route="imgSearch")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    return imgSearch(req)
    
@app.blob_trigger(arg_name="myblob", path="imgs",
                               connection="AzureWebJobsStorage") 
def blob_trigger(myblob: func.InputStream):
    return imgRegistration(myblob)
    
