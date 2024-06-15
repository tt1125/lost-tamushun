import json
import logging
import os
from google.cloud import functions_v1
from dotenv import load_dotenv
from app.imgSearch import img_search

from firebase_functions import https_fn
from firebase_admin import initialize_app , storage , firestore


# 環境変数の取得
search_service_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_service_key = os.getenv('SEARCH_SERVICE_KEY')
search_index_name = os.getenv('SEARCH_INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')


@https_fn.on_call()
def create_img(req: https_fn.CallableRequest):
    # file_id = req.data["fileId"]
    file_id = "bmo.png"
    img_file  = storage.bucket().file(f"org-imgs/{file_id}")
    print(img_file)

    return https_fn.Response("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
