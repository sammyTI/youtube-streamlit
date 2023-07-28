import streamlit as st
from apiclient.discovery import build
import json
from datetime import datetime, timedelta
from PIL import Image

# YouTube APIキーを読み込む
with open('secret.json') as f:
    secret = json.load(f)
DEVELOPER_KEY = secret['KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def search_videos_by_channel(channel_id, max_results, duration_filter, min_rating, max_rating):
    # 日付範囲の設定
    published_after, _ = get_date_range(duration_filter)
    search_response = youtube.search().list(
        channelId=channel_id,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        order='viewCount',
        videoDuration='medium',
        publishedAfter=published_after,
        regionCode='JP'
    ).execute()

    video_info = []
    video_count = 0  # 動画の数をカウントする変数を初期化

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_stats = get_video_stats(video_id)
            if video_stats:
                subscriber_count = get_subscriber_count(channel_id)
                if subscriber_count > 0:
                    views_per_subscriber = int(video_stats['viewCount']) / subscriber_count
                    rating = views_per_subscriber  # 動画評価指数をratingとして定義
                    if min_rating <= rating <= max_rating:  # 動画評価指数が指定範囲内のみ追加
                        video_info.append({
                            'title': search_result['snippet']['title'],
                            'viewCount': int(video_stats['viewCount']),
                            'publishedAt': search_result['snippet']['publishedAt'],
                            'viewsPerSubscriber': views_per_subscriber,
                            'thumbnail': search_result['snippet']['thumbnails']['high']['url'],
                            'videoId': video_id,
                            'rating': rating  # 動画評価指数を追加
                        })
                        video_count += 1  # 動画が条件を満たす場合に動画数をカウント

    return video_info, video_count  # 動画の情報と動画数の両方を返すように修正

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
        return int(channel_result['statistics']['subscriberCount'])

    return 0

def get_date_range(duration_filter):
    # 日付範囲の計算
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30) if duration_filter == '1ヶ月以内' else \
        end_date - timedelta(days=90) if duration_filter == '3ヶ月以内' else \
        end_date - timedelta(days=180)

    # YouTube APIの形式に変換
    published_after = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    published_before = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    return published_after, published_before

def get_channel_info(channel_id):
    channel_response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()

    for channel_result in channel_response.get('items', []):
        title = channel_result['snippet']['title']
        subscriber_count = int(channel_result['statistics']['subscriberCount'])
        return {'title': title, 'subscriberCount': subscriber_count, 'channelId': channel_id}

    return None

def main():
    # 初期デフォルト値を指定
    default_channel_id = ''
    default_max_results = 10
    default_duration_filter = '6ヶ月以内'
    default_min_rating, default_max_rating = 1.0, 10.0

    st.title('YouTube動画評価ツール')
    channel_id = st.text_input("チャンネルIDを入力してください:", default_channel_id)

    st.write('### 表示数の設定')
    max_results = st.slider('表示数', 1, 50, default_max_results)

    duration_filter = st.selectbox('フィルター期間', ['6ヶ月以内', '3ヶ月以内', '1ヶ月以内'], index=0 if default_duration_filter == '6ヶ月以内' else 1 if default_duration_filter == '3ヶ月以内' else 2)

    min_rating, max_rating = st.slider('動画評価指数の範囲', 0.0, 10.0, (default_min_rating, default_max_rating))
    # クリアボタンの処理
    if st.button("クリア"):
        channel_id = default_channel_id
        max_results = default_max_results
        duration_filter = default_duration_filter
        min_rating, max_rating = default_min_rating, default_max_rating
    if st.button("分析"):
        if channel_id:
            st.write("チャンネルID：", channel_id)
            channel_info = get_channel_info(channel_id)
            if channel_info:
                st.write("チャンネル名：", channel_info['title'])
                st.write("登録者数：", f"{channel_info['subscriberCount']:,}")
                st.markdown(f"[チャンネルページに移動](https://www.youtube.com/channel/{channel_info['channelId']})")

            # 修正されたsearch_videos_by_channel関数を呼び出し
            videos, video_count = search_videos_by_channel(channel_id, max_results, duration_filter, min_rating, max_rating)

            st.write("期間内の動画投稿本数：", video_count)  # 動画数を表示

            if not videos:
                st.write("条件に合致する動画は見つかりませんでした。")
            else:
                st.markdown('## 評価順に動画を表示します')
                st.write("フィルター条件で該当した動画数:", len(videos))

                # 4列5行のグリッドレイアウトで動画を表示する
                num_columns = 4
                max_rows = 10  # 最大表示行数を5行とする

                num_rows = min(max_rows, -(-len(videos) // num_columns))  # 動画の数に応じて行数を計算

                for i in range(num_rows):
                    col = st.columns(num_columns)
                    for j in range(num_columns):
                        index = i * num_columns + j
                        if index < len(videos):
                            video = videos[index]
                            col[j].image(video['thumbnail'], use_column_width=True)
                            col[j].write(video['title'])
                            col[j].write(f"視聴回数： {video['viewCount']:,}")
                            published_at = datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                            published_at_formatted = published_at.strftime('%Y/%m/%d %a %H:%M')
                            day_of_week = {"Mon": "月", "Tue": "火", "Wed": "水", "Thu": "木", "Fri": "金", "Sat": "土", "Sun": "日"}
                            published_at_day_of_week = day_of_week[published_at.strftime("%a")]
                            col[j].write(f"投稿日時： {published_at_formatted.replace(published_at.strftime('%a'), published_at_day_of_week)}")
                            col[j].write(f"動画評価指数： {video['viewsPerSubscriber']:.2f}")
                            video_url = f"https://www.youtube.com/watch?v={video['videoId']}"
                            col[j].write(f"[動画を見る]({video_url})")
                            col[j].write('---')
                    # st.balloons()


if __name__ == '__main__':
    main()
