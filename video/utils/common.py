def cookie_to_dict(cookie: str) -> dict:
    '''
    cookies 字符串转字典
    :param cookie: cookie 字符
    :return: cookie字典
    '''
    return {item.split('=')[0]: item.split('=')[1] for item in cookie.split('; ')}


def dict_to_cookie(data: dict) -> str:
    '''
    cookie 字典转字符串
    :param data: cookie字典
    :return: cookie 字符
    '''
    cookie = ''
    for key, value in data.items():
        cookie += key + '=' + value + ';'
    cookie = cookie[:-1]
    return cookie
