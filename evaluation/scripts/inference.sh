#! /bin/bash

use_origin=0
ckpt="1"
gpu_id=0

if [ $use_origin -eq 1 ]; then
    echo "Using hallo3-origin"
else
    echo "Using sft-stage2->1, ckpt=${ckpt}"
fi

input_dir="./evaluation/dataset/HDTF/inputs"
output_base="./evaluation/dataset/HDTF/outputs_trained"
log_dir="./runs/logs"
mkdir -p ${log_dir}

for i in $gpu_id; do
    input_file="${input_dir}/input_22-${i}.txt"
    output_dir="${output_base}/card${i}"
    gpu_id=$i

    export CUDA_VISIBLE_DEVICES=${gpu_id}
    export MASTER_PORT=$((RANDOM % 10000 + 20000))  # 避免端口冲突

    echo "[GPU ${gpu_id}] Processing ${input_file}..."

    run_cmd="WORLD_SIZE=1 RANK=0 LOCAL_RANK=0 LOCAL_WORLD_SIZE=1 \
python hallo3/sample_video.py \
--base ./configs/cogvideox_5b_i2v_s2.yaml ./configs/inference.yaml \
--seed $RANDOM \
--input-file ${input_file} \
--output-dir ${output_dir}"

    # 启动后台运行，并重定向日志
    eval ${run_cmd} > "${log_dir}/inference_testset_${i}.log" 2>&1 &

    sleep 1  # 避免太快启动，端口冲突
done

wait
echo "✅ All inference jobs finished on `hostname`"
