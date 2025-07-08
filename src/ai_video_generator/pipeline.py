# src/ai_video_generator/pipeline.py
from .transcriber import transcribe_from_url
from .optimizer import optimize_text_and_generate_tags
from .generator import generate_assets_async
from .video_builder import build_video_from_assets
import asyncio
from pathlib import Path


async def process_video(url: str, output_dir: str):
    # 1. Whisper 转录
    text = transcribe_from_url(url)
    sentences = text.strip().split("。")

    # 2. 大模型优化文本 + tag
    tagged = [optimize_text_and_generate_tags(s) for s in sentences if s.strip()]

    # 3. 图像 + 音频生成（带缓存、并发）
    odir = Path(output_dir)
    odir.mkdir(exist_ok=True)
    results = []
    for idx, (s, tags) in enumerate(tagged):
        img, aud = await generate_assets_async(s, tags, idx, odir)
        results.append((s, img, aud))

    # 4. 合成视频（字幕+控制速率）
    build_video_from_assets(results, odir / "final_video.mp4")
