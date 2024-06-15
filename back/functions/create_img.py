import logging
import os
import random
from openai import OpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import azure.functions as func
from dotenv import load_dotenv

load_dotenv()

# 環境変数の取得

search_service_endpoint = os.getenv("SEARCH_SERVICE_ENDPOINT")
search_service_key = os.getenv("SEARCH_SERVICE_KEY")
search_index_name = os.getenv("SEARCH_INDEX_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

bp = func.Blueprint()


@bp.route(route="default_template")
def default_template(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        if not openai_api_key:
            raise ValueError("OpenAI API key is required.")

        # BlobのURL取得
        blob_url = f"https://{storage_account_name}.blob.core.windows.net/imgs/IMG_4415_Original.jpg"
        print(blob_url)

    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Error occurred: " + str(e), status_code=500)

    return func.HttpResponse("Processing completed successfully.", status_code=200)
