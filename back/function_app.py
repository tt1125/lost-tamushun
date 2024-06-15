import azure.functions as func
from http_blueprint import default_template
from imgSearch import imgSearch
from imgRegistration import imgRegistration
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    print("http_triggerhogehoge")
    return default_template(req)
    
