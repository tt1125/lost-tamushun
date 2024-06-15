import azure.functions as func
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

import json
import logging
import os
from openai import OpenAI

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

# 環境変数の取得
search_service_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
search_service_key = os.getenv('SEARCH_SERVICE_KEY')
search_index_name = os.getenv('SEARCH_INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')


# Azure Search クライアントの初期化
search_client = SearchClient(
    endpoint=search_service_endpoint,
    index_name=search_index_name,
    credential=AzureKeyCredential(search_service_key)
)

client = OpenAI(api_key=openai_api_key)

@app.function_name("imgSearch")
@app.route(route="imgSearch")
def imgSearch(req: func.HttpRequest) -> func.HttpResponse:
      logging.info('Python HTTP trigger function processed a request.')

      req_messages = req.get_json()
      prompt = req_messages.get('prompt')
      # リクエストボディから 最後のチャットのcontent を取得

      if not prompt:
          return func.HttpResponse(
              "parameter 'prompt' is required.",
              status_code=400
          )
      
      search_query_prompt = """
        ## 命令文
        プロンプトが写真の検索に関するものであれば、プロンプトに続くクエリを生成してください。
        プロンプトが写真検索に関するものでない場合は、"none "とだけ返してください。

        以下に例を示す

        ### 例1
        prompt: ピンクの写真を探してください。
        ピンク

        ### 例2
        prompt: Hackzハッカソンとは何ですか。
        none

        ### プロンプト
        prompt: {prompt}
      """

      try:
          # OpenAIを使用して検索クエリを生成
          openai_response = client.chat.completions.create(model="gpt-4o-2024-05-13",
          messages=[
              {
                  "role": "user",
                  "content": search_query_prompt.format(prompt=prompt)
              }
          ],
          max_tokens=50)
          logging.info('OpenAI response: %s', openai_response)
          

          answer = openai_response.choices[0].message.content
          logging.info('Generated search query: %s', answer)
          
          if answer != "none":
            logging.info('Searching for images...')
            response_message = imgSearchResponse(answer)
            response_message_json = json.dumps(response_message, ensure_ascii=False)
            return func.HttpResponse(response_message_json, status_code=200)
            
          else:
            logging.info('No search query generated.')
            response_message = {
                  "img_url": "",
                  "img_description": "画像が見つかりませんでした。",
            }
            logging.info('Response: %s', response_message)
            response_message_json = json.dumps(response_message, ensure_ascii=False)
            return func.HttpResponse(response_message_json, status_code=200)

      except Exception as e:
          logging.error('Error: %s', str(e))
          return func.HttpResponse(f"Error: {str(e)}", status_code=500)

def imgSearchResponse(answer: str):
    try:
        # Azure Search での検索クエリの作成と実行
        search_results = search_client.search(search_text=answer, top=1)
        logging.info('Search Results: %s', search_results)

        # 検索結果の詳細を取得してログに出力
        img_url = None
        img_description = None
        for result in search_results:
            img_url = result['metaData']['url']
            img_description = result['content']
            break
        
        if img_url is None:
            img_url = ""
            img_description = "画像が見つかりませんでした。"
        
        return {
            "img_url": img_url,
            "img_description": img_description,
        }

    except Exception as e:
        logging.error('Error: %s', str(e))
        return None


@app.function_name("blob_trigger")
@app.blob_trigger(arg_name="myblob", path="imgs",
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
