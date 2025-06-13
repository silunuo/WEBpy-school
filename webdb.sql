CREATE DATABASE IF NOT EXISTS scanner_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scanner_db;

-- 创建存储爬取的URL
CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- 主键，自动递增
    url TEXT NOT NULL,                           -- 存储抓取到的 URL
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 爬取时间，默认当前时间
    is_xss_detected BOOLEAN DEFAULT 0,      -- XSS 检测结果，默认没有检测（布尔值）
    xss_scan_result TEXT,                       -- 存储 XSS 检测结果
    scan_date TIMESTAMP NULL                    -- 检测时间
);

-- 如果需要存储检测记录（例如：多次检测记录）
CREATE TABLE IF NOT EXISTS xss_scan_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_id INT NOT NULL,                        -- 外键，关联urls表
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 检测时间
    scan_result TEXT,                           -- 检测结果
    FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE -- 外键关联
);
-- 添加SQL注入相关字段到urls表
ALTER TABLE urls 
ADD COLUMN is_sql_detected BOOLEAN DEFAULT 0,
ADD COLUMN sql_scan_result TEXT,
ADD COLUMN sql_scan_date TIMESTAMP NULL;

-- 创建SQL注入扫描日志表
CREATE TABLE IF NOT EXISTS sql_scan_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_id INT NOT NULL,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scan_result TEXT,
    FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE
);