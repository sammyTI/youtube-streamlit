from apiclient.discovery import build
import json
from collections import Counter
import streamlit as st
from janome.tokenizer import Tokenizer
from collections import Counter

st.set_page_config(layout="wide")


with open('secret.json') as f:
    secret = json.load(f)

DEVELOPER_KEY = secret['KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def search_videos_by_keyword(keyword, max_results):
    search_response = youtube.search().list(
        q=keyword,
        type='video',
        part='id,snippet',  # 'statistics'を削除
        maxResults=max_results,
        order='viewCount',
        videoDuration='medium',  # Short動画をフィルタするため4分以上の動画に絞る
        publishedAfter='2023-01-01T00:00:00Z',  # 検索期間
        publishedBefore='2023-07-01T23:59:59Z'  # 検索期間
    ).execute()

    video_info = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_stats = get_video_stats(video_id)
            if video_stats:
                video_info.append({
                    'title': search_result['snippet']['title'],
                    'thumbnail': search_result['snippet']['thumbnails']['high']['url'],
                    'viewCount': int(video_stats['viewCount']),
                    'subscriberCount': int(get_subscriber_count(search_result['snippet']['channelId']))
                })

    return video_info


def get_video_stats(video_id):
    stats_response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    for video_result in stats_response.get('items', []):
        return video_result['statistics']

    return None


def get_subscriber_count(channel_id):
    channel_response = youtube.channels().list(
        part='statistics',
        id=channel_id
    ).execute()

    for channel_result in channel_response.get('items', []):
        return channel_result['statistics']['subscriberCount']


def analyze_title_words(videos):
    all_titles = ' '.join([video['title'] for video in videos])
    words = all_titles.split()
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(10)
    return most_common_words


def mecab_analysis(text):
    t = Tokenizer()
    output = []
    tokens = t.tokenize(text)
    for token in tokens:
        part_of_speech = token.part_of_speech.split(',')[0]
        if part_of_speech in ['名詞', '動詞', '形容詞']:
            output.append(token.surface)
    return output



def count_csv(videos):
    all_titles = ' '.join([video['title'] for video in videos])
    text = all_titles
    words = mecab_analysis(text)
    counter = Counter(words)
    return counter.most_common()  # `most_common()`メソッドを呼び出して結果を返す


def main():
    st.title('YouTube分析')
    st.sidebar.write('## クエリと閾値の設定')
    keyword = st.sidebar.text_input("キーボードから入力してください:")
    st.sidebar.write('### 表示数の設定')
    max_results = st.sidebar.slider('表示数', 1, 50, 10)
    order = 'viewCount',  # 再生数でソート
    regionCode = 'JP',  # 地域を日本に指定
    type = 'video',  # 検索対象を動画に指定

    if st.sidebar.button("検索"):
        st.write("キーワードから検索:", keyword)
        videos = search_videos_by_keyword(keyword, max_results)
        st.markdown('## 視聴回数の多い順位表示します')
        num_videos = len(videos)
        num_columns = 4
        num_rows = (num_videos - 1) // num_columns + 1
        for i in range(num_rows):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                index = i * num_columns + j
                if index < num_videos:
                    video = videos[index]
                    cols[j].image(video['thumbnail'], use_column_width=True, width=500)
                    cols[j].text(video['title'])
                    cols[j].text("視聴回数: " + f"{video['viewCount']:,}")
                    cols[j].text("登録者数: " + f"{video['subscriberCount']:,}")
                    if video['subscriberCount'] > 0:
                        cols[j].text("視聴回数/登録者数: {:.2f}".format(video['viewCount'] / video['subscriberCount']))

        most_common_words = count_csv(videos)
        st.markdown('## タイトルによく使われる単語')
        for word, count in most_common_words:
            if len(word) > 1 and count > 1:
                st.write(f"ワード「{word}」 使用回数 {count} 回")


if __name__ == '__main__':
    main()
