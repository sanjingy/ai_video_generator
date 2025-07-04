import requests
from dashscope import ImageSynthesis
import os

'''图像 & 语音生成器模块'''

# 暂时使用通义千文的
#client = OpenAI(api_key=input("请输入图片模型API"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")


def generate_image(prompt: str, output_path: str):
    response = ImageSynthesis.call(api_key=input("key:"),
                                   model="wanx2.1-t2i-turbo",
                                   prompt=prompt,
                                   n=1,
                                   size='1080*1440')
    print(response)
    url = response["output"]["results"][0]["url"]
    image_data = requests.get(url).content
    with open(output_path, "wb") as f:
        f.write(image_data)
    print(f"🖼️ 图片已生成：{output_path}")


generate_image('一间有着精致窗户的花店，漂亮的木质门，摆放着花朵',r'D:\Project\DM_program\ai_video_generator\tests\1.jpg')