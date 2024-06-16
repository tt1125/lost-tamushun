# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import os
from firebase_functions import https_fn
from firebase_admin import initialize_app
from app.imgSearch import img_search
from dotenv import load_dotenv

initialize_app()
load_dotenv()

search_service_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_service_key = os.getenv('SEARCH_SERVICE_KEY')
search_index_name = os.getenv('SEARCH_INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')

@https_fn.on_request()
def img_search_trigger(req: https_fn.Request) -> https_fn.Response:
    req_json = req.get_json()
    prompt = req_json.get('prompt')
    res = img_search(prompt, search_service_endpoint, search_service_key, search_index_name, openai_api_key)
    return res