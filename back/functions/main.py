import json
import logging
import os
from google.cloud import functions_v1
from dotenv import load_dotenv
from app.imgSearch import img_search

load_dotenv()

# 環境変数の取得
search_service_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_service_key = os.getenv('SEARCH_SERVICE_KEY')
search_index_name = os.getenv('SEARCH_INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')

def img_search_entry_point(request):
    return img_search(request, search_service_endpoint, search_service_key, search_index_name, openai_api_key)
