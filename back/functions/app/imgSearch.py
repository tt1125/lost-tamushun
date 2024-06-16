import json
import logging
import os
from openai import OpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from google.cloud import functions_v1

def img_search(prompt: str, search_service_endpoint, search_service_key, search_index_name, openai_api_key ):
    # OpenAIを使用してベクトルを生成
    client = OpenAI(api_key=openai_api_key)
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
        search_client = SearchClient(
            endpoint=search_service_endpoint,
            index_name=search_index_name,
            credential=AzureKeyCredential(search_service_key)
        )
        
        # OpenAIを使用して検索クエリを生成
        search_word_res = client.chat.completions.create(model="gpt-4o-2024-05-13",
        messages=[
            {
                "role": "user",
                "content": search_query_prompt.format(prompt=prompt)
            }
        ],
        max_tokens=50)
        search_word = search_word_res.choices[0].message.content
        print('search_word: ', search_word)
        
        if search_word == "none":
            return {
                "img_url": "",
                "img_description": "画像の検索に関する質問を入力してください。"
            }

        openai_response = client.embeddings.create(input=search_word, model="text-embedding-ada-002")
        print('openai_response: ', openai_response)
        vector = openai_response.data[0].embedding
        vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=3, fields="vector")

        # Azure Searchでの検索クエリの作成と実行
        search_results = search_client.search(
            search_text=search_word, 
            vector_queries=[vector_query],
            top=1
        )
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
