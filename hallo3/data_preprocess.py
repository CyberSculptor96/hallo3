# pylint: disable=W1203,W0718
"""
This module is used to process videos to prepare data for training. It utilizes various libraries and models
to perform tasks such as video frame extraction, audio extraction, face mask generation, and face embedding extraction.
The script takes in command-line arguments to specify the input and output directories, GPU status, level of parallelism,
and rank for distributed processing.

Usage:
    python -m scripts.data_preprocess --input /path/to/video_dir --dataset_name dataset_name --gpu_status --parallelism 4 --rank 0

Example:
    python -m scripts.data_preprocess -i data/videos -o data/output -g -p 4 -r 0
"""
import argparse
import logging
import os
from pathlib import Path
from typing import List, Union
import json
import shutil
import subprocess
import cv2
import torch
from tqdm import tqdm
from sgm.utils.audio_processor import AudioProcessor
from sgm.utils.image_processor import ImageProcessorForDataProcessing
from sgm.utils.util import convert_video_to_images, extract_audio_from_videos, get_fps

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def setup_directories(video_path: Path) -> dict:
    """
    Setup directories for storing processed files.

    Args:
        video_path (Path): Path to the video file.

    Returns:
        dict: A dictionary containing paths for various directories.
    """
    if args.input.is_file() and args.input.suffix == '.json':
        base_dir = args.input.parent
    else:
        base_dir = video_path.parent.parent
    
    dirs = {
        "face_mask": base_dir / "face_mask",
        "face_emb": base_dir / "face_emb",
        "audio_emb": base_dir / "audio_emb"
    }

    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    return dirs


def process_single_video(video_path: Path,
                         output_dir: Path,
                         image_processor: ImageProcessorForDataProcessing,
                         audio_processor: AudioProcessor,
                         ) -> None:
    """
    Process a single video file.

    Args:
        video_path (Path): Path to the video file.
        output_dir (Path): Directory to save the output.
        image_processor (ImageProcessorForDataProcessing): Image processor object.
        audio_processor (AudioProcessor): Audio processor object.
        gpu_status (bool): Whether to use GPU for processing.
    """
    assert video_path.exists(), f"Video path {video_path} does not exist"
    dirs = setup_directories(video_path)
    logging.info(f"Processing video: {video_path}")

    try:
        images_output_dir = output_dir / 'images' / video_path.stem
        images_output_dir.mkdir(parents=True, exist_ok=True)
        images_output_dir = convert_video_to_images(
            video_path, images_output_dir, fps=24.0)
        logging.info(f"Images saved to: {images_output_dir}")
        
        fps = get_fps(video_path)

        audio_output_dir = output_dir / 'audios'
        audio_output_dir.mkdir(parents=True, exist_ok=True)
        audio_output_path = audio_output_dir / f'{video_path.stem}.wav'
        m4a_audio_path = video_path.resolve().with_suffix(".m4a")
        if not m4a_audio_path.exists():
            audio_output_path = extract_audio_from_videos(
                video_path, audio_output_path)
        else:
            ffmpeg_cmd = [
                "ffmpeg", '-v', 'error',
                "-y", "-i", str(m4a_audio_path),
                str(audio_output_path)
            ]
            subprocess.run(ffmpeg_cmd, check=True)

        logging.info(f"Audio extracted to: {audio_output_path}")

        face_mask, face_emb, _, _, _ = image_processor.preprocess(
            images_output_dir)
        cv2.imwrite(
            str(dirs["face_mask"] / f"{video_path.stem}.png"), face_mask)
        torch.save(face_emb, str(
            dirs["face_emb"] / f"{video_path.stem}.pt"))
        audio_path = output_dir / "audios" / f"{video_path.stem}.wav"
        
        audio_emb, _ = audio_processor.preprocess(audio_path, fps=fps, expected_seq_len=121)
        torch.save(audio_emb, str(
            dirs["audio_emb"] / f"{video_path.stem}.pt"))
        
        ## 及时删除images文件夹，减少存储占用
        shutil.rmtree(images_output_dir)

    except Exception as e:
        logging.error(f"Failed to process video {video_path}: {e}")


def process_all_videos(input_video_list: List[Path], output_dir: Path) -> None:
    """
    Process all videos in the input list.

    Args:
        input_video_list (List[Path]): List of video paths to process.
        output_dir (Path): Directory to save the output.
        gpu_status (bool): Whether to use GPU for processing.
    """
    project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    face_analysis_model_path = project_root / "pretrained_models/face_analysis"
    landmark_model_path = project_root / "pretrained_models/face_analysis/models/face_landmarker_v2_with_blendshapes.task"
    audio_separator_model_file = project_root / "pretrained_models/audio_separator/Kim_Vocal_2.onnx"
    wav2vec_model_path = project_root / "pretrained_models/wav2vec/wav2vec2-base-960h"

    audio_processor = AudioProcessor(
        16000,
        wav2vec_model_path,
        False,
        os.path.dirname(audio_separator_model_file),
        os.path.basename(audio_separator_model_file),
        os.path.join(output_dir, "vocals"),
    )

    image_processor = ImageProcessorForDataProcessing(
        face_analysis_model_path, landmark_model_path)

    for video_path in tqdm(input_video_list, desc="Processing videos"):
        process_single_video(video_path, output_dir,
                             image_processor, audio_processor)


## 增加对json文件输入的支持
def get_video_paths(source: Union[Path, str], parallelism: int, rank: int) -> List[Path]:
    """
    Get paths of videos to process, partitioned for parallel processing.

    Args:
        source (Union[Path, str]): Source directory containing videos or a JSON file with video paths.
        parallelism (int): Level of parallelism.
        rank (int): Rank for distributed processing.

    Returns:
        List[Path]: List of video paths to process.
    """
    if isinstance(source, Path) and source.is_file() and source.suffix == '.json':
        # If the input is a JSON file, read video paths from it
        with open(source, 'r') as f:
            data = json.load(f)
        video_paths = sorted([Path(entry['video-path']) for entry in data if 'video-path' in entry and Path(entry['video-path']).exists()])
    else:
        # Otherwise, treat it as a directory and find all .mp4 files
        source_dir = Path(source)
        video_paths = [item for item in sorted(source_dir.iterdir()) if item.is_file() and item.suffix == '.mp4']
    
    # Partition the video paths for parallel processing
    if rank == 0:
        print(f"{len(video_paths)=}")
    return [video_paths[i] for i in range(len(video_paths)) if i % parallelism == rank]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process videos to prepare data for training. Run this script twice with different GPU status parameters."
    )
    parser.add_argument("-i", "--input", type=Path,
                        required=True, help="Directory containing videos or a JSON file with video paths")
    parser.add_argument("-o", "--output_dir", type=Path,
                        help="Directory to save results, default is parent dir of input dir")
    parser.add_argument("-p", "--parallelism", default=1,
                        type=int, help="Level of parallelism")
    parser.add_argument("-r", "--rank", default=0, type=int,
                        help="Rank for distributed processing")

    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = args.input.parent

    video_path_list = get_video_paths(
        args.input, args.parallelism, args.rank)

    if not video_path_list:
        logging.warning("No videos to process.")
    else:
        process_all_videos(video_path_list, args.output_dir)