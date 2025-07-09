from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip,concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

import pysubs2
from pathlib import Path

import os
os.environ["IMAGEMAGICK_BINARY"] = "magick"


'''合成单句视频模块'''

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

'''
生成字幕
'''
def save_srt(items, srt_path):
    subs = pysubs2.SSAFile()
    for i,(txt, img, aud) in enumerate(items,1):
        dur = AudioFileClip(aud).duration
        subs.append(pysubs2.SSAEvent(
            start=int(0 * 1000 + sum(AudioFileClip(a).duration for _,_,a in items[:i-1])*1000),
            end=int(dur*1000 + sum(AudioFileClip(a).duration for _,_,a in items[:i-1])*1000),
            text=txt
        ))
    subs.save(srt_path)
    print("字幕文件已保存：", srt_path)

'''合并视频'''

def build_video_from_assets(items, output_path, target_fps=24, forced_duration=None):
    clips = []
    for txt, img, aud in items:
        try:
            with AudioFileClip(aud) as audio:
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

                clip = CompositeVideoClip([image, subtitle]).with_fps(target_fps)
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