from ai_video_generator.speech_transcriber import transcribe_from_url

if __name__ == "__main__":
    video_url = input("https://www.douyin.com/aweme/v1/play/?video_id=v0200fg10000d1237k7og65r9vku1qn0&line=0&file_id=c9be667b5ec54932aa81c2c5b3d6f51b&sign=284c5954f9ee47ba3043dc7138612960&is_play_url=1&source=PackSourceEnum_AWEME_DETAIL")
    text = transcribe_from_url(video_url)
    print("\n📝 视频中的语音文字如下：\n")
    print(text)