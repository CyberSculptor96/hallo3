## 必须首先cd进入某目录，再执行删除操作！！

dirs=$(find . -maxdepth 1 -type d | tail -n +2 | head -n 10000)
total=$(echo "$dirs" | wc -l)
count=0

for dir in $dirs; do
    rm -rf "$dir"
    count=$((count + 1))
    printf "\rProgress: [%-50s] %d%%" $(printf '#%.0s' $(seq 1 $((count * 50 / total)))) $((count * 100 / total))
done
echo -e "\nDone!"
