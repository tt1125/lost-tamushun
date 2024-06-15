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
    prompt = req_messages[-1].get('content')
    # リクエストボディから 最後のチャットのcontent を取得

    if not prompt:
        return func.HttpResponse(
             "parameter 'prompt' is required.",
             status_code=400
        )
    
    search_query_prompt = """
      ## 命令文
      プロンプトが写真の検索に関するものであれば、プロンプトに続くクエリを生成してください。
      プロンプトが写真の内容に関する質問であれば、"img_question"とだけ返してください。
      プロンプトが写真検索に関するものでない場合は、"none "とだけ返してください。

      以下に例を示す

      ### 例1
      prompt: ピンクの写真を探してください。
      ピンク色 写真

      ### 例2
      prompt: この写真に映るカメラのメーカーは何ですか？
      img_question
      
      ### 例3
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
          rest_messages = removeImgQuestion(req_messages)
          response_message = imgSearchResponse(answer, rest_messages ,req_messages)

        if answer == "img_question":
            logging.info('Image question detected.')
            response_message = normalResponse(req_messages)
        else:
          logging.info('No search query generated.')
          response_message = normalResponse(req_messages)

        logging.info('Response message: %s', response_message)
        
        # リストをJSON形式に変換してレスポンスとして返す
        response_message_json = json.dumps(response_message, ensure_ascii=False)
        
        logging.info('Response message JSON: %s', response_message_json)

        return func.HttpResponse(response_message_json, status_code=200)
        # return func.HttpResponse(img_url, status_code=200)

    except Exception as e:
        logging.error('Error: %s', str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

# messagesからroleがimg_questionのものを省く関数
def removeImgQuestion(messages: list):
    return [m for m in messages if m['role'] != 'img_question']

def imgSearchResponse(answer: str, rest_messages: list, raw_messages: list):
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
        
        logging.info('Image URL: %s', img_url)

        if img_url is None:
            logging.info('No images found.')
            return None

        response_answer = [
            {
                "role": "img_question",
                "content": img_url
            },
            {
                "role": "assistant",
                "content": f"検索結果はこちらです。画像の説明は以下です。{img_description}"
            },
        ]
        logging.info('Answer: %s', response_answer)

        # チャット形式のレスポンスを作成
        raw_messages.append(response_answer)
        return raw_messages

    except Exception as e:
        logging.error('Error: %s', str(e))
        return None

# 画像の内容に関する質問に対する回答を返す関数
def imgQuestionResponse(answer: str, messages: list):
    try:
        if img_url is None:
            logging.info('No images found.')
            return None

        response_answer = {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "検索結果はこちらです。"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                        "detail": "low"
                    },
                },
                {"type": "text", "text": img_description}
            ]
        }
        logging.info('Answer: %s', response_answer)

        # チャット形式のレスポンスを作成
        messages.append(response_answer)
        return messages

    except Exception as e:
        logging.error('Error: %s', str(e))
        return None
    
# 通常の回答を返す関数
def normalResponse(messages: list):
    opneai_response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        max_tokens=300,
    )
    logging.info('OpenAI response----------: %s', opneai_response)
    
    response_message = opneai_response
    return response_message

