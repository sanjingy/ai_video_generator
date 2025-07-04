from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip



'''合成单句视频模块'''

def create_clip(image_path: str, audio_path: str, subtitle_text: str, output_path: str):
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    image = ImageClip(image_path).with_duration(duration).resize(height=720)
    image = image.set_audio(audio)

    subtitle = TextClip(
        subtitle_text,
        fontsize=48,
        color='white',
        font='Arial-Bold',
        bg_color='black',
        method='caption',
        size=image.size
    ).with_duration(duration).set_position(('center', 'bottom'))

    final = CompositeVideoClip([image, subtitle])
    final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"🎞️ 视频片段已保存：{output_path}")
