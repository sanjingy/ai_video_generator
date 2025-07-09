from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip,concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

import pysubs2
from pathlib import Path
import os
os.environ["IMAGEMAGICK_BINARY"] = "magick"

'''
clip = TextClip(font=Path(r"C:\Windows\Fonts\ARIALNI.TTF"),text="你好",size=(12,13),font_size=70, color='white', bg_color='black', method='caption')
clip = clip.with_duration(2)
clip.write_videofile("test_subtitle.mp4", fps=24)
'''
def build_video_from_assets(items, output_path, target_fps=24, forced_duration=None):
    clips = []
    for txt, img, aud in items:
        try:
            audio = AudioFileClip(aud)
            duration = forced_duration or audio.duration
            image = ImageClip(img).with_duration(duration).with_audio(audio)

            subtitle = TextClip(
                font=Path(r"C:\Windows\Fonts\ARIALNI.TTF"),
                text=txt,
                font_size=48,
                color='white',
                bg_color='black',
                size=image.size,
                method='caption',  # 需要 ImageMagick
                horizontal_align="center",
                vertical_align="bottom",
            ).with_duration(duration)#.set_position(('center', 'bottom'))

            clip = CompositeVideoClip([image, subtitle]).with_fps(24)
            clips.append(clip)

        except Exception as e:
            print(f"❌ 错误：处理 {aud} 时出错：{e}")
            continue

    if not clips:
        print("⚠️ 没有成功的视频片段，无法生成最终视频。")
        return

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(str(output_path), fps=target_fps, codec="libx264", audio_codec="aac")
    print("✅ 视频合并完成：", output_path)

items = [
    ("你好，这是测试字幕1。", r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_000.jpg",
     r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_000.mp3"),
    ("第二句测试字幕，继续测试。", r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_001.jpg",
     r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_001.mp3"),
]

# 输出路径
output_path = Path(r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\test1.mp4")

# 调用函数生成视频
build_video_from_assets(items, output_path)
