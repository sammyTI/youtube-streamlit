import streamlit as st
import numpy as np
import pandas as pd

st.title('Streamlit')
st.title('DataFrame')
# st.write('DataFrame')

df = pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40],
})

st.write('動的な表を作りたい場合：write(),dataframe()')

# st.write(df) #引数widthなどの指定が不可能
# st.dataframe(df.style.highlight_max(axis=0),width=1200,height=300)
st.dataframe(df.style.highlight_max(axis=0))

st.write('静的な表を作りたい場合：table()')

st.table(df.style.highlight_max(axis=0))

st.title('Markdown')

"""
# 章
## 節
### 項

```python
import streamlit as st
import numpy as np
import pandas as pd
```
"""

st.title('Chart elements')

st.write('Chart')
df = pd.DataFrame(
    np.random.rand(20,3),
    columns=['a','b','c']
)

st.table(df.style.highlight_max(axis=0))
st.line_chart(df)#グラフ
st.area_chart(df)#折れ線グラフ
st.bar_chart(df)#棒グラフ


st.write('MAP')
df = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69,139.70],
    columns=['lat','lon']
)
st.map(df)