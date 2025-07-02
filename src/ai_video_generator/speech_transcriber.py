import whisper
from ai_video_generator.utils.video_utils import download_video, extract_audio

def transcribe_from_url(url: str) -> str:
    print(f"🎬 开始处理视频：{url}")
    video_path = download_video(url)
    audio_path = extract_audio(video_path)

    print("🎧 正在进行语音识别...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]