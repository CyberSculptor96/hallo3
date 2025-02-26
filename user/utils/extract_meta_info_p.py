"""
    多线程加速版本
    @Author: huanghj
    @Date: 2025.02.08
"""
import argparse
import json
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import torch
from tqdm import tqdm


def collect_video_folder_paths(root_path: Path) -> list:
    """收集所有视频文件夹路径"""
    return [frames_dir.resolve() for frames_dir in root_path.iterdir() if frames_dir.is_dir()]


def construct_meta_info(frames_dir_path: Path) -> dict:
    """构建视频帧的元信息"""
    mask_path = str(frames_dir_path).replace("images", "face_mask") + ".png"
    face_emb_path = str(frames_dir_path).replace("images", "face_emb") + ".pt"
    audio_emb_path = str(frames_dir_path).replace("images", "audio_emb") + ".pt"
    video_path = str(frames_dir_path).replace("images", "videos") + ".mp4"
    caption_path = str(frames_dir_path).replace("images", "caption") + ".txt"

    # 检查文件是否存在
    if not os.path.exists(mask_path):
        return None
    if not os.path.exists(video_path):
        return None
    if not os.path.exists(caption_path):
        return None

    # 读取 face_emb 和 audio_emb 时进行错误处理
    try:
        face_emb = torch.load(face_emb_path)
        if face_emb is None:
            return None
    except Exception as e:
        print(f"Error loading face_emb {face_emb_path}: {e}", flush=True)
        return None

    try:
        audio_emb = torch.load(audio_emb_path)
        if audio_emb is None:
            return None
    except Exception as e:
        print(f"Error loading audio_emb {audio_emb_path}: {e}", flush=True)
        return None

    # 读取文本 caption
    try:
        with open(caption_path, 'r', encoding='utf-8') as file:
            caption = file.read().strip()
    except Exception as e:
        print(f"Error reading caption {caption_path}: {e}", flush=True)
        return None

    return {
        "video_path": video_path,
        "face_mask_union_path": mask_path,
        "face_emb_path": face_emb_path,
        "vocals_emb_base_all": audio_emb_path,
        "caption": caption
    }


def main():
    """主函数，提取元信息"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root_path", type=str, required=True, help="视频目录根路径")
    parser.add_argument("-n", "--dataset_name", type=str, required=True, help="数据集名称")
    parser.add_argument("--meta_info_name", type=str, help="输出 JSON 文件名称")
    parser.add_argument("-w", "--workers", type=int, default=8, help="并行线程数")

    args = parser.parse_args()

    if args.meta_info_name is None:
        args.meta_info_name = args.dataset_name

    image_dir = Path(args.root_path) / "images"
    output_dir = Path("./data")
    output_dir.mkdir(exist_ok=True)

    # 收集所有视频文件夹路径
    frames_dir_paths = collect_video_folder_paths(image_dir)

    meta_infos = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(construct_meta_info, path): path for path in frames_dir_paths}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Videos"):
            result = future.result()
            if result:
                meta_infos.append(result)

    # 写入 JSON
    output_file = output_dir / f"{args.meta_info_name}.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(meta_infos, f, indent=4)

    print(f"Final data count: {len(meta_infos)}")


if __name__ == "__main__":
    main()
