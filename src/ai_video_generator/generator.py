import os, json, hashlib, asyncio, requests
from pathlib import Path
from retry import retry
import edge_tts
from dashscope import ImageSynthesis  # 通义千问的图像生成

# 读取配置
config_path = Path(r"D:\download\config.json")  # 使用原始字符串
try:
    config_data = json.loads(config_path.read_text(encoding="utf-8"))
    print("配置加载成功:", config_data)
except FileNotFoundError:
    print(f"错误：配置文件 {config_path} 不存在")
except json.JSONDecodeError as e:
    print(f"错误：配置文件格式无效 - {e}")
except Exception as e:
    print(f"未知错误：{e}")
config = json.loads(config_path.read_text(encoding="utf-8"))

def get_paths(sentence, tags, odir):
    key = hashlib.sha256((sentence + ''.join(tags)).encode()).hexdigest()[:8]
    return odir / f"{key}.jpg", odir / f"{key}.mp3"


@retry()
def generate_image(prompt: str, output_path: str):
    try:
        response = ImageSynthesis.call(
            api_key=config["api_keys"]["dashscope"],
            model="wanx2.1-t2i-turbo",
            prompt=prompt,
            n=1,
            size='1080*1440'
        )

        if response.status_code != 200 or response.output.task_status != "SUCCEEDED":
            raise Exception(f"图片生成失败: {getattr(response.output, 'message', '未知错误')}")

        url = response.output.results[0].url
        image_data = requests.get(url).content
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"🖼️ 图片已生成：{output_path}")

    except Exception as e:
        print(f"❌ 生成图片失败: {str(e)}")
        raise

@retry()
async def generate_audio(text: str, output_path: str, voice="zh-CN-XiaoxiaoNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(output_path)
    print(f"🔊 语音已生成：{output_path}")

"""根据句子和tag生成图像和音频文件"""
async def generate_assets_async(sentence, tags, idx, odir):
    img, aud = get_paths(sentence, tags, odir)
    if img.exists() and aud.exists():
        print(f"✅ 缓存命中：{img}, {aud}")
        return str(img), str(aud)

    prompt = f"{sentence}，风格：{','.join(tags)}"
    await asyncio.gather(
        asyncio.to_thread(generate_image, prompt, str(img)),
        generate_audio(sentence, str(aud))
    )
    return str(img), str(aud)
