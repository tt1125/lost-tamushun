from firebase_admin import storage, firestore
import os
import asyncio

from .genelate_img import control_net  , img2img  , main
def create_img(file_id, selections, add_prompt):
    bucket = storage.bucket()
    blob = bucket.blob(f"org-imgs/{file_id}")

    # ダウンロード先のファイルパスを設定
    local_filename = f"{file_id}.jpg"

    # ダウンロードしてローカルに保存
    with open(local_filename, "wb") as file_obj:
        blob.download_to_file(file_obj)

    asyncio.run(main(file_id, selections, add_prompt))
    local_filename = f"imgs/{file_id}_gen.jpg"
    blob = bucket.blob(f"gen-imgs/{file_id}")
    blob.upload_from_filename(local_filename)


    file_paths = [
        f"{file_id}.jpg",
        f"imgs/{file_id}_low.jpg",
        f"imgs/{file_id}_gen.jpg",
    ]

    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)


