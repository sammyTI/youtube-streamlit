import requests

search_url = "https://www.youtube.com/@TBSSPORTS6"
response = requests.get(search_url)

if response.status_code == 200:
    print(response.text)
else:
    print("探索URLの取得に失敗しました。")
