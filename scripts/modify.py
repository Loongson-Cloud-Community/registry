import re
import os
import sys
from packaging import version

def modify_dockerfile(dockerfile_content):
    """
    1. ARG GO_VERSION=1.16.15
    如果版本小于19 默认修改到19
    2. ARG GORELEASER_XX_VERSION=1.11
    统一成1.11
    """
    lines = dockerfile_content.splitlines()
    modified_lines = []

    # 1. 在第一行前面添加 '#'
    if lines:
        modified_lines.append(f"#{lines[0]}")
        remaining_lines = lines[1:]
    else:
        remaining_lines = []
    
    go_version_pattern = re.compile(r'^ARG\s+GO_VERSION\s*=\s*(\d+(?:\.\d+){0,2})')
    goreleaser_pattern = re.compile(r'^ARG\s+GORELEASER_XX_VERSION\s*=.*')

    for line in remaining_lines:
        # 修改 GO_VERSION
        match = go_version_pattern.match(line)
        if match:
            current_ver = match.group(1)
            # 取主版本号（如果是 1.16.15 这样形式，只提取 major.minor）
            ver = version.parse(current_ver)
            if ver < version.parse("19"):
                line = "ARG GO_VERSION=19"
            modified_lines.append(line)
            continue

        # 修改 GORELEASER_XX_VERSION
        if goreleaser_pattern.match(line):
            line = "ARG GORELEASER_XX_VERSION=1.11"
            modified_lines.append(line)
            continue

        # 其他保持不变
        modified_lines.append(line)

    return "\n".join(modified_lines)


#python3 *.py <path>
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python modify_dockerfile.py <Dockerfile路径>")
        print("示例: python modify_dockerfile.py ./Dockerfile")
        sys.exit(1)  # 退出程序，表示错误

    path = sys.argv[1]


    if not os.path.exists(path):
        print(f"错误: 文件 '{path}' 不存在。")
        sys.exit(1)
    else:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                dinput = f.read()

            modifed_context = modify_dockerfile(dinput)

            print(modifed_context)

        except Exception as e:
            print(f"处理文件时发生错误: {e}")
            sys.exit(1)
