from apiclient.discovery import build
import json
from collections import Counter
import streamlit as st
from janome.tokenizer import Tokenizer
from collections import Counter
from PIL import Image
from datetime import datetime, timedelta


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
        part='id,snippet',
        maxResults=max_results,
        order='viewCount',
        videoDuration='medium',
        publishedAfter='2023-01-01T00:00:00Z',
        publishedBefore='2023-07-01T23:59:59Z',
        regionCode='JP'
    ).execute()

    video_info = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            channel_id = search_result['snippet']['channelId']  # チャンネルIDを取得
            video_stats = get_video_stats(video_id)
            if video_stats:
                channel_url = f"https://www.youtube.com/channel/{channel_id}"  # チャンネルのURLを作成
                published_at = search_result['snippet']['publishedAt']  # 投稿日時を取得
                video_info.append({
                    'title': search_result['snippet']['title'],
                    'channel_title': search_result['snippet']['channelTitle'],
                    'thumbnail': search_result['snippet']['thumbnails']['high']['url'],
                    'viewCount': int(video_stats['viewCount']),
                    'subscriberCount': int(get_subscriber_count(channel_id)),
                    'publishedAt': published_at,  # 投稿日時を追加
                    'video_url': f"https://www.youtube.com/watch?v={video_id}",
                    'channel_url': channel_url
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
    return counter.most_common()    

def filter_videos_by_evaluation(videos, min_evaluation=2, max_evaluation=10):
    filtered_videos = []
    for video in videos:
        if video['subscriberCount'] > 0:
            evaluation = video['viewCount'] / video['subscriberCount']
            if min_evaluation <= evaluation <= max_evaluation:
                filtered_videos.append(video)
    return filtered_videos

def filter_videos_by_published_date(videos, days_ago):
    filtered_videos = []
    for video in videos:
        published_at = datetime.strptime(video['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
        if published_at >= datetime.utcnow() - timedelta(days=days_ago):
            filtered_videos.append(video)
    return filtered_videos

def sort_videos_by_rating(videos):
    return sorted(videos, key=lambda x: x['viewCount'] / x['subscriberCount'], reverse=True)

def main():
    # 初期デフォルト値を指定
    default_channel_id = ''
    default_max_results = 10
    default_duration_filter = '6ヶ月以内'
    default_min_rating, default_max_rating = 1.0, 10.0

    st.title('YouTube分析')
    st.write('## クエリと閾値の設定')
    keyword = st.text_input("キーボードから入力してください:")
    st.write('## フィルター設定')
    st.write('### 表示数')
    max_results = st.slider('表示数', 1, 50, 10)
    st.write('### 動画評価指数')
    min_rating, max_rating = st.slider('動画評価指数の範囲', 0.0, 10.0, (default_min_rating, default_max_rating))
    st.write('### 投稿日時の範囲')
    duration_filter = st.selectbox('投稿日時の範囲', ['全期間', '6ヶ月以内', '3ヶ月以内', '1ヶ月以内'], index=1)  # 初期値を6ヶ月以内に設定
    if st.button("検索"):
        st.write("キーワードから検索:", keyword)
        videos = search_videos_by_keyword(keyword, max_results)
        videos = filter_videos_by_evaluation(videos, min_rating, max_rating)

        if duration_filter == '全期間':
            videos = filter_videos_by_published_date(videos, 36500)  # 適当に大きな値を指定して全期間とする
        elif duration_filter == '6ヶ月以内':
            videos = filter_videos_by_published_date(videos, 180)
        elif duration_filter == '3ヶ月以内':
            videos = filter_videos_by_published_date(videos, 90)
        elif duration_filter == '1ヶ月以内':
            videos = filter_videos_by_published_date(videos, 30)

        videos = sort_videos_by_rating(videos)

        # 該当動画数を表示
        st.write(f"該当動画数: {len(videos)}")

        st.markdown('## 動画評価指数が高い順に表示します')
        num_videos = len(videos)
        num_columns = 4  # 4列に変更
        num_rows = (num_videos - 1) // num_columns + 1
        for i in range(num_rows):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                index = i * num_columns + j
                if index < num_videos:
                    video = videos[index]
                    cols[j].image(video['thumbnail'], use_column_width=True)
                    cols[j].write(video['title'])
                    # 投稿日時を指定したフォーマットで表示
                    published_at = datetime.strptime(video['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_published_at = published_at.strftime("%Y/%m/%d %a %H:%M")
                    cols[j].write(f"投稿日時: {formatted_published_at}")
                    cols[j].write(f"[{video['channel_title']}]({video['channel_url']})")  # チャンネル名にリンクを付ける
                    cols[j].write("視聴回数: " + f"{video['viewCount']:,}")
                    cols[j].write("登録者数: " + f"{video['subscriberCount']:,}")
                    if video['subscriberCount'] > 0:
                        cols[j].write("動画評価指数: {:.2f}".format(video['viewCount'] / video['subscriberCount']))
                    cols[j].write(f"[動画を見る]({video['video_url']})")  # 動画リンクを表示

        most_common_words = count_csv(videos)
        # タイトルによく使われる単語を視覚的に表示
        st.markdown('## タイトルによく使われる単語')
        for word, count in most_common_words:
            if len(word) > 1 and count > 1:
                # 使用回数によってフォントサイズと色を変更
                font_size = min(20 + count * 3, 50)  # 最小フォントサイズ20, 最大フォントサイズ50
                color = f"rgb(0, {min(255, 100 + count * 10)}, 0)"  # 最小緑色(0, 100, 0), 最大緑色(0, 255, 0)
                st.markdown(f"<p style='font-size:{font_size}px; color:{color};'>ワード「{word}」 使用回数 {count} 回</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()