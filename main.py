import streamlit as st
from pages import youtube_analyze_from_search_v2, youtube_analyze_from_channel_v1
from PIL import Image

# ここで set_page_config() を呼び出す
image = Image.open('./asset/youtube_favicon.png')
st.set_page_config(
    page_title="YouTube分析ツール", 
    page_icon=image, 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://www.google.com",
        'About': """
        # YouTube分析アプリ
        このアプリはYouTubeの分析に用いるアプリで、検索キーワードやチャンネルIDをもとに分析した結果を表示しています。
        """
    }
)

# ページの辞書を定義
PAGES = {
    "キーワードから分析": youtube_analyze_from_search_v2,
    "チャンネルから分析": youtube_analyze_from_channel_v1,
}

st.sidebar.title('ページ選択')
page = st.sidebar.selectbox("ページを選択してください", list(PAGES.keys()))

if page == "キーワードから分析":
    PAGES["キーワードから分析"].main()
elif page == "チャンネルから分析":
    PAGES["チャンネルから分析"].main()