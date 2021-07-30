基于[Scrapy](https://scrapy.org/ "scrapy官网")框架的网络爬虫系统
===


### 项目部署说明
- [环境配置](#环境配置)
- [爬虫创建](#爬虫创建)


### 环境配置
Python虚拟环境配置
Python3.6.5+
- 把根目录文件```.env_example```复制到根目录```.env```，作为当前环境的配置文件  
- 把根目录文件```.gitignore_example```复制到根目录```.gitignore```，作为当前环境的忽略文件  
```Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```


### 爬虫创建
- 创建爬虫(一般使用网站域名进行命名)
```Bash
scrapy genspider -t basic example 'example.com'
```
- 爬取数据字段设置(video/items.py)
- 爬取的数据处理程序(video/piplines.py)
