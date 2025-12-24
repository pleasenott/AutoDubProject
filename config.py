import os
from pathlib import Path

# === 路径配置 ===
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "inputs"
WORKSPACE_DIR = BASE_DIR / "workspace"
OUTPUT_DIR = BASE_DIR / "outputs"

# 创建必要的文件夹
WORKSPACE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 输入文件路径
VIDEO_SRC_DIR = INPUT_DIR / "video"
AUDIO_SRC_DIR = INPUT_DIR / "audio"
TXT_CN_PATH = INPUT_DIR / "text_cn.txt"
TXT_EN_PATH = INPUT_DIR / "text_en.txt"

# 中间文件路径
PROCESSED_CLIPS_DIR = WORKSPACE_DIR / "clips"
MERGED_VIDEO_PATH = WORKSPACE_DIR / "merged_raw.mp4"
SRT_PATH = WORKSPACE_DIR / "subtitles.srt"
ASS_PATH = WORKSPACE_DIR / "subtitles.ass"
TEMP_WAV_PATH = WORKSPACE_DIR / "temp_audio.wav"

# 最终输出
FINAL_OUTPUT_PATH = OUTPUT_DIR / "final_submission.mp4"

# === 参数配置 ===
WHISPER_MODEL = "medium"  # medium, large, etc.
FONT_NAME = "Arial"       # 字幕字体
FONT_SIZE = 8             # 字幕大小