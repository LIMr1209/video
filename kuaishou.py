import os
from urllib.parse import urlparse

import requests


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


def get_item_id(url, headers):
    '''
    获取快手详情url  item_id
    :param url: 抖音链接
    :param headers: 请求头
    :return:
    '''
    result = urlparse(url)
    if result.hostname == 'v.kuaishou.com':
        res = requests.get(url, headers=headers)
        url = res.url
    item_id = url.split('?')[0].rsplit('/', 1)[1]
    return item_id


def start(url: str):
    '''
    开始
    :param url: 快手链接
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    }

    item_id = get_item_id(url, headers)

    data = {'operationName': 'visionVideoDetail', 'variables': {'photoId': item_id, 'page': 'detail'},
            'query': 'query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {    status    type    author {      id      name      following      headerUrl      __typename    }    photo {      id      duration      caption      likeCount      realLikeCount      coverUrl      photoUrl      liked      timestamp      expTag      llsid      viewCount      videoRatio      stereoType      croppedPhotoUrl      manifest {        mediaType        businessType        version        adaptationSet {          id          duration          representation {            id            defaultSelect            backupUrl            codecs            url            height            width            avgBitrate            maxBitrate            m3u8Slice            qualityType            qualityLabel            frameRate            featureP2sp            hidden            disableAdaptive            __typename          }          __typename        }        __typename      }      __typename    }    tags {      type      name      __typename    }    commentLimit {      canAddComment      __typename    }    llsid    danmakuSwitch    __typename  }}'}
    res = requests.post('https://www.kuaishou.com/graphql', json=data, headers=headers)
    result = res.json()
    video_url = result['data']['visionVideoDetail']['photo']['photoUrl']
    title = result['data']['visionVideoDetail']['photo']['caption']
    love_count = result['data']['visionVideoDetail']['photo']['likeCount']
    view_count = result['data']['visionVideoDetail']['photo']['viewCount']
    tags = result['data']['visionVideoDetail']['tags']
    author = result['data']['visionVideoDetail']['author']['name']

    download(video_url, '{}.mp4'.format(title))


if __name__ == '__main__':
    url = 'https://v.kuaishou.com/cLHMJI'
    # url = 'https://www.kuaishou.com/short-video/3xk5waye24pfxn6?authorId=3xhfyp6fexi2476&streamSource=find&area=homexxbrilliant'
    start(url)
