import os
import json
from playwright.sync_api import sync_playwright

def punch(cookie_str):
    with sync_playwright() as p:
        # 启动无头浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 解析并注入 Cookie
        cookies = []
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.luogu.com.cn',
                    'path': '/'
                })
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        # 访问签到接口，Playwright 会自动执行 JS 挑战
        page.goto("https://www.luogu.com.cn/index/ajax_punch", wait_until="networkidle")
        
        # 等待挑战完成并加载最终内容
        page.wait_for_timeout(5000) 
        
        # 获取页面最终文本（挑战通过后通常会返回 JSON 或重定向）
        content = page.inner_text("body")
        browser.close()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content

if __name__ == "__main__":
    uid = os.getenv('LUOGU_UID')
    client_id = os.getenv('LUOGU_CLIENT_ID')
    c3vk = os.getenv('LUOGU_C3VK')
    
    if not all([uid, client_id, c3vk]):
        print("错误：请设置环境变量")
        exit(1)

    cookie = f"__client_id={client_id}; _uid={uid}; _C3VK={c3vk}"
    result = punch(cookie)
    print(result)
