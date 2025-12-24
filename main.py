import os
import sys
from config import VIDEO_SRC_DIR, AUDIO_SRC_DIR, TXT_CN_PATH, TXT_EN_PATH
from core.media_processor import sync_video_audio, concat_videos
from core.sub_generator import generate_bilingual_srt
from core.sub_renderer import srt_to_ass, burn_subtitles

def check_inputs():
    """检查输入文件是否齐全"""
    if not any(VIDEO_SRC_DIR.glob("*.mp4")):
        print(f"❌ 错误: {VIDEO_SRC_DIR} 中没有 MP4 视频")
        return False
    if not any(AUDIO_SRC_DIR.glob("*.m4a")):
        print(f"❌ 错误: {AUDIO_SRC_DIR} 中没有 M4A 音频")
        return False
    if not TXT_EN_PATH.exists() or not TXT_CN_PATH.exists():
        print("❌ 错误: 缺少 text_en.txt 或 text_cn.txt")
        return False
    return True

def main():
    print("==========================================")
    print("   一键生成英文配音作业 (AutoDubProject)   ")
    print("==========================================")
    
    if not check_inputs():
        return

    # 1. 视频音频变速对齐
    processed_clips = sync_video_audio(VIDEO_SRC_DIR, AUDIO_SRC_DIR)
    if not processed_clips:
        print("❌ 没有生成任何片段，程序终止")
        return

    # 2. 拼接长视频
    concat_videos(processed_clips)

    # 3. 识别并生成字幕
    # 注意：MERGED_VIDEO_PATH 在 config 中定义，隐式传递
    # 这里直接传递路径给函数处理
    from config import MERGED_VIDEO_PATH
    generate_bilingual_srt(MERGED_VIDEO_PATH, TXT_CN_PATH, TXT_EN_PATH)

    # 4. 转 ASS
    srt_to_ass()

    # 5. 压制最终视频
    burn_subtitles()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 程序发生未捕获的错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 可选：运行完后清理 workspace 下的临时文件
        # import shutil
        # from config import WORKSPACE_DIR
        # shutil.rmtree(WORKSPACE_DIR)
        pass