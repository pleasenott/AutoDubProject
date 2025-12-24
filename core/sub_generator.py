import stable_whisper
import os
import re
import warnings
import subprocess
from config import TEMP_WAV_PATH, SRT_PATH, WHISPER_MODEL

warnings.filterwarnings("ignore")

def extract_audio(video_path):
    print("   ...正在提取纯净音频")
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path), 
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", 
        str(TEMP_WAV_PATH)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def load_lines(path):
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def format_timestamp(seconds):
    if seconds is None: seconds = 0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def clean_str(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text)

def generate_bilingual_srt(video_path, cn_path, en_path):
    """文件3功能：生成对齐的双语SRT"""
    print(f">>> 步骤3: AI 生成双语字幕 ({WHISPER_MODEL})...")
    
    extract_audio(video_path)
    
    model = stable_whisper.load_model(WHISPER_MODEL, device="cpu") # 如有显卡改为 cuda
    zh_lines = load_lines(cn_path)
    en_lines = load_lines(en_path)
    
    full_en_text = " ".join(en_lines)
    result = model.align(str(TEMP_WAV_PATH), text=full_en_text, language='en')
    
    all_words = []
    for seg in result.segments:
        if seg.words:
            all_words.extend(seg.words)
            
    srt_content = ""
    curr_idx = 0
    total_words = len(all_words)
    
    for i, en_line in enumerate(en_lines):
        zh_text = zh_lines[i] if i < len(zh_lines) else ""
        target_len = len(clean_str(en_line))
        if target_len == 0: continue

        line_start = None
        line_end = 0.0
        collected_len = 0
        
        while collected_len < target_len and curr_idx < total_words:
            w_obj = all_words[curr_idx]
            if line_start is None: line_start = w_obj.start
            line_end = w_obj.end
            collected_len += len(clean_str(w_obj.word))
            curr_idx += 1
            
        if line_start is None: line_start = line_end
        if line_end < line_start: line_end = line_start + 0.5
        
        srt_content += f"{i+1}\n{format_timestamp(line_start)} --> {format_timestamp(line_end)}\n"
        srt_content += f"{zh_text}\n{en_line}\n\n"
        
    with open(SRT_PATH, "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    print(f"   ✅ SRT 字幕已生成: {SRT_PATH}")