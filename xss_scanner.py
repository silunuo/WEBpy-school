#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
#  author:lwl
#  Collaborator:cr and lx and tyf

import requests
from bs4 import BeautifulSoup
import re

def detect_xss(url):
    try:
        # 测试payload
        payloads = [
            "<script>alert('XSS1')</script>",
            "<img src=x onerror=alert('XSS2')>",
            "'\"><script>alert('XSS3')</script>",
            "javascript:alert('XSS4')",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTNScpPC9zY3JpcHQ+"
        ]
        vulnerabilities = []
        # 测试GET参数
        parsed_url = requests.compat.urlparse(url)
        query = parsed_url.query
        if query:
            # 测试每个参数
            for param in re.split(r'[&;]', query):
                if '=' in param:
                    key, value = param.split('=', 1)
                    for payload in payloads:
                        test_url = url.replace(f"{key}={value}", f"{key}={payload}")
                        response = requests.get(test_url, timeout=10)
                        if payload in response.text:
                            vulnerabilities.append(f"反射型XSS (GET参数): {key}={payload}")

        # 测试表单
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')

        for form in forms:
            form_action = form.get('action')
            form_method = form.get('method', 'get').lower()

            inputs = {}
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                input_type = input_tag.get('type', 'text').lower()
                if name and input_type in ['text', 'hidden', 'search', 'email', 'password']:
                    inputs[name] = payloads[0]  # 使用第一个payload测试

            if form_action and inputs:
                target_url = requests.compat.urljoin(url, form_action)

                try:
                    if form_method == 'post':
                        res = requests.post(target_url, data=inputs, timeout=10)
                    else:
                        res = requests.get(target_url, params=inputs, timeout=10)

                    for payload in payloads:
                        if payload in res.text:
                            vulnerabilities.append(f"存储型XSS (表单): {list(inputs.keys())[0]}={payload}")
                except Exception as e:
                    continue

        # 测试链接属性
        for tag in soup.find_all(['a', 'img', 'iframe']):
            for attr in ['href', 'src', 'data', 'onload', 'onerror']:
                attr_value = tag.get(attr, '')
                if attr_value:
                    for payload in payloads:
                        if payload in attr_value:
                            vulnerabilities.append(f"基于属性的XSS: {tag.name} {attr}={payload}")

        if vulnerabilities:
            return "发现XSS漏洞:\n" + "\n".join(vulnerabilities)
        return "未发现XSS漏洞"

    except Exception as e:
        return f"检测失败: {str(e)}"