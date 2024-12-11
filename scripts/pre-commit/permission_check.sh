#!/bin/bash

# 防止脚本被多次执行时重复打印日志
if [ "$PRE_COMMIT_ALREADY_RUN" = "true" ]; then
    exit 0
fi


# 定义不允许修改的目录
PROTECTED_DIRS=( \
    "src/core0" \
    "src/core1-4" \
    "src/core5" \
    "src/npu" \
    "src/sys" \
)

# 获取将要提交的修改文件
CHANGED_FILES=$(git diff --cached --name-only)

echo "将要提交的文件:"
echo "$CHANGED_FILES"

echo "[修改权限检查]==========================="

PROTECTED_MODIFIED=false
# 检查每个修改的文件是否在受保护的目录中
for FILE in $CHANGED_FILES; do
    for DIR in "${PROTECTED_DIRS[@]}"; do
        if [[ "$FILE" == $DIR/* ]]; then
            echo "ERROR: 不允许修改目录 $DIR 中的文件。ERROR文件：$FILE。"
            PROTECTED_MODIFIED=true
        fi
    done
done

if [[ "$PROTECTED_MODIFIED" = "true" ]]; then
    echo "[检查修改权限未通过]====================="
    exit 1
fi

echo "[检查修改权限通过]====================="
exit 0
