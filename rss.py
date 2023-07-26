import requests
import re
import xml.etree.ElementTree as ET

def extract_target_part_from_rss(search_url, target_url):
    # 探索URLの内容を取得
    response = requests.get(search_url)
    if response.status_code != 200:
        print("探索URLの取得に失敗しました。")
        return None

    try:
        # RSSフィードを解析
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print("RSSフィードの解析に失敗しました。エラー内容:", e)
        return None

    target_part = None
    for channel_id in root.iter('channel'):
        link = channel_id.find('link').text
        if re.search(target_url, link):
            match = re.search(r'channel_id=(\w+)', link)
            if match:
                target_part = match.group(1)
                break

    return target_part

# 使用例
search_url = "https://www.youtube.com/@TBSSPORTS6"
target_url = r"https://www\.youtube\.com/feeds/videos\.xml\?channel_id=(\w+)"
specified_part = extract_target_part_from_rss(search_url, target_url)
print("指定部分:", specified_part)
