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
from optimizer import optimize_text_and_generate_tags
from generator import generate_assets
from video_builder import create_clip
import os

sentences = optimize_text_and_generate_tags(next, style="二次元")
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for idx, item in enumerate(sentences):
    sentence, tags = item["optimized"], item["tags"]
    img_path, audio_path = generate_assets(sentence, tags, idx, output_dir)
    video_path = os.path.join(output_dir, f"clip_{idx:03}.mp4")
    create_clip(img_path, audio_path, sentence, video_path)
