import subprocess
import os
from pathlib import Path
from config import PROCESSED_CLIPS_DIR, MERGED_VIDEO_PATH

def get_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return float(result.stdout.strip())

def sync_video_audio(video_dir: Path, audio_dir: Path):
    """文件1功能：将视频变速以匹配音频时长"""
    PROCESSED_CLIPS_DIR.mkdir(exist_ok=True)
    
    print(">>> 步骤1: 视频音频时长对齐...")
    processed_files = []

    # 获取所有视频并排序，确保顺序
    video_files = sorted(list(video_dir.glob("*.mp4")))

    for video_path in video_files:
        name = video_path.stem
        audio_path = audio_dir / f"{name}.m4a"
        output_path = PROCESSED_CLIPS_DIR / f"{name}.mp4"

        if not audio_path.exists():
            print(f"⚠️ 警告: {name} 找不到对应音频，跳过")
            continue

        try:
            v_dur = get_duration(video_path)
            a_dur = get_duration(audio_path)
            ratio = v_dur / a_dur
            
            cmd = [
                "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
                "-filter:v", f"setpts=PTS/{ratio}",
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "copy", "-shortest", str(output_path)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            processed_files.append(output_path)
            print(f"   ✅ 已处理: {name} (比例 {ratio:.2f})")
        except Exception as e:
            print(f"   ❌ 处理失败 {name}: {e}")
            
    return processed_files

def concat_videos(video_files):
    """文件2功能：拼接所有处理后的视频"""
    print(">>> 步骤2: 拼接视频片段...")
    list_file = PROCESSED_CLIPS_DIR / "concat_list.txt"
    
    # 按文件名排序，确保拼接顺序正确
    video_files.sort(key=lambda x: x.name)

    with open(list_file, "w", encoding="utf-8") as f:
        for v in video_files:
            # 解决Windows路径转义问题
            path_str = str(v.absolute()).replace("\\", "/")
            f.write(f"file '{path_str}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file), "-c", "copy", str(MERGED_VIDEO_PATH)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    print(f"   ✅ 拼接完成: {MERGED_VIDEO_PATH}")