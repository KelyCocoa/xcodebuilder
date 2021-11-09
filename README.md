## xcodebuilder简介
- xcodebuilder通过python脚本实现iOS打包上传fir.im测试以及上传AppStore connect。
- 运行环境为Mac操作系统 python3.8，python虚拟环境使用pipenv。

## 快速上手
```
# 如果没有安装虚拟环境需要先安装pipenv
pip install pipenv
# cd到xcodebuilder目录通过虚拟环境安装所需要的包
pipenv install
# 在config模块，ExportOptions_dev.plist和ExportOptions_prod.plist配置自己的相关配置信息
# --deploy=dev打测试包上传fir.im --deploy=prod打正式包上传appstore --deploy=dev&prod both
python3 index.py --deploy=dev
# python3 index.py -h 查看更多相关命令
```