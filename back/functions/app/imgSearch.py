import json
import logging
from openai import OpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from google.cloud import functions_v1

def img_search(request, search_service_endpoint, search_service_key, search_index_name, openai_api_key):
    logging.info('Python HTTP trigger function processed a request.')

    req_json = request.get_json()
    prompt = req_json.get('prompt')

    if not prompt:
        return functions_v1.Response(
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
        client = OpenAI(api_key=openai_api_key)
        
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
            response_message = img_search_response(answer, search_service_endpoint, search_service_key, search_index_name)
            response_message_json = json.dumps(response_message, ensure_ascii=False)
            return functions_v1.Response(response_message_json, status_code=200)
          
        else:
            logging.info('No search query generated.')
            response_message = {
                "img_url": "",
                "img_description": "画像が見つかりませんでした。",
            }
            logging.info('Response: %s', response_message)
            response_message_json = json.dumps(response_message, ensure_ascii=False)
            return functions_v1.Response(response_message_json, status_code=200)

    except Exception as e:
        logging.error('Error: %s', str(e))
        return functions_v1.Response(f"Error: {str(e)}", status_code=500)

def img_search_response(answer: str, search_service_endpoint, search_service_key, search_index_name):
    try:
        search_client = SearchClient(
            endpoint=search_service_endpoint,
            index_name=search_index_name,
            credential=AzureKeyCredential(search_service_key)
        )

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
