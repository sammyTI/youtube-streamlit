import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

image = Image.open('./asset/youtube_favicon.png')
st.set_page_config(
    page_title="Slime Creator", 
    page_icon=image, 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={
         'Get Help': 'https://www.google.com',
         'Report a bug': "https://www.google.com",
         'About': """
         # 画像生成風アプリ
         このアプリは画像生成風アプリで、実際にはキングスライムしか表示しません。
         """
     })

st.title("YouTube分析ツール")
st.header('このツールはYouTube Data API v3を使用し作られています。')

col1, col2 = st.columns(2)

with col1:
    st.header("テキストから分析")
    # st.markdown("[![serch](./asset/serch.png)]")
    # st.markdown("![serch](asset/serch.png)")
    st.image("./asset/serch.png")
    st.button("ツールを使用する。サイドバーから選択できます。")
        # /youtube_analyze_from_channel_v1

with col2:
    st.header("チャンネルから分析")
    st.image("./asset/channel.png")
    st.button("分析ツールを使用する。サイドバーから選択できます。")