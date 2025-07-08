'''
from transcriber import transcribe_from_url
from optimizer import optimize_text_and_generate_tags

if __name__ == "__main__":
    video_url = input("🎥 请输入视频链接：")

    print("📥 下载视频并转音频...")
    text = transcribe_from_url(video_url)

    print("🧠 开始优化转录文本并生成风格 tag...")
    result = optimize_text_and_generate_tags(text, style="二次元")

    for item in result:
        print("📝 原句:", item["sentence"])
        print("✅ 优化:", item["optimized"])
        print("🏷️ Tags:", " ".join(item["tags"]))
        print("-" * 40)
'''
'''
import json
from pathlib import Path

from optimizer import optimize_text_and_generate_tags
from generator import generate_assets
from video_builder import create_clip
import os
from transcriber import transcribe_from_url

config = json.loads(Path("D:\download\config.json").read_text(encoding="utf-8"))
if __name__ == "__main__":
    video_url = input("🎥 请输入视频链接：")
    #video_url = config["source_video_url"]
    #语音风格
    tts_voice = config["tts_voice"]
    #图片风格
    style = config["image_style"]

    print("📥 下载视频并转音频...")
    text = transcribe_from_url(video_url)

    print("🧠 开始优化转录文本并生成风格 tag...")
    result = optimize_text_and_generate_tags(text, style="二次元")

    #sentences = optimize_text_and_generate_tags(next, style="二次元")
    output_dir=Path(config["output_dir"])
    os.makedirs(output_dir, exist_ok=True)

    for idx, item in enumerate(result):
        sentence, tags = item["optimized"], item["tags"]
        img_path, audio_path = generate_assets(sentence, tags, idx, output_dir)
        video_path = os.path.join(output_dir, f"clip_{idx:03}.mp4")
        create_clip(img_path, audio_path, sentence, video_path)
'''
# src/ai_video_generator/main.py
import asyncio
from ai_video_generator.pipeline import process_video

if __name__ == "__main__":
    video_url = input("请输入视频URL：").strip()
    asyncio.run(process_video(video_url, output_dir="outputs"))