import os
import shutil
import yaml
import argparse
import sys

def load_config(config_path=None):
    """ 加载配置文件, 默认使用脚本所在路径的 client_config.yaml。"""
    if config_path is None:
        pwd_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(pwd_dir, 'client_config.yaml')

    if not os.path.exists(config_path):
        print(f"Configuration file does not exist: {config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)

def copy_files(source_base, target_base, mappings, direction):
    """ 根据映射关系复制文件或目录。"""
    for mapping in mappings:
        project_path = mapping.get('project')
        zipper_path = mapping.get('zipper')

        if not project_path or not zipper_path:
            print(f"Invalid mapping: {mapping}")
            continue

        if direction == 'project_to_zipper': # separate
            source = os.path.join(source_base, project_path)
            target = os.path.join(target_base, zipper_path)
        elif direction == 'zipper_to_project': # join            
            source = os.path.join(source_base, zipper_path)
            target = os.path.join(target_base, project_path)

        try:
            if os.path.isdir(source):
                if os.path.exists(target):
                    shutil.rmtree(target)
                shutil.copytree(source, target)
                print(f"Copied directory: {source} -> {target}")
            elif os.path.isfile(source):
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(source, target)
                print(f"Copied file: {source} -> {target}")
            else:
                print(f"Source path does not exist or is invalid: {source}")
        except Exception as e:
            print(f"Failed to copy: {source} -> {target}. Error: {e}")

def separate(config):
    """ 生成用于提交 GitHub 的代码。"""
    source = config['project_path']
    target = config['zipper_path']
    mappings = config.get('file_mappings', [])

    if not mappings:
        print("No file mappings defined.")
        sys.exit(1)

    os.makedirs(target, exist_ok=True)
    copy_files(source, target, mappings, direction='project_to_zipper')
    print(f"Code has been separated to: {target}")

def join(config):
    """ 通过Zipper更新本地代码 """
    source = config['zipper_path']
    target = config['project_path']
    mappings = config.get('file_mappings', [])

    if not mappings:
        print("No file mappings defined.")
        sys.exit(1)

    os.makedirs(target, exist_ok=True)
    copy_files(source, target, mappings, direction='zipper_to_project')
    print(f"Code has been merged to: {target}")
def main():
    parser = argparse.ArgumentParser(description="Extract code to CI-Zipper")
    parser.add_argument(
        'action',
        choices=['client-separate', 'client-join'],
        help="Choose action type: 'client-separate' extract project code to Zipper for commit,\n 'client-join' update project from Zipper."
    )
    parser.add_argument(
        '--config',
        default=None,
        help="Path to configuration file (default: client_config.yaml)"
    )

    args = parser.parse_args()
    config = load_config(args.config)

    if args.action == 'client-separate':
        separate(config)
    elif args.action == 'client-join':
        join(config)
    else:
        print("Invalid action type.")
        sys.exit(1)

if __name__ == "__main__":
    main()
