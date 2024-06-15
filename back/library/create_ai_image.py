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

async def control_net():
    d = Path("results")
    d.mkdir(exist_ok=True)

    async with API() as api_handler:
        api = api_handler.api

        image = base64.b64encode((d / "test2_low_res.jpg").read_bytes()).decode()

        controlnet = ControlNetModel.Form_Lock
        _, mask = await api.low_level.generate_controlnet_mask(controlnet, image)

        model = ImageModel.Anime_Curated

        preset = ImagePreset.from_default_config(model)
        preset.controlnet_model = controlnet
        preset.controlnet_condition = base64.b64encode(mask).decode()
        preset.controlnet_strength = 0.8

        # NOTE: for some reasons, the images with controlnet are slightly different
        async for _, img in api.high_level.generate_image(
            """A magnificent photo that looks like a scene from the Harry Potter world, 
            featuring magical landscapes, enchanting castles, and mystical creatures.,photorealistic , 4K resolution,
            High resolution, masterpiece, realistic, highly detailed, cinematic lighting, vibrant colors.""",
            model,
            preset,
        ):
            (d / "image_with_controlnet.png").write_bytes(img)