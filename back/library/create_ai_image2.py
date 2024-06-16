#stable StableDiffusionImg2Img ローカルなら無料

import matplotlib.pyplot as plt
import random
import torch
import pandas as pd
import openpyxl as op
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
from diffusers import StableDiffusionImg2ImgPipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    use_safetensors=True,
    device=device,
).to(device)

# pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5",
#     torch_dtype=torch.float32,
#     use_safetensors=True,
# ).to("cuda")
pipe.enable_attention_slicing()

from resolution_lower import reduce_resolution

def load_and_resize_image(image_path):
   # 画像の読み込み
   image = Image.open(image_path).resize((512, 1024)).convert("RGB") #reduce_resolution を適用したいが、、どうやるん
   return image

def imgToImg(prompt, image_path):
   """
   * パラメータの初期化
   """
   # 推論ステップ数
   num_inference_steps = 5
   guidance_scale = random.uniform(8, 12)
   # ネガティブプロンプト
   n_prompt = "keep the architecture, EasyNegative, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, (worst quality:1.2), low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, lowres graffiti, (low quality lowres simple background:1.1),sketch, painting, cartoon, 3d, anime, drawing,ugly face, unclear eyes, bad mouth, same peoples,no change in buildings, no change in landscape, no change in scenery, no change in buildings"
   # 乱数生成のシード値を設定
   seed = random.randint(1, 1000)
   # シード値を設定
   torch.manual_seed(seed)
   strength = 0.9

   # インプット画像の読み込み
   input_image = load_and_resize_image(image_path)

   # 例外処理
   if input_image is None:
       raise ValueError("インプット画像がありません。'./'に画像[サンプル1.png] or [サンプル2.png]が存在するか確認してください。")

   if input_image is None:
       # エラーハンドリング: input_imageがNoneの場合にエラーを処理する
       return None

   try:
       # 画像の生成
       edit_image = pipe(
           prompt,
           negative_prompt=n_prompt,
           image=input_image,
           num_inference_steps=num_inference_steps,
           strength=strength,
           guidance_scale=guidance_scale,
       ).images[0]

       # タイムスタンプを取得
       timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

       # 画像の保存
       output_image_path = f"./output_{timestamp}.png"
       edit_image.save(output_image_path)

       # 入力画像と出力画像を表示
       plt.figure(figsize=(12, 6))
       plt.subplot(1, 2, 1)
       plt.imshow(input_image)
       plt.title("Input Image")
       plt.axis('off')

       plt.subplot(1, 2, 2)
       plt.imshow(edit_image)
       plt.title("Output Image")
       plt.axis('off')

       plt.show()

       # デバッグ用出力
       print(f"プロンプト: {prompt}")
       print(f"出力画像のパス: {output_image_path}")
       print(f"シード値: {seed}")
       print(f"推論ステップ数: {num_inference_steps}")
       print(f"ガイドスケール: {guidance_scale}")
       print(f"強度: {strength}")
       print("---")

       return output_image_path

   except Exception as e:
       print(e)
       return None
   
from translate_ja2en import translate_2en_text 

prompt = translate_2en_text("ディズニー風に変更して")  #英語の方が精度いい
image_path = "test1_low_res.jpg" # インプット画像を指定する

imgToImg(prompt, image_path)