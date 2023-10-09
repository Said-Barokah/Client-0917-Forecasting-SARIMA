import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from pmdarima import auto_arima


def app() :
    st.subheader('Split Data menjadi Data Training dan Data Testing')
    column = pd.read_csv('data/meta/column_data.csv')
    time_series = column['time series'][0]
    df = pd.read_csv('data/data_resample.csv',parse_dates=[time_series],index_col=time_series)
    # test_size = (st.date_input('Dari tanggal berapa yang ingin dijadikan data test',min_value=df.index.min(),value=datetime.date(2021,12,1),max_value=df.index.max()))
    value = int(df.shape[0] * 0.80)
    from pmdarima.model_selection import train_test_split
    train_size  = st.number_input('Masukkan jumlah dari data train:',min_value=1,max_value=df.shape[0]-1,value=value)
    
    df_train, df_test = train_test_split(df, train_size=train_size)
    # df_train, df_test = df[df.index.min():test_size] ,df[test_size+timedelta(days=7):df.index.max()]

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df_train, label="Data Train")
    ax.plot(df_test, label="Data Test")
    ax.set_title("Training dan Data Test")
    ax.legend()
    st.pyplot(fig)
    if(st.button('Simpan data train dan data test')):
        df_train.to_csv('data/data_train.csv')
        df_test.to_csv('data/data_test.csv')
        st.success('data train dan data test sudah berhasil disimpan')
    # sarima_model=auto_arima(df_train, seasonal=True,m=54, trace=True,information_criterion='aicc', error_action='warn', suppress_warnings=True, random_state = 20)
    # st.write(sarima_model.summary())

    # n_forecast = len(df_test) + 20
    # pred = sarima_model.predict(n_forecast)
    # dates = pd.date_range(df_train.index[-1],periods=n_forecast,freq="W")
    # pred = pd.Series(pred, index=dates)

    # fig, ax = plt.subplots(figsize=(10,4))
    # ax.plot(df_train,"b-",label="train")
    # ax.plot(df_test,"r-",label="test")
    # ax.plot(pred,"g-",label="forecast")
    # ax.legend()
    # st.write(pred)
    # st.write(fig)

    
    



