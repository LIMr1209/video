import json
import os
import time
from urllib.parse import urlparse, unquote
import re

import requests
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',  # noqa
}


def download(video_url: str, path: str):
    """
    下载抖音video
    :param video_url: 视频链接
    :return:
    """

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
                    os.path.exists(path) and os.path.getsize(path) >= content_length) or content_length == 0:
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('下载成功,%s file size : %d   total size:%d' % (path, os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


def browser_init():
    """
    初始化浏览器
    """
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\AutomationProfile"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    browser = webdriver.Chrome(options=chrome_options)

    # chrome_options = Options()
    # # chrome_options.add_argument("--headless")  # 无头浏览器
    # # 这些网站识别不出来你是用了Selenium，因此需要将模拟浏览器设置为开发者模式
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # # ua = UserAgent().random
    # # chrome_options.add_argument("user-agent={}".format(ua))
    # #
    # # 其中PageLoadStrategy有三种选择： 默认normal
    # # (1) NONE: 当html下载完成之后，不等待解析完成，selenium会直接返回
    # # (2) EAGER: 要等待整个dom树加载完成，即DOMContentLoaded这个事件完成，仅对html的内容进行下载解析
    # # (3) NORMAL: 即正常情况下，selenium会等待整个界面加载完成（指对html和子资源的下载与解析,如JS文件，图片等，不包括ajax）
    # caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "normal"  # complete
    # # caps["pageLoadStrategy"] = "eager"  #interactive
    # # caps["pageLoadStrategy"] = "none"
    # # 初始化chrome对象
    # browser = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
    # browser.maximize_window()
    # browser.set_page_load_timeout(10)  # 页面加载超时时间
    # browser.set_script_timeout(10)  # 执行js 超时时间
    # WebDriverWait(browser, 30)  # 指定元素加载超时时间
    return browser

def start_detail_new(url: str = None):
    response = requests.get(url, headers=fake_headers)
    page_content = unquote(response.text)
    title = re.findall(r'"desc":"([^"]*)"', page_content)[0].strip()
    # video URLs are in this pattern {"src":"THE_URL"}, in json format
    urls_pattern = r'"playAddr":(\[.*?\])'
    urls = json.loads(re.findall(urls_pattern, page_content)[0])
    video_url = 'https:' + urls[0]['src']
    current_folder = os.getcwd()
    target_folder = os.path.join(current_folder, 'download', 'detail')
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)
    path = os.path.join(target_folder, '{}.mp4'.format(title))
    download(video_url, path)



def start_detail(url: str = None):
    """
    :param url: 详情页url
    :return:
    """
    browser = browser_init()
    browser.get(url)
    try:
        elem = WebDriverWait(browser, 20, 0.5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//video')
            )
        )
    except Exception as e:
        print('错误')
        return
    video_url = browser.find_element_by_xpath('//video').get_attribute('src')
    # author = browser.find_element_by_xpath(
    #     '//*[@id="root"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/a/div/span/span/span/span/span').get_attribute(
    #     'innerText')
    # published_at = browser.find_element_by_xpath(
    #     '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/span').get_attribute('innerText')
    title = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/h1/span[2]/span[1]/span/span/span').get_attribute('innerText')
    # love_count = browser.find_element_by_xpath(
    #     '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[1]/span').get_attribute('innerText')
    # comment_count = browser.find_element_by_xpath(
    #     '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span').get_attribute('innerText')
    current_folder = os.getcwd()
    target_folder = os.path.join(current_folder, 'download', 'detail')
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)
    path = os.path.join(target_folder, '{}.mp4'.format(title))
    download(video_url, path)


def start_user(user_url: str = None, account_name: str = None, sec_uid: str = None):
    """
    :param user_url: 用户主页url
    :param sec_uid: 用户id
    :param account_name: 用户账户名称
    :return:
    """
    if not user_url and not sec_uid and not account_name:
        print('参数错误')
        return
    if user_url:
        sec_uid = user_url.split('?')[0].rsplit('/', 1)[1]
    elif account_name:
        try:
            browser = browser_init()
            browser.get("https://www.douyin.com/search/%s?source=search_history&type=user" % account_name)
            try:
                elem = WebDriverWait(browser, 20, 0.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div[3]/ul/li[1]/a/div[2]/span[1]/span')
                    )
                )
            except:
                browser.refresh()
                time.sleep(5)
            account_name_search = browser.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div/div[2]/div[3]/ul/li[1]/a/div[2]/span[1]/span').get_attribute(
                'innerText')
            if account_name_search != account_name:
                print("搜索错误")
                return
            user_url = browser.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div/div[2]/div[3]/ul/li[1]/a').get_attribute('href')
            sec_uid = user_url.split('?')[0].rsplit('/', 1)[1]
        except:
            print("搜索错误")
            return
    # api_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAA4N4OrZzTSmCPp8vVAqCeyU215Kav2JgFv2Lfy4DNWRs&count=21&max_cursor=0&aid=1128&_signature=QOtJJBARHVwzHUNLqlT-mEDrST&dytk=593d265a74e3384e06112b423ef268da'
    api_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    }
    params = {
        'sec_uid': sec_uid,
        'count': '21',
        'max_cursor': '0',
        'aid': '1128',
        '_signature': 'QOtJJBARHVwzHUNLqlT-mEDrST',
        'dytk': '593d265a74e3384e06112b423ef268da'
    }
    max_cursor, video_count = None, 0
    while True:
        if max_cursor:
            params['max_cursor'] = max_cursor
        res = requests.get(api_url, headers=headers,
                           params=params)
        result = json.loads(res.content.decode('utf-8'))
        aweme_list = result.get('aweme_list', [])
        for aweme in aweme_list:
            video_url = aweme['video']['play_addr']['url_list'][-1]
            video_count += 1
            author_name = aweme['author']['nickname']
            title = aweme['desc']
            current_folder = os.getcwd()
            target_folder = os.path.join(current_folder, 'download', author_name)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            path = os.path.join(target_folder, '{}.mp4'.format(title))
            download(video_url, path)
        if result.get('has_more'):
            max_cursor = result.get('max_cursor')
        else:
            break

def start_collect_new(collect_url: str=None, collect_id: int=None):
    if not collect_url and not collect_id:
        print("参数错误")
        return
    if collect_url:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        }
        result = urlparse(collect_url)
        if result.hostname == 'v.douyin.com':
            res = requests.get(collect_url, headers=headers)
            collect_url = res.history[0].headers['location']
        collect_id = collect_url.split('?')[0].rsplit('/', 2)[1]
    template_url = 'https://www.douyin.com/collection/%s?pos=%s'
    pos = 0
    current_folder = os.getcwd()
    target_folder = os.path.join(current_folder, 'download', 'collect', 'test')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    while True:
        url = template_url % (collect_id, pos)
        response = requests.get(url, headers=fake_headers)
        page_content = unquote(response.text)
        if '你要观看的视频不存在' in page_content:
            print('合集爬取完成')
            return
        title = re.findall(r'"desc":"([^"]*)"', page_content)[0].strip()
        # video URLs are in this pattern {"src":"THE_URL"}, in json format
        urls_pattern = r'"playAddr":(\[.*?\])'
        urls = json.loads(re.findall(urls_pattern, page_content)[0])
        video_url = 'https:' + urls[0]['src']
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, 'download', 'detail')
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)
        path = os.path.join(target_folder, '{}.mp4'.format(title))
        download(video_url, path)


def start_collect(collect_url: str=None, collect_id: int=None):
    """
    :param collect_url: 合集链接
    :param collect_id: 合集ID
    :return:
    """
    if not collect_url and not collect_id:
        print("参数错误")
        return
    if collect_url:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        }
        result = urlparse(collect_url)
        if result.hostname == 'v.douyin.com':
            res = requests.get(collect_url, headers=headers)
            collect_url = res.history[0].headers['location']
        collect_id = collect_url.split('?')[0].rsplit('/', 2)[1]
    template_url = 'https://www.douyin.com/collection/%s?pos=%s'
    browser = browser_init()
    pos = 0
    current_folder = os.getcwd()
    browser.get(template_url % (collect_id, 0))
    collect_title = browser.title
    target_folder = os.path.join(current_folder, 'download', 'collect', collect_title )
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    while True:
        url = template_url % (collect_id, pos)
        browser.get(url)
        if '你要观看的视频不存在' in browser.page_source:
            print('合集爬取完成')
            return
        try:
            elem = WebDriverWait(browser, 20, 0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//video')
                )
            )
        except Exception as e:
            print('错误')
            return
        video_url = browser.find_element_by_xpath('//video').get_attribute('src')
        title = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/h1').get_attribute('innerText')
        title = title.replace('|','-').replace(' ','')
        path = os.path.join(target_folder, '{}.mp4'.format(title))
        download(video_url, path)
        pos += 1


if __name__ == '__main__':
    # detail_url = 'https://www.douyin.com/video/6969844956399668488?previous_page=main_page' # 横屏
    # detail_url = 'https://v.douyin.com/evq3qMW/'  # == 'https://www.douyin.com/video/6989560504071081247?previous_page=app_code_link' # app 竖屏
    # start_detail(detail_url)
    # start_detail_new(detail_url)
    # author_url = 'https://www.douyin.com/user/MS4wLjABAAAA4N4OrZzTSmCPp8vVAqCeyU215Kav2JgFv2Lfy4DNWRs'
    start_user(account_name="mei9578")
    # collect_url = 'https://www.douyin.com/collection/6990254672946661413'
    # collect_url = 'https://v.douyin.com/ect8xBe/'
    # start_collect(collect_url)
