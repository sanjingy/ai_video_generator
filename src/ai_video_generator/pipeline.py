# src/ai_video_generator/pipeline.py
from ai_video_generator.transcriber import transcribe_from_url
from .optimizer import optimize_text_and_generate_tags
from .generator import generate_assets_async
from .video_builder import build_video_from_assets
import asyncio
from pathlib import Path
import json
config = json.loads(Path("D:\download\config.json").read_text(encoding="utf-8"))

async def process_video(url: str, output_dir: str):
    # 1. Whisper 转录
    print("📥 下载视频并转音频...")
    text = transcribe_from_url(url)
    #sentences = text.strip().split("。")
    style = config["image_style"]

    print("🧠 开始优化转录文本并生成风格 tag...")
    tagged  = optimize_text_and_generate_tags(text, style)
    # tagged = [      (s, optimize_text_and_generate_tags(s, style))for s in sentences if s.strip() ]


    # 3. 图像 + 音频生成（带缓存、并发）
    odir = Path(output_dir)
    odir.mkdir(exist_ok=True)
    results = []
    for idx, item in enumerate(tagged):
        sentence, tags = item["optimized"], item["tags"]
        img, aud = await generate_assets_async(sentence, tags, idx, odir)
        results.append((sentence, img, aud))


    # 4. 合成视频
    build_video_from_assets(results, odir / "final_video.mp4")
    return results