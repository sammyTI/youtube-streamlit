import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title('Streamlit')
st.title('Display Image')

img = Image.open('pengin.jpg')

st.image(img, caption='ペンギン', use_column_width=True)

# df = pd.DataFrame({
#     '1列目':[1,2,3,4],
#     '2列目':[10,20,30,40],
# })

# st.write('動的な表を作りたい場合：write(),dataframe()')
