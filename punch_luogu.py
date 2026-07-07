import os
import json
from curl_cffi import requests as cffi_requests  # 👈 替换为 curl_cffi

def makeHead(cookie):
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.luogu.com.cn/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "Cookie": cookie
    }

def punch(cookie):
    url = "https://www.luogu.com.cn/index/ajax_punch"
    
    # 👇 关键：impersonate="chrome" 会模拟真实 Chrome 的 TLS/HTTP2 指纹
    # 同时自动设置正确的 User-Agent，无需手动指定
    response = cffi_requests.get(
        url,
        headers=makeHead(cookie),
        impersonate="chrome124"  # 模拟 Chrome 124 的完整指纹
    )
    response.encoding = 'utf-8'
    
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text

if __name__ == "__main__":
    uid = os.getenv('LUOGU_UID')
    client_id = os.getenv('LUOGU_CLIENT_ID')
    c3vk = os.getenv('LUOGU_C3VK')
    
    if not all([uid, client_id, c3vk]):
        print("错误：请设置环境变量 LUOGU_UID、LUOGU_CLIENT_ID 和 LUOGU_C3VK")
        exit(1)

    cookie = f"__client_id={client_id}; _uid={uid}; _C3VK={c3vk}"
    result = punch(cookie)
    print(result)
