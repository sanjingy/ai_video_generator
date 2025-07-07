import os
import requests
import asyncio
import edge_tts
from dashscope import ImageSynthesis  # 通义千问使用另一套
import json
from pathlib import Path
# from openai import OpenAI
'''图像 & 语音生成器模块'''

# 暂时使用通义千文的
# client = OpenAI(api_key=input("请输入图片模型API"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
config = json.loads(Path("D:\download\config.json").read_text(encoding="utf-8"))
def generate_image(prompt: str, output_path: str):
    try:
        # 调用API
        response = ImageSynthesis.call(
            #api_key=input("输入图片生成大模型key:"),
            api_key=config["api_keys"]["dashscope"],
            model="wanx2.1-t2i-turbo",
            prompt=prompt,
            n=1,
            size='1080*1440'
        )

        print("API响应:", response)  # 调试用

        # 检查任务状态
        if response.status_code != 200 or response.output.task_status != "SUCCEEDED":
            error_msg = response.output.message if hasattr(response.output, 'message') else "未知错误"
            raise Exception(f"图片生成失败: {error_msg} (代码: {getattr(response.output, 'code', '无')})")

        # 确保results不为空
        if not response.output.results:
            raise Exception("未生成任何图片结果")

        # 获取图片URL
        url = response.output.results[0].url  # 使用点号访问属性

        # 下载并保存图片
        image_data = requests.get(url).content
        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"🖼️ 图片已生成：{output_path}")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        # 可以选择返回False或重新抛出异常
        raise

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
