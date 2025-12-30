#!/bin/bash

# 检查输入参数是否正确
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <CUDA_VISIBLE_DEVICES>"
  exit 1
fi

# 设置使用的 GPU
GPUS=$1
export CUDA_VISIBLE_DEVICES=$GPUS
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

# 配置随机端口
export MASTER_PORT=$RANDOM

# 定义输出目录
OUTPUT_DIR="/wangbenyou/shunian/workspace/talking_face/evaluation/videos/hallo3"

# 创建日志目录
LOG_DIR="./runs/log"
mkdir -p $LOG_DIR

# 运行命令
run_cmd="python hallo3/sample_video.py --base ./configs/cogvideox_5b_i2v_s2.yaml ./configs/inference.yaml --output-dir $OUTPUT_DIR"

echo ${run_cmd}
eval ${run_cmd} > $LOG_DIR/inference_testset_${GPUS}.log 2>&1

echo "DONE on `hostname`"
