import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Симулятор ИИ-трейдера")
st.write("Выберите акцию, и ИИ покажет, как бы она торговалась за последний год.")

# Кнопки выбора
ticker = st.selectbox("Выберите акцию:", ["AAPL", "TSLA", "MSFT", "GOOGL"])
short_window = st.slider("Короткая средняя (дней):", 5, 50, 20)
long_window = st.slider("Длинная средняя (дней):", 20, 200, 50)

if st.button("Запустить ИИ"):
    with st.spinner('ИИ анализирует рынок...'):
        data = yf.download(ticker, period="1y", progress=False)
        
        # Делаем так, чтобы данные были одномерными (фикс для новых версий yfinance)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data['Short_SMA'] = data['Close'].rolling(window=short_window).mean()
        data['Long_SMA'] = data['Close'].rolling(window=long_window).mean()
        
        data['Signal'] = 0
        data.loc[data['Short_SMA'] > data['Long_SMA'], 'Signal'] = 1
        data['Position'] = data['Signal'].diff()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data['Close'], label='Цена', color='blue', alpha=0.6)
        ax.plot(data['Short_SMA'], label='Короткая средняя', color='orange')
        ax.plot(data['Long_SMA'], label='Длинная средняя', color='red')
        
        ax.plot(data[data['Position'] == 1].index, data['Short_SMA'][data['Position'] == 1], '^', markersize=10, color='g', label='Покупка')
        ax.plot(data[data['Position'] == -1].index, data['Short_SMA'][data['Position'] == -1], 'v', markersize=10, color='r', label='Продажа')
        
        ax.set_title(f"Торговля {ticker}")
        ax.legend()
        st.pyplot(fig)
        
        trades = data['Position'].value_counts().sum()
        st.write(f"*Сделок совершено:* {trades}")


