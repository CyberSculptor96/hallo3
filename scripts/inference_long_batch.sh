#! /bin/bash
GPUS=$3
export CUDA_VISIBLE_DEVICES=$GPUS
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

environs="WORLD_SIZE=1 RANK=0 LOCAL_RANK=0 LOCAL_WORLD_SIZE=1"

export MASTER_PORT=$RANDOM
run_cmd="$environs python hallo3/sample_video.py --base ./configs/cogvideox_5b_i2v_s2.yaml ./configs/inference.yaml --seed $RANDOM --input-file $1 --output-dir $2"

echo ${run_cmd}
eval ${run_cmd}> ./runs/logs/inference_testset_${GPUS}.log 2>&1

echo "DONE on `hostname`"
