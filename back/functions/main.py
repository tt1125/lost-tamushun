
import functions_framework

@functions_framework.http
def hello_get(request):
    return "Hello World!"
