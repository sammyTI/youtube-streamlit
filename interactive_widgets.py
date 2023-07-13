import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
# 起動方法 streamlit run main.py
# 終了方法 Ctrl+C
# リファレンス https://docs.streamlit.io/library/api-reference
st.title('Streamlit')

st.title('Interactive Widgets')

l_column, r_column = st.columns(2)
buttonl = l_column.button('左カラムに文字を表示')
buttonr = r_column.button('右カラムに文字を表示')
if buttonr:
    r_column.write('ここは右カラム')
if buttonl:
    l_column.write('ここは左カラム')

expander1 = st.expander('質問１')
expander1.write('回答内容を書く')

expander2 = st.expander('質問２')
expander2.write('回答内容を書く')

expander3 = st.expander('質問３')
expander3.write('回答内容を書く')

# img = Image.open('pengin.jpg')

# if st.checkbox('Show Image'):
#     st.image(img, caption='ペンギン', use_column_width=True)

# option = st.selectbox(
#     '好きな数字を教えてください',
#     list(range(1,11))
# )
# 'あなたの好きな数字は、',option,'です。'

# text = st.text_input('あなたの趣味を教えてください。')
# 'あなたの趣味：',text,'です。'

# condition = st.slider('今日の調子は？',0,100,50)
# 'コンディション：',condition,
