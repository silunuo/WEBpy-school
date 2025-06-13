#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
#  author:lwl
#  Collaborator:cr and lx and tyf
#


import os
import webbrowser
from flask import Flask, render_template, request, redirect, url_for
from crawler import crawl
from db import get_all_urls, log_xss_scan, delete_url, get_scan_logs, get_recent_scans, log_sql_scan, get_all_scan_logs
from sql_scanner import detect_sql_injection
from xss_scanner import detect_xss

app = Flask(__name__)

@app.route('/')
def index():
    urls = get_all_urls()
    return render_template('index.html', urls=urls)
@app.route('/start_crawl', methods=['POST'])
def start_crawl():
    target_url = request.form.get('url')
    if target_url:
        crawl(target_url)
    return redirect(url_for('index'))
@app.route('/scan_xss', methods=['POST'])
def scan_xss():
    target_url = request.form.get('target_url')
    url_id = request.form.get('url_id')
    if target_url and url_id:
        result = detect_xss(target_url)
        log_xss_scan(url_id, result)
        return render_template('scan_result.html',
                               url=target_url,
                               result=result,
                               recent_scans=get_recent_scans())
    return redirect(url_for('index'))
@app.route('/delete_url', methods=['POST'])
def delete_url_route():
    url_id = request.form.get('url_id')
    if url_id:
        delete_url(url_id)
    return redirect(url_for('index'))
@app.route('/logs')
def show_logs():
    logs = get_all_scan_logs()  # 获取所有日志（XSS+SQL）
    return render_template('logs.html', logs=logs)
@app.route('/scan_sql', methods=['POST'])
def scan_sql():
    target_url = request.form.get('target_url')
    url_id = request.form.get('url_id')

    if target_url and url_id:
        result = detect_sql_injection(target_url)
        log_sql_scan(url_id, result)
        return render_template('scan_result.html',
                               url=target_url,
                               result=result,
                               recent_scans=get_recent_scans(),
                               scan_type="SQL注入")

    return redirect(url_for('index'))

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True)

