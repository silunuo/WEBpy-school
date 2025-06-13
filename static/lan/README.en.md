<div align="center">
<h1>Flask-Requests-SQL\XSS-CH</h1>
Web Crawler & Vulnerability Detection Automation System<br><br>

[**English**](./static/lan/README.en.md) | [**中文简体**](./README.md) 

</div>

> Developed independently by learning from public network dependency libraries' documentation. Safe to use.
>
## Introduction
This repository features:
+ Clean and visually appealing web interface based on Flask framework
+ Requests library as web crawling dependency
+ Utilizes pymysql for frontend-backend data transmission (Note: Local database reading program not implemented)
+ Performs common XSS vulnerability detection and SQL injection detection on crawled web pages
+ Extensible detection framework allowing users to expand detection capabilities

## Project Structure
```bash
WEBpy-school/
├── static/
│   ├── css/
│   │   └── style.css       # Frontend styles
│   ├── img/
│   │   ├── SUNc.png        # Project Logo
│   │   └── SUNb.png        # Project Logo
│   └── lan/
│       └── README.en.md    # Non-native language documentation
├── templates/
│   ├── index.html          # Main interface
│   ├── logs.html           # Logs page
│   └── scan_result.html    # Scan results page
├── app.py                  # Flask main application
├── crawler.py              # Web crawler module
├── db.py                   # Database operations module
├── sql_scanner.py          # SQL injection detection module
├── xss_scanner.py          # XSS vulnerability detection module
├── webdb.sql               # Database initialization script
├── python-version.txt      # Development Python version
├── requirements.txt        # Dependency libraries list
├── LICENSE                 # MIT License
└── README.md               # Project documentation
```
## Getting Started
### Prerequisites
+ Python 3.7+
+ MySQL 5.7+
+ Third-party libraries:``` flask beautifulsoup4 requests pymysql ```
### Setup
Clone repository:
```bash
git clone https://github.com/silunuo/WEBpy-school.git
cd WEBpy-school
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Initialize database:
```bash
mysql -u root -p < webdb.sql
```
Modify database configuration in```db.py``` :
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
### Launch Application
Start WebUI with:
```bash
python app.py
```

## Special Thanks
+ learning documentation from HelloFlask https://github.com/greyli/helloflask.git
