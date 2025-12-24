import pysubs2
import subprocess
from config import SRT_PATH, ASS_PATH, MERGED_VIDEO_PATH, FINAL_OUTPUT_PATH, FONT_NAME, FONT_SIZE

def srt_to_ass():
    """文件4功能：转换字幕格式"""
    print(">>> 步骤4: 转换 ASS 样式...")
    subs = pysubs2.load(str(SRT_PATH), encoding="utf-8")
    
    style = pysubs2.SSAStyle(
        fontname=FONT_NAME,
        fontsize=FONT_SIZE,
        primarycolor=pysubs2.Color(255, 255, 255),
        outlinecolor=pysubs2.Color(0, 0, 0),
        outline=1,
        shadow=0,
        alignment=pysubs2.Alignment.BOTTOM_CENTER,
    )
    subs.styles["Default"] = style
    subs.save(str(ASS_PATH))
    print(f"   ✅ ASS 文件已生成")

def burn_subtitles():
    """文件5功能：压制最终视频"""
    print(">>> 步骤5: 最终合成渲染...")
    
    # 路径转为绝对路径并处理 FFmpeg 滤镜中的转义问题
    # 在 Windows 下，滤镜路径需要转义反斜杠，或者使用正斜杠
    ass_path_str = str(ASS_PATH.absolute()).replace("\\", "/").replace(":", "\\:")
    
    cmd = [
        "ffmpeg", "-y", 
        "-i", str(MERGED_VIDEO_PATH),
        "-vf", f"ass='{ass_path_str}'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "copy",
        str(FINAL_OUTPUT_PATH)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"🎉🎉🎉 全部完成！最终文件: {FINAL_OUTPUT_PATH}")