
import yaml
import argparse
import subprocess
import os
import sys
from collections import defaultdict

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

def parse_arguments():
    """
    自定义解析命令行参数，支持动态的模块和其对应的标签。
    例如:
        test.py -cpu ut it -npu it -mini-test
    """
    args = sys.argv[1:]
    modules = defaultdict(list)
    current_module = None

    for arg in args:
        if arg.startswith('-'):
            # 去除前导'-'，作为模块名称
            current_module = arg.lstrip('-')
            # 对于像 'mini-test' 这样的模块，如果不需要额外标签，则可以保留为空列表
            modules[current_module] = []
        else:
            if current_module is None:
                print(f"未识别的参数: {arg}")
                sys.exit(1)
            modules[current_module].append(arg)

    return modules

def filter_tests(tests, module_filters):
    """
    根据模块过滤器筛选测试。
    module_filters 是一个字典，键是模块名称，值是该模块下的标签列表。
    """
    selected_tests = set()

    for module, labels in module_filters.items():
        for test in tests:
            test_labels = test.get('labels', [])
            if module not in test_labels:
                continue
            if labels:
                # 如果指定了标签，则测试必须包含模块标签和至少一个指定标签
                if any(label in test_labels for label in labels):
                    selected_tests.add(test['name'])
            else:
                # 如果没有指定标签，则测试只需要包含模块标签
                selected_tests.add(test['name'])

    # 根据测试名称从测试列表中获取完整的测试配置
    final_tests = [test for test in tests if test['name'] in selected_tests]
    return final_tests

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
    module_filters = parse_arguments()

    # 加载测试配置
    pwd_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(pwd_dir, 'testlist.yaml')
    tests = load_tests(yaml_path)
    if not tests:
        print("没有找到任何测试配置。")
        sys.exit(0)

    # 筛选测试
    selected_tests = filter_tests(tests, module_filters)

    if not selected_tests:
        print("没有匹配的测试。")
        sys.exit(0)

    # 执行测试
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
