# CI-Zipper

CI-Zipper本质是个即插即用的CI小工具，当作一个插件下到`本地环境/测试服务器`即可进行提交/合并代码的管理。
我把它称为Zipper，在本地开发环境（Client）我们通过Separating分离出要提交的代码，在测试服务器（server）我们通过Joining将这段代码再缝进去。 

### 目录结构


### Quick Start

1. 下载仓库并配置环境依赖

```
git clone https://github.com/SEU-ACAL/CI-Zipper.git
cd CI-Zipper
pip install -r requirements.txt
pre-commit install
```

2. Client端配置`client_config.yaml`：
- ~~修改 `source_repo_path` 与 `separate_target_path` 为你本地的绝对路径~~
- 检查 `file_mappings` 的对应关系

3. 运行 `ci_client.py`脚本
```
python ./scripts/ci/ci_client.py client-seperate/client-join
```

4. (仅用于CI测试，开发情况下无需使用) Server端配置`server_config.yaml`：
-~~ 修改 `source_repo_path` 与 `join_target_path` 为测试服务器的绝对路径~~
- 检查 `file_mappings` 的对应关系

5. (仅用于CI测试，开发情况下无需使用) 运行 `ci_server.py`脚本
```
python ./scripts/ci/ci_server.py server-join
```

### Configuration and Commands Explanation

1. `ci_client.py`
   - client-seperate: 分离出要提交的代码
   - client-join: 合并代码到测试环境
   - --config: 配置文件路径(当你移动了yaml的config文件时，才需要单独指定)

2. `ci_server.py`
   - server-join: 合并代码到测试环境
   - --config: 配置文件路径(当你移动了yaml的config文件时，才需要单独指定)
