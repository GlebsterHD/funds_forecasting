import os
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

option = st.sidebar.selectbox("Which Dashboard?", ('example', 'dashboard'))
st.header(option)
# пока для примера оставим выбор компании тут
symbol = "MSFT"
if option == 'dashboard':
    if not (os.path.exists("data.csv")):
        st.write("Downloading data")
        
        work = yf.Ticker(symbol)
        end_date = datetime.now().strftime('%Y-%m-%d')
        df = work.history(start='2022-01-01',end=end_date)
        st.dataframe(df)
        df.to_csv("data.csv")
    else:
        st.write("File exists")
        df = pd.read_csv("data.csv")
        st.dataframe(df)

    st.write(f"Size of file in MB: {os.path.getsize('data.csv')/1024/1024}")
    st.dataframe(df)
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=symbol)])

    fig.update_xaxes(type='category')
    fig.update_layout(height=700)

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)



if option == 'example':
    """
     Эту часть для примра ее потом удалим
    """
    st.title("Funds forecasting")
    st.header("Funds forecasting")
    st.subheader("subheader")
    st.write("loremipsum")


    some_list = [1, 2, 3]
    some_dict = {
        'a': 1,
        'b': 2,
    }

    st.write(some_list)
    st.write(some_dict)

    df = pd.DataFrame(np.random.rand(50, 20), columns=('col %d' % i for i in range(20)))

    st.dataframe(df)
    st.image('https://t4.ftcdn.net/jpg/00/59/96/75/360_F_59967553_9g2bvhTZf18zCmEVWcKigEoevGzFqXzq.jpg')
