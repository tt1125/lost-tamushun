import asyncio
import base64
from pathlib import Path

from boilerplate import API

from novelai_api.ImagePreset import (
    ImageGenerationType,
    ImageModel,
    ImagePreset,
    ControlNetModel,
)

from translate_ja2en import translate_2en_text

from resolution_lower import reduce_resolution

from prompt_pattern import convert_to_prompt

async def control_net():
    d = Path("results")
    d.mkdir(exist_ok=True)

    async with API() as api_handler:
        api = api_handler.api
        reduce_resolution(d / "test1.jpg", d / "test1_low_res.jpg", 4) # 画像の解像度を下げる
        image = base64.b64encode((d / "test1_low_res.jpg").read_bytes()).decode()

        controlnet = ControlNetModel.Palette_Swap
        _, mask = await api.low_level.generate_controlnet_mask(controlnet, image)

        model = ImageModel.Anime_Full

        preset = ImagePreset.from_default_config(model)
        preset.controlnet_model = controlnet
        preset.controlnet_condition = base64.b64encode(mask).decode()
        preset.controlnet_strength = 1.8
        preset.steps = 5

        from prompt_pattern import convert_to_prompt
        prompt_text = convert_to_prompt("disney")#何風にするか
        additional_text = translate_2en_text("彼は手にカメラを持ち、美しい風景を撮影しています。")#以下に追加の指示文(日本語)を追加
        # full_prompt_text = prompt_text + additional_text
        full_prompt_text = "movie joker comic"

        # NOTE: for some reasons, the images with controlnet are slightly different 
        async for _, img in api.high_level.generate_image(
            full_prompt_text,
            model,
            preset,
            ImageGenerationType.IMG2IMG,
        ):
            (d / "image_with_controlnet1.png").write_bytes(img)

# async def control_net():
#     d = Path("results")
#     d.mkdir(exist_ok=True)
#     # reduce_resolution(d / "test.jpg", d / "test_low_res.jpg", 4) # 画像の解像度を下げる

#     async with API() as api_handler:
#         api = api_handler.api
#         image = base64.b64encode((d / "test_low_res.jpg").read_bytes()).decode()

#         controlnet = ControlNetModel.Form_Lock
#         _, mask = await api.low_level.generate_controlnet_mask(controlnet, image)

#         model = ImageModel.Anime_Curated

#         preset = ImagePreset.from_default_config(model)
#         preset.controlnet_model = controlnet
#         preset.controlnet_condition = base64.b64encode(mask).decode()
#         preset.controlnet_strength =  1.8  #元の画像の影響の強さ
#         preset.steps = 8 # 画像生成のステップ数(デフォルトは28くらい)10は欲しい

#         from prompt_pattern import convert_to_prompt
#         prompt_text = convert_to_prompt("harry_potter")#何風にするか
#         additional_text = translate_2en_text("彼は手にカメラを持ち、美しい風景を撮影しています。")#以下に追加の指示文(日本語)を追加
#         full_prompt_text = prompt_text + additional_text

#         # NOTE: for some reasons, the images with controlnet are slightly different
#         async for _, img in api.high_level.generate_image( # 画像生成の指示文（英語）
#             prompt_text,
#             model,
#             preset,
#         ):
#             (d / "image_with_controlnet1.ssss.png").write_bytes(img)

async def img2img():
    d = Path("results")
    d.mkdir(exist_ok=True)
    reduce_resolution(d / "test1.jpg", d / "test1_low_res.jpg", 4) # 画像の解像度を下げる
    image = base64.b64encode((d / "test1_low_res.jpg").read_bytes()).decode()

    async with API() as api_handler:
        api = api_handler.api

        image = base64.b64encode((d / "test1_low_res.jpg").read_bytes()).decode()

        model = ImageModel.Anime_Full
        # controlnet = ControlNetModel.Scribbler

        preset = ImagePreset.from_default_config(model)
        preset.noise = 0.5
        # note that steps = 28, not 50, which mean strength needs to be adjusted accordingly
        preset.strength = 1.7
        preset.image = image
        preset.steps = 3
        # preset.controlnet_model = controlnet


        prompt_text = convert_to_prompt("disney")#何風にするか
        additional_text = translate_2en_text("彼は手にカメラを持ち、美しい風景を撮影しています。")#以下に追加の指示文(日本語)を追加
        full_prompt_text = prompt_text + additional_text

        async for _, img in api.high_level.generate_image(
            full_prompt_text
            ,
            model,
            preset,
            ImageGenerationType.IMG2IMG,
        ):
            (d / "image_with_img2img.png").write_bytes(img)

if __name__ == "__main__":
    asyncio.run(img2img())
    # asyncio.run(control_net())

