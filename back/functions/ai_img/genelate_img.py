import asyncio
import base64
from pathlib import Path

from .boilerplate import API

from novelai_api.ImagePreset import (
    ImageGenerationType,
    ImageModel,
    ImagePreset,
    ControlNetModel,
)

from .translate_ja2en import translate_2en_text

from .res_lower import reduce_resolution

from .prompt_pattern import convert_to_prompt

import asyncio
import time
from pathlib import Path

from novelai_api.ImagePreset import ImageModel, ImagePreset, ImageSampler, UCPreset
from novelai_api.NovelAIError import NovelAIError



async def control_net(file_id, selection, add_prompt):

    d = Path("imgs")
    d.mkdir(exist_ok=True)
    
    

    async with API() as api_handler:
        api = api_handler.api
        reduce_resolution( f"./{file_id}.jpg", d/ f"./{file_id}_low.jpg", 4) # 画像の解像度を下げる
        image = base64.b64encode((d/ f"./{file_id}_low.jpg").read_bytes()).decode()

        controlnet = ControlNetModel.Form_Lock
        _, mask = await api.low_level.generate_controlnet_mask(controlnet, image)

        model = ImageModel.Anime_Full

        preset = ImagePreset.from_default_config(model)
        preset.controlnet_model = controlnet
        preset.controlnet_condition = base64.b64encode(mask).decode()
        preset.controlnet_strength = 1.8
        preset.steps = 5

        prompt_text = convert_to_prompt(selection)#何風にするか
        additional_text = translate_2en_text(add_prompt)#以下に追加の指示文(日本語)を追加
        # full_prompt_text = prompt_text + additional_text
        full_prompt_text = prompt_text + additional_text
        # NOTE: for some reasons, the images with controlnet are slightly different 
        async for _, img in api.high_level.generate_image(
            full_prompt_text,
            model,
            preset,
            ImageGenerationType.IMG2IMG,
        ):
            (d/ f"./{file_id}_gen.jpg").write_bytes(img)

async def img2img(file_id, selection, add_prompt):
    d = Path("imgs")
    d.mkdir(exist_ok=True)

    reduce_resolution( f"./{file_id}.jpg", d/ f"./{file_id}_low.jpg", 4) # 画像の解像度を下げる
    image = base64.b64encode(( d/f"./{file_id}_low.jpg").read_bytes()).decode()

    async with API() as api_handler:
        api = api_handler.api
        model = ImageModel.Anime_v3
        # controlnet = ControlNetModel.Scribbler

        preset = ImagePreset.from_default_config(model)
        preset.noise = 0.5
        # note that steps = 28, not 50, which mean strength needs to be adjusted accordingly
        preset.strength = 1.7
        preset.image = image
        preset.steps = 3
        # preset.controlnet_model = controlnet


        prompt_text = convert_to_prompt(selection)#何風にするか
        additional_text = translate_2en_text(add_prompt)#以下に追加の指示文(日本語)を追加
        full_prompt_text = prompt_text + additional_text

        async for _, img in api.high_level.generate_image(
            full_prompt_text,
            model,
            preset,
            ImageGenerationType.IMG2IMG,
        ):
            (d/ f"./{file_id}_gen.jpg").write_bytes(img)

async def main(file_id, selection, add_prompt):
    d = Path("imgs")
    d.mkdir(exist_ok=True)

    reduce_resolution( f"./{file_id}.jpg", d/ f"./{file_id}_low.jpg", 4) # 画像の解像度を下げる
    image = base64.b64encode(( d/f"./{file_id}_low.jpg").read_bytes()).decode()

    async with API() as api_handler:
        api = api_handler.api

        model = ImageModel.Furry_v3

        preset = ImagePreset.from_default_config(model)
        preset.uc_preset = UCPreset.Preset_Light

        prompt_text = convert_to_prompt(selection)#何風にするか
        additional_text = translate_2en_text(add_prompt)#以下に追加の指示文(日本語)を追加
        full_prompt_text = prompt_text + additional_text

        prompt = ""
        samplers = list(ImageSampler)

        async for _, img in api.high_level.generate_image(full_prompt_text, model, preset):
            (d/f"./{file_id}_gen.jpg").write_bytes(img)


if __name__ == "__main__":
    asyncio.run(img2img())
    # asyncio.run(control_net())