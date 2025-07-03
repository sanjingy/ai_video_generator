import os
import tempfile
import requests
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
'''下载视频，并取出音频'''
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

'''
def extract_audio_from_video(video_path: str) -> str:
    """
    从视频中提取音频，返回音频路径（.wav）
    """
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path, logger=None)
    print(audio_path)
    return audio_path
'''
def extract_audio_from_video(video_path: str, output_dir: str = "D:/download") -> str:
    """
    从视频中提取音频，保存到指定路径，返回音频文件的完整路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 构造音频文件名
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, base_name + ".wav")


    # 提取音频
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)

    #清洗音频
    audio = AudioSegment.from_wav(audio_path)
    audio = audio.low_pass_filter(3000)  # 去掉高频噪声
    audio.export(audio_path, format="wav")

    print(f"✅ 音频已保存到: {audio_path}")
    return audio_path