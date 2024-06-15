from PIL import Image

def reduce_resolution(image_path, output_path, factor):
    with Image.open(image_path) as img:
        # 元の画像の解像度を取得
        width, height = img.size

        # 新しい解像度を計算
        new_width = width // factor
        new_height = height // factor

        # 画像のリサイズ
        resized_img = img.resize((new_width, new_height))

        # リサイズした画像を保存
        resized_img.save(output_path)