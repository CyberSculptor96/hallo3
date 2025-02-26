"""
    使用时请移至./hallo3目录下，确保没有路径问题
"""
import argparse
import logging
import sys
import os
from pathlib import Path
from typing import List

import torch
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from hallo3.sgm.utils.audio_processor import AudioProcessor
from hallo3.sgm.utils.util import extract_audio_from_videos

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_missing_audio_emb_files(missing_file_path: Path) -> List[Path]:
    """
    读取缺失的 `audio_emb` 文件路径，并转换为对应的视频文件路径。

    Args:
        missing_file_path (Path): `missing_files.txt` 文件路径。

    Returns:
        List[Path]: 需要重新提取 `audio_emb` 的视频文件路径列表。
    """
    missing_videos = []
    with open(missing_file_path, "r", encoding="utf-8") as file:
        for line in file:
            missing_audio_emb_path = Path(line.strip())

            if "audio_emb" in missing_audio_emb_path.parts:
                video_filename = missing_audio_emb_path.stem + ".mp4"
                video_path = missing_audio_emb_path.parents[1] / "videos" / video_filename
                
                if video_path.exists():
                    missing_videos.append(video_path)
                else:
                    logging.warning(f"对应视频文件不存在: {video_path}")
    
    return missing_videos


def process_audio_embedding(video_path: Path, output_dir: Path, audio_processor: AudioProcessor) -> None:
    """
    仅重新提取 `audio_emb` 并保存。

    Args:
        video_path (Path): 视频文件路径。
        output_dir (Path): `audio_emb` 存储目录。
        audio_processor (AudioProcessor): 处理音频的工具。
    """
    try:
        fps = 25  # 默认帧率，如有 `get_fps` 方法可替换

        audio_output_dir = output_dir / "audios"
        audio_output_dir.mkdir(parents=True, exist_ok=True)
        audio_output_path = audio_output_dir / f"{video_path.stem}.wav"

        if not audio_output_path.exists():
            logging.info(f"提取音频: {video_path} -> {audio_output_path}")
            extract_audio_from_videos(video_path, audio_output_path)
        
        # 处理音频嵌入
        audio_emb, _ = audio_processor.preprocess(audio_output_path, fps=fps)

        audio_emb_output_path = output_dir / "audio_emb" / f"{video_path.stem}.pt"
        torch.save(audio_emb, audio_emb_output_path)
        logging.info(f"已保存 audio_emb: {audio_emb_output_path}")

    except Exception as e:
        logging.error(f"处理 {video_path} 失败: {e}")


def process_missing_audio_emb(missing_files: Path, output_dir: Path) -> None:
    """
    处理所有缺失的 `audio_emb`。

    Args:
        missing_files (Path): `missing_files.txt` 文件路径。
        output_dir (Path): 结果存储目录。
    """
    audio_separator_model_file = "../pretrained_models/audio_separator/Kim_Vocal_2.onnx"
    wav2vec_model_path = '../pretrained_models/wav2vec/wav2vec2-base-960h'

    audio_processor = AudioProcessor(
        16000,
        wav2vec_model_path,
        False,
        os.path.dirname(audio_separator_model_file),
        os.path.basename(audio_separator_model_file),
        os.path.join(output_dir, "vocals"),
    )

    missing_videos = load_missing_audio_emb_files(missing_files)

    if not missing_videos:
        logging.info("没有需要处理的 audio_emb 文件")
        return

    for video_path in tqdm(missing_videos, desc="Processing missing audio_emb"):
        process_audio_embedding(video_path, output_dir, audio_processor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="重新提取缺失的 audio_emb 文件")
    parser.add_argument("-m", "--missing_files", type=Path, required=True, help="缺失文件列表 (missing_files.txt)")
    parser.add_argument("-o", "--output_dir", type=Path, required=True, help="输出目录")

    args = parser.parse_args()
    
    process_missing_audio_emb(args.missing_files, args.output_dir)
