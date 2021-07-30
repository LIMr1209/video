import os
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download(video_url: str, path: str):
    '''
    下载抖音video
    :param url:
    :return:
    '''

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36'}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(video_url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length) or content_length == 0:
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('下载成功,file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


def start(url: str):
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\AutomationProfile"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    browser = webdriver.Chrome(options=chrome_options)
    # url = 'https://www.douyin.com/video/6969844956399668488?previous_page=main_page' # 横屏
    url = 'https://v.douyin.com/evq3qMW/'  # == 'https://www.douyin.com/video/6989560504071081247?previous_page=app_code_link' # app 竖屏
    browser.get(url)

    try:
        elem = WebDriverWait(browser, 20, 0.5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//video')
            )
        )
    except:
        print('错误')
        return
    video_url = browser.find_element_by_xpath('//video').get_attribute('src')
    print(video_url)
    author = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/a/div/span/span/span/span/span').get_attribute(
        'innerText')
    published_at = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/span').get_attribute('innerText')
    title = browser.title
    love_count = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/span').get_attribute('innerText')
    comment_count = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span').get_attribute('innerText')

    download(video_url, '{}.mp4'.format(title))


if __name__ == '__main__':
    # url = 'https://www.douyin.com/video/6969844956399668488?previous_page=main_page' # 横屏
    url = 'https://v.douyin.com/evq3qMW/'  # == 'https://www.douyin.com/video/6989560504071081247?previous_page=app_code_link' # app 竖屏
    start(url)
