#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
#  author:silunuo
#  Collaborator:cr and lx and tyf

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from db import insert_url

def crawl(base_url, max_links=20):
    visited = set()
    to_visit = [base_url]

    while to_visit and len(visited) < max_links:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(base_url, link['href'])
                if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                    to_visit.append(absolute_url)

            insert_url(url)
            visited.add(url)
        except Exception as e:
            print(f"跳过 {url}: {e}")
