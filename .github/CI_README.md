# CI 流程说明


目前CI依次进行以下检查流程

### check 提交污染
依据`<change:xxx>`标签进行判断
权限修改部分:
-  `<change:CPU>` 可修改`hardware/cpu`文件夹下文件
-  `<change:NPU>` 可修改`hardware/npu`文件夹下文件
-  `<change:test>` 可修改`test`文件夹下文件
其余文件夹为公开修改

如要添加额外文件夹，请联系`@shirohasuki`修改CI

### Complie lint

### UT (如Cache, 脉动阵列....)

### IT (CPU, NPU)

### 接口验证

### ST (大型workload/benchmark)

### FPGA仿真（后期加入）