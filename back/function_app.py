import azure.functions as func 
from http_blueprint import bp
from imgSearch import bp as img_bp
from imgRegistration import bp as img

app = func.FunctionApp() 

app.register_functions(bp)
app.register_functions(img_bp) 
app.register_functions(img)