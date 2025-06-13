<div align="center">
<h1>Flask-Requests-SQL\XSS-CH</h1>
网页爬虫与漏洞检测自动化系统<br><br>

![LOGO](./static/img/SUNb.png)

[**English**](./static/lan/README.en.md) | [**中文简体**](./README.md) 

</div>

> 无参考，根据公共网络的依赖库开发文档学习自行编写制作，放心使用 
>
## 简介
本仓库具有以下特点
+ 基于FLASK框架的简洁美观的网页界面
+ 使用Requests作为网络爬虫依赖
+ 利用pymysql实现前后端数据传输，遗憾并未编写读取本地数据库的程序
+ 对爬取的网页可进行常见XSS漏洞检测和SQL注入漏洞
+ 检测框架扩展性尚可，使用者可自行扩展检测内容

## 项目结构
```bash
WEBpy-school/
├── static/
│   ├── css/
│   │   └── style.css       # 前端样式
│   ├── img/
│   │   ├── SUNc.png        # 项目Logo
│   │   └── SUNb.png        # 项目Logo
│   └── lan/
│       └── README.en.md    # 非本土语言项目文档
├── templates/
│   ├── index.html          # 主界面
│   ├── logs.html           # 日志页面
│   └── scan_result.html    # 扫描结果页面
├── app.py                  # Flask主应用
├── crawler.py              # 网页爬虫模块
├── db.py                   # 数据库操作模块
├── sql_scanner.py          # SQL注入检测模块
├── xss_scanner.py          # XSS漏洞检测模块
├── webdb.sql               # 数据库初始化脚本
├── python-version.txt      # 开发python版本
├── requirements.txt        # 依赖库列表
├── LICENSE                 # MIT许可证
└── README.md               # 项目文档
```
## 开始使用
### 运行条件
+ Python 3.7+
+ MySQL 5.7+
+ 第三方库：``` flask beautifulsoup4 requests pymysql ```
### 启动前准备
克隆仓库
```bash
git clone https://github.com/silunuo/WEBpy-school.git
cd WEBpy-school
```
安装依赖
```bash
pip install -r requirements.txt
```
初始化数据库
```bash
mysql -u root -p < webdb.sql
```
进入```db.py```修改以下配置
```bash
def get_connection():
    return pymysql.connect(
        host="your_host", 
        user="your_username",
        password="your_password",
        database="scanner_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
```
### 直接启动
使用以下指令来启动 WebUI
```bash
python app.py
```

## 特别鸣谢
+ HelloFlask的开发学习文档 https://github.com/greyli/helloflask.git
