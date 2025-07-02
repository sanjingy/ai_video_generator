from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import uuid


def download_video(url: str, output_dir="downloads") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(output_dir, filename)

    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=False).first()
    stream.download(output_path=output_path)
    print(f"✅ 视频下载完成：{output_path}")
    return output_path


def extract_audio(video_path: str, output_dir="audio") -> str:
    os.makedirs(output_dir, exist_ok=True)
    audio_path = os.path.join(output_dir, os.path.basename(video_path).replace(".mp4", ".wav"))

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"✅ 音频提取完成：{audio_path}")
    return audio_path