#! /bin/bash
CUDA_VISIBLE_DEVICES="4,5,6,7"
echo "RUN on $(hostname), CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

PORT=24507
run_cmd="PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True torchrun --standalone --nproc_per_node=4 --master_port=$PORT hallo3/train_video.py --wandb --base configs/cogvideox_5b_i2v_s2.yaml configs/sft_s2.yaml --seed $RANDOM"

echo ${run_cmd}
eval ${run_cmd} > ./runs/logs/stage2.2.log 2>&1

echo "DONE on `hostname`"