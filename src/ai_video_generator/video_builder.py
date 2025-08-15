from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip,concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

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

'''生成 SRT 字幕文件'''
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

'''将图像 + 音频 合成主视频 final_video.mp4'''

def build_video_from_assets(items, output_path, target_fps=24, forced_duration=None):
    clips = []
    for txt, img, aud in items:
        try:
            audio = AudioFileClip(aud)
            duration = forced_duration or audio.duration
            image = ImageClip(img).with_duration(duration).with_audio(audio)

            subtitle = TextClip(
                font=Path(r"C:\Windows\Fonts\simsun.ttc"),
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


def add_subtitles_to_video(video_path: Path, subtitle_path: Path, output_path: Path):
    """
    将 .srt 字幕叠加到视频上并导出为新视频
    :param video_path: 原始视频路径
    :param subtitle_path: SRT 字幕路径
    :param output_path: 带字幕的视频输出路径
    """

    os.environ["IMAGEMAGICK_BINARY"] = "magick"  # 设置 ImageMagick 路径（确保已安装）

    print("📼 加载主视频：", video_path)
    main_clip = VideoFileClip(str(video_path))

    # 定义字幕生成器：将每行文字转为 TextClip
    generator = lambda txt: TextClip(
        txt,
        font="Arial Unicode MS",   # 可改成本地存在的中文字体，如："ARIALUNI.TTF"
        fontsize=48,
        color="white",
        bg_color="black",
        method="caption",
        size=main_clip.size,
    )

    print("📝 加载字幕文件：", subtitle_path)
    subtitles = SubtitlesClip(str(subtitle_path), generator)

    print("🎬 开始叠加字幕...")
    final = CompositeVideoClip([main_clip, subtitles.set_position(("center", "bottom"))])

    final.write_videofile(
        str(output_path),
        fps=main_clip.fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(output_path.with_suffix(".m4a")),
        remove_temp=True
    )

    print("✅ 成功导出带字幕视频：", output_path)

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
