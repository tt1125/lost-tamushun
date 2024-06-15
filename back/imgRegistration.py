imgRegistration = func.Blueprint()
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
search_service_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_service_key = os.getenv('SEARCH_SERVICE_KEY')
search_index_name = os.getenv('SEARCH_INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')

# OpenAIのAPIキー設定
client = OpenAI(api_key=openai_api_key)

bp = func.Blueprint()


@imgRegistration.blob_trigger(arg_name="imgRegistration", path="imgs",
                               connection="AzureWebJobsStorage") 
def imgRegistration(myblob: func.InputStream):
    logging.info('Python HTTP trigger function processed a request.')
    myblob_name = myblob.name

    try:
        if not openai_api_key:
            raise ValueError('OpenAI API key is required.')

        # BlobのURL取得
        blob_url = f"https://{storage_account_name}.blob.core.windows.net/imgs/{myblob_name}"
        print(blob_url)
        

        # 1. 画像を説明
        # ChatGPTを使用して画像の説明を生成
        response = response = client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": "この画像を説明してください。"},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": blob_url,
                        "detail": "low"
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
            )
        imgDescription = response.choices[0].message.content
        logging.info('Image Description: %s', imgDescription)

        # 2. 埋め込みの生成
        embedding_response = client.embeddings.create(input=imgDescription,
        model="text-embedding-ada-002")
        embeddings = embedding_response.data[0].embedding

        logging.info('Embeddings: %s', embeddings)

        # 3. Azure AI Searchにベクトルデータを登録
        search_client = SearchClient(
            endpoint=search_service_endpoint,
            index_name=search_index_name,
            credential=AzureKeyCredential(search_service_key)
        )

        # ランダムなIDを生成
        random_index = random.randint(0, 1000)

        documents_to_index = [
            {
                "id": myblob_name,
                "content": imgDescription,
                "vector": embeddings,
                "metaData": {
                    "title": myblob_name,
                    "url": blob_url,
                }
            }
        ]

        logging.info('Documents to Index: %s', documents_to_index)

        res = search_client.upload_documents(documents=documents_to_index)
        logging.info('Upload Documents Result: %s', res)
      
    except Exception as e:
        logging.error(e)
