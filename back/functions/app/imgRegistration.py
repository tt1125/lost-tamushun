
import logging
import firebase_admin
from firebase_admin import credentials, storage
from openai import OpenAI
from datetime import timedelta
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

def imgRegistration(file_path, search_service_endpoint, search_service_key, search_index_name, openai_api_key):
    # OpenAIのAPIキー設定
    client = OpenAI(api_key=openai_api_key)
    try:
        if not openai_api_key:
            raise ValueError('OpenAI API key is required.')
        
        storage_url = get_image_url(file_path)
        file_name = file_path.split("/")[-1]
        print("storage_url:", storage_url)
        

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
                        "url": storage_url,
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

        documents_to_index = [
            {
                "id": file_name,
                "content": imgDescription,
                "vector": embeddings,
                "metaData": {
                    "title": file_name,
                    "url": storage_url,
                }
            }
        ]

        logging.info('Documents to Index: %s', documents_to_index)

        res = search_client.upload_documents(documents=documents_to_index)
        logging.info('Upload Documents Result: %s', res)
      
    except Exception as e:
        logging.error(e)



def get_image_url(file_path):
    # ストレージバケットの参照を取得
    bucket = storage.bucket()

    # 画像ファイルのブロブを取得
    blob = bucket.blob(file_path)

    # 画像ファイルの公開URLを取得
    image_url = blob.generate_signed_url(version="v4", expiration=timedelta(hours=1), method='GET')
    
    return image_url