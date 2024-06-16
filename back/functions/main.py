# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app , storage ,firestore

from ai_img.create_img import create_img

initialize_app()


@https_fn.on_call()
def create(req: https_fn.CallableRequest):
    selection = req.data["selections"]
    add_prompt = req.data["add_prompt"]
    file_id = req.data["file_id"]

    # file_id = "test.jpg"
    # selection = "harry_potter"
    # add_prompt = "カメラを持った少年が、魔法の世界に迷い込んでしまった。"

    create_img(file_id , selection , add_prompt)

    return https_fn.Response("ok!")