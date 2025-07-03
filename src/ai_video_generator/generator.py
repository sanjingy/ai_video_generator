import os
import requests
import asyncio
import edge_tts
from openai import OpenAI
'''图像 & 语音生成器模块'''

#暂时使用通义千文的
client = OpenAI(api_key=input("请输入图片模型API"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")


def generate_image(prompt: str, output_path: str):
    response = client.images.generate(
        model="flux-dev",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    url = response.data[0].url
    image_data = requests.get(url).content
    with open(output_path, "wb") as f:
        f.write(image_data)
    print(f"🖼️ 图片已生成：{output_path}")


async def generate_audio(text: str, output_path: str, voice="zh-CN-XiaoxiaoNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(output_path)
    print(f"🔊 语音已生成：{output_path}")


def generate_assets(sentence: str, tags: list[str], index: int, output_dir: str):
    """根据句子和tag生成图像和音频文件"""
    prompt = f"{sentence} " + " ".join([f"#{tag}" for tag in tags])
    img_path = os.path.join(output_dir, f"clip_{index:03}.jpg")
    audio_path = os.path.join(output_dir, f"clip_{index:03}.mp3")

    generate_image(prompt, img_path)
    asyncio.run(generate_audio(sentence, audio_path))

    return img_path, audio_path
