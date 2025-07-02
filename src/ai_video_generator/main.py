'''
from ai_video_generator.speech_transcriber import transcribe_from_url

if __name__ == "__main__":
    video_url = input("请输入视频 URL：")
    text = transcribe_from_url(video_url)
    print("\n📝 视频中的语音文字如下：\n")
    print(text)
'''
from ai_video_generator.transcriber import transcribe_from_url

video_url = input("请输入视频 URL：")
text = transcribe_from_url(video_url)

print("\n🎤 转录结果如下：\n")
print(text)