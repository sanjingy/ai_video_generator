import os
import tempfile
import requests
from moviepy.video.io.VideoFileClip import VideoFileClip


def download_video(url: str) -> str:
    """
    下载视频到临时路径，返回视频文件路径
    """
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception("视频下载失败")

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".mp4")
    with os.fdopen(tmp_fd, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return tmp_path


def extract_audio_from_video(video_path: str) -> str:
    """
    从视频中提取音频，返回音频路径（.wav）
    """
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path, logger=None)
    return audio_path