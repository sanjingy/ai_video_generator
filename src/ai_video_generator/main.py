'''
from ai_video_generator.speech_transcriber import transcribe_from_url

if __name__ == "__main__":
    video_url = input("请输入视频 URL：")
    text = transcribe_from_url(video_url)
    print("\n📝 视频中的语音文字如下：\n")
    print(text)
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
