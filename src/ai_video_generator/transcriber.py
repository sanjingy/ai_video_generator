import whisper
from ai_video_generator.utils.downloader import download_video, extract_audio_from_video


def transcribe_from_url(url: str) -> str:
    """
    给定视频链接，下载视频、提取音频并转文字
    """
    print("📥 下载视频...")
    video_path = download_video(url)

    print("🎧 提取音频...")
    audio_path = extract_audio_from_video(video_path)

    print("🧠 Whisper 模型加载中...")
    model = whisper.load_model("base")  # 可改为 "small" 或 "medium"

    print("📝 开始转录...")
    result = model.transcribe(audio_path)

    return result["text"]