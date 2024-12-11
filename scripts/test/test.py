import yaml
import argparse
import subprocess
import os
import sys


zipper_path = os.environ.get('CI_ZIPPER_PATH')
def load_tests(yaml_path):
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data.get('tests', [])
    except FileNotFoundError:
        print(f"YAML 配置文件未找到: {yaml_path}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"解析 YAML 文件时出错: {exc}")
        sys.exit(1)

def filter_tests(tests, labels=None, folder=None):
    filtered = tests
    if labels:
        # 仅保留包含所有指定标签的测试
        filtered = [
            test for test in filtered
            if test.get('labels') and all(label in test['labels'] for label in labels)
        ]
    if folder:
        filtered = [test for test in filtered if test.get('folder') == folder]
    return filtered

def execute_command(command, cwd):
    try:
        print(f"执行命令: {command} (在 {cwd})")
        cwd = os.path.join(zipper_path, cwd)
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"命令输出:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"命令 '{command}' 执行失败，错误信息:\n{e.stderr}")

def main():
    parser = argparse.ArgumentParser(description="根据 YAML 配置执行测试")
    parser.add_argument(
        '--labels',
        nargs='+',
        help='筛选测试的标签（可以指定多个标签，必须同时满足）'
    )
    parser.add_argument('--folder', type=str, help='筛选测试的文件夹')
    parser.add_argument('--yaml', type=str, default='tests.yaml', help='YAML 配置文件路径')
    args = parser.parse_args()

    tests = load_tests(args.yaml)
    if not tests:
        print("没有找到任何测试配置。")
        sys.exit(0)

    selected_tests = filter_tests(tests, labels=args.labels, folder=args.folder)

    if not selected_tests:
        print("没有匹配的测试。")
        sys.exit(0)

    for test in selected_tests:
        labels = test.get('labels', [])
        folder = test.get('folder', '.')
        command = test.get('command')
        name = test.get('name', 'Unnamed Test')

        print(f"\n=== 执行测试: {name} ===")
        print(f"标签: {', '.join(labels)}")
        execute_command(command, folder)

if __name__ == "__main__":
    main()
