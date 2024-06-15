# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app , storage , firestore


initialize_app()


@https_fn.on_call()
def create_img(req: https_fn.CallableRequest):
    # file_id = req.data["fileId"]
    file_id = "bmo.png"
    img_file  = storage.bucket().file(f"org-imgs/{file_id}")
    print(img_file)

    return https_fn.Response("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
