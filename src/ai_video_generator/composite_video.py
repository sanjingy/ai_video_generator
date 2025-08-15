from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from pathlib import Path

'''将 SRT 字幕叠加进主视频'''
def concat_clips(output_dir:Path, final_name="final.mp4"):
    clips = []
    for mp4 in sorted(output_dir.glob("clip_*.mp4")):
        clips.append(VideoFileClip(str(mp4)))
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(str(output_dir/final_name), fps=24, codec="libx264", audio_codec="aac")
    print("✅ 最终视频合并完成")
