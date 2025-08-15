from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip,concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from pathlib import Path
import os
import matplotlib.font_manager as fm
'''
# 正确的调用方式
test = TextClip(
    text="测试文字",  # 文本内容直接作为第一个参数
    font=Path(r"C:\Windows\Fonts\simsun.ttc"),

    font_size=48,
    color='white',
    method='label'
)
test.save_frame(r"D:\Project\DM_program\ai_video_generator\tests\test.png")
'''

#video_path = Path(r"D:/download/final_video.mp4")
video_path = Path(r"D:/download/")
subtitle_path = Path(r"D:\download\subtitles.srt")
output_path = Path(r"D:\download\fainavi.mp4")
'''
with open(subtitle_path, 'r', encoding='utf-8') as f:
    print(f.read())  # 检查前几行内容
'''

def get_preferred_font_path():
    preferred_fonts = ["Microsoft YaHei", "Arial", "SimSun", "SimHei"]
    system_fonts = fm.findSystemFonts(fontpaths=None, fontext="ttf")

    for font_path in system_fonts:
        try:
            font_name = fm.FontProperties(fname=font_path).get_name()
            if font_name in preferred_fonts:
                print(f"✅ 使用字体: {font_name}")
                return font_path
        except Exception:
            continue
    raise RuntimeError("❌ 无法找到可用字体。")

def concat_video_clips(input_dir: Path, output_path: Path):
    print("📁 加载子视频目录：", input_dir)
    if not input_dir.exists():
        raise FileNotFoundError(f"❌ 输入目录不存在：{input_dir}")

    # 读取所有视频文件，按文件名排序
    video_files = sorted(input_dir.glob("*.mp4"))
    if not video_files:
        raise ValueError("❌ 没有找到任何子视频文件 (*.mp4)")

    print(f"🔍 发现 {len(video_files)} 个子视频，将进行拼接...")

    clips = [VideoFileClip(str(f)) for f in video_files]
    final_clip = concatenate_videoclips(clips, method="compose")

    final_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
    print("✅ 视频拼接完成：", output_path)


# 示例用法

concat_video_clips(video_path, output_path)
