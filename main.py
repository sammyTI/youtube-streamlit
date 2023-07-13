import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time
# 起動方法 streamlit run main.py
# 終了方法 Ctrl+C
# リファレンス https://docs.streamlit.io/library/api-reference
# https://github.com/sammyTI/youtube-streamlit.git
st.title('Streamlit')

st.title('プログレスバーの表示')
'Start!!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    if i > 70:
        time.sleep(0.05)
    else:
        time.sleep(0.1)
'Done!!!'

l_column, r_column = st.columns(2)
buttonr = r_column.button('右カラムに文字を表示')
buttonl = l_column.button('左カラムに文字を表示')

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
