import streamlit as st
import pandas as pd
from pmdarima.arima import ARIMA
from pmdarima.arima import auto_arima

from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_percentage_error as mape

def app():
    st.header('Forecasting Data')
    column = pd.read_csv('data/meta/column_data.csv')
    time_series = column['time series'][0]
    series = column['series'][0]
    df_auto_model = pd.read_csv('data/meta/auto_model.csv')
    df_man_model = pd.read_csv('data/meta/manual_model.csv')

    

    man_model_order=[int(x) for x in str(df_man_model.loc[0][1][1:-1]).split(',')]
    auto_model_sea =[int(x) for x in str(df_man_model.loc[0][1][1:-1]).split(',')]

    df_train = pd.read_csv('data/data_train.csv',parse_dates=[time_series],index_col=time_series)
    df_test = pd.read_csv('data/data_test.csv',parse_dates=[time_series],index_col=time_series)
    df_infreq = pd.infer_freq(df_test.index)
    mape_dict = {'model': [], 'mape': []}

    st.subheader('Manual Model')
    st.write(df_man_model)


    for i in range(len(df_man_model)):
        st.write(f'Manual Model {i+1}')
        man_model_order=[int(x) for x in str(df_man_model.loc[i][0][1:-1]).split(',')]
        man_model_sea=[int(x) for x in str(df_man_model.loc[i][1][1:-1]).split(',')]
        sarima_model = SARIMAX(df_train,order=tuple(man_model_order),seasonal_order=tuple(man_model_sea))
        sarima_model_fit=sarima_model.fit()

        forecast = st.number_input(f'Masukkan jumlah peramalan data pada model {i}',min_value=1,value=20,key=i)
        n_forecast = len(df_test) + forecast
        pred = sarima_model_fit.predict(start=len(df_train), end=len(df_train)+n_forecast)
        dates = pd.date_range(df_train.index[-1],periods=n_forecast,freq=df_infreq)
        pred = pd.Series(pred, index=dates).iloc[1:]
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(df_train,"b-",label="train")
        ax.plot(df_test,"r-",label="test")
        ax.plot(pred,"g-",label="forecast")
        ax.legend()

        tab1, tab2 = st.tabs(["Plot Data", "forecast dan akurasi"])
        with tab1:
            st.write(fig)
        with tab2:
            df_test.rename(columns={series: 'Actual'}, inplace=True)
            df_res = df_test.join(pred)
            st.write(df_res)
            res_mape = mape(df_res['Actual'],df_res['predicted_mean'])
            st.write(f'Hasil mean_absolute_percentage_error dari peramalan tersebut adalah {round(res_mape,3)}')
            mape_dict['model'].append(f'manual {tuple(man_model_order)}{tuple(man_model_sea)}')
            mape_dict['mape'].append(res_mape)
    st.subheader('Auto Model')
    st.write(f'Auto Model {1}')
    st.write(df_auto_model)
    auto_model_order=[int(x) for x in str(df_auto_model.loc[0][0][1:-1]).split(',')]
    auto_model_sea=[int(x) for x in str(df_auto_model.loc[0][1][1:-1]).split(',')]
    
    sarima_model = SARIMAX(df_train,order=tuple(auto_model_order),seasonal_order=tuple(auto_model_sea))
    forecast = st.number_input('Masukkan jumlah peramalan data',min_value=1,value=20,key=99)
    sarima_model_fit = sarima_model.fit()
    n_forecast = len(df_test) + forecast
    
    pred = sarima_model_fit.predict(start=len(df_train), end=len(df_train)+n_forecast)
    dates = pd.date_range(df_train.index[-1],periods=n_forecast,freq=df_infreq)
    pred = pd.Series(pred, index=dates).iloc[1:]
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df_train,"b-",label="train")
    ax.plot(df_test,"r-",label="test")
    ax.plot(pred,"g-",label="forecast")
    ax.legend()
    tab1, tab2 = st.tabs(["Plot Data", "forecast dan akurasi"])
    with tab1:
        st.write(fig)
    with tab2:
        df_test.rename(columns={series: 'Actual'}, inplace=True)
        df_res = df_test.join(pred)
        st.write(pred)
        res_mape = mape(df_res['Actual'],df_res['predicted_mean'])
        st.write(f'Hasil mean_absolute_percentage_error dari peramalan tersebut adalah {round(res_mape,3)}')
        mape_dict['model'].append(f'auto{tuple(auto_model_order)}({tuple(auto_model_sea)})')
        mape_dict['mape'].append(res_mape)
    st.subheader('Perbandingan Nilai MAPE')
    tab1, tab2 = st.tabs(["Grafik MAPE", "Model"])
    df_mape = pd.DataFrame(mape_dict,index=mape_dict['model'])

    with tab1:
        st.bar_chart(df_mape['mape'])
    with tab2:
        st.write(df_mape)
        
