import you_get
import sys
from you_get import common as you_get       # 导入you-get库

# 设置下载目录
directory = r'C:\Users\aaa10\Desktop\project\video'
# 要下载的视频地址
url = 'https://v.douyin.com/evq3qMW/'
# 传参数
sys.argv = ['you-get', '-o', directory, url]

you_get.main()
