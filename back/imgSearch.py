

import json
import logging
import os
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

# Azure Search クライアントの初期化
search_client = SearchClient(
    endpoint=search_service_endpoint,
    index_name=search_index_name,
    credential=AzureKeyCredential(search_service_key)
)

# Blueprint の登録
bp = func.Blueprint()
client = OpenAI(api_key=openai_api_key)

@bp.route(route="imgSearch", auth_level=func.AuthLevel.ANONYMOUS)
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
      ピンク色

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
          response_message = imgSearchResponse(answer, req_messages)
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

def imgSearchResponse(answer: str, messages: list):
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