import requests
import os
import json

def makeHead(cookie):
    return {
        "Host": "www.luogu.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "identity",  # 👈 关键：禁止服务器压缩响应
        "Connection": "keep-alive",
        "Referer": "https://www.luogu.com.cn/",  # 已修正多余空格
        "Cache-Control": "no-cache",
        "TE": "Trailers",
        "Cookie": cookie
    }

def punch(cookie):
    url = "https://www.luogu.com.cn/index/ajax_punch"  # 已修正多余空格
    response = requests.get(url, headers=makeHead(cookie))
    response.encoding = 'utf-8'
    # 使用 try-except 捕获 JSON 解析错误
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return response.text

if __name__ == "__main__":
    uid = os.getenv('LUOGU_UID')
    client_id = os.getenv('LUOGU_CLIENT_ID')
    c3vk = os.getenv('LUOGU_C3VK')
    if not all([uid, client_id, c3vk]):
        print("错误：请设置环境变量 LUOGU_UID、LUOGU_CLIENT_ID 和 LUOGU_C3VK")
        exit(1)

    cookie = f"__client_id={client_id}; _uid={uid}; _C3VK={c3vk};"
    result = punch(cookie)
    print(result)
