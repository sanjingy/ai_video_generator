from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip


def create_clip(image_path: str, audio_path: str, subtitle_text: str, output_path: str):
    try:
        # 加载音频
        audio = AudioFileClip(audio_path)
        duration = audio.duration

        # 创建图像剪辑
        image = ImageClip(image_path).with_duration(duration)
        image = image.resized(height=720).with_audio(audio)

        # 创建字幕 - 最新MoviePy兼容写法
        subtitle = (TextClip(
            text=subtitle_text,  # 明确使用参数名
            size=(image.w, None),
            color='white',
            bg_color='black',
            method='caption',
            #font='Arial-Bold',  # 字体名称
            font_size=48)  # 字号
                    .with_duration(duration)
                    #.set_position(('center', 'bottom'))
                    )

        # 合成最终视频
        final = CompositeVideoClip([image, subtitle])
        final.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            #verbose=False,
            logger=None  # 禁用日志避免干扰
        )
        print(f"✅ 视频成功生成: {output_path}")
        return True

    except Exception as e:
        print(f"❌ 视频生成失败: {str(e)}")
        return False

# 调用示例
create_clip(
    image_path=r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_000.jpg",
    audio_path=r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_000.mp3",
    subtitle_text='一个小猫',
    output_path=r"D:\Project\DM_program\ai_video_generator\src\ai_video_generator\output\clip_000.mp4"
)