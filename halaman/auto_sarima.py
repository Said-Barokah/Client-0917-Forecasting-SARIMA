import streamlit as st
import pandas as pd
import time
import timeit
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima

def app():
    
    column = pd.read_csv('data/meta/column_data.csv')
    time_series = column['time series'][0]
    df_train = pd.read_csv('data/data_train.csv',parse_dates=[time_series],index_col=time_series)
    df_test = pd.read_csv('data/data_test.csv',parse_dates=[time_series],index_col=time_series)
    df_man_model = pd.read_csv('data/meta/manual_model.csv')
    df_infreq = pd.infer_freq(df_test.index)
    # pengambilan nilai seasonal
    model_data=df_man_model.loc[0][1][1:-1]
    model_data=  str(model_data).split(',')
    model_data = [int(x) for x in model_data]
    st.subheader('Auto Sarima')
    seasonal = st.number_input('Masukkan nilai variabel musiman (s):',min_value=0,value=model_data[3])
    if(st.button('cek model dengan auto sarima')):
        with st.spinner('Wait for it...'):
            sarima_model=auto_arima(df_train, seasonal=True, trace=True,m=seasonal,error_action='warn', suppress_warnings=True, random_state = 20, n_fits=30)
        result = sarima_model.summary()
        # result_csv = result.as_csv()
        # with open('data/auto_model_results.csv', 'w') as f:
        #     f.write(result_csv)
        # st.write(result.rsquared)
        st.write(result)
        res_dict = sarima_model.to_dict()
        st.write(res_dict)
        df_auto_model = pd.DataFrame(data={'order':[(res_dict['order'][0],res_dict['order'][1],res_dict['order'][2])],
                                           'seasonal_order':[(res_dict['seasonal_order'][0],res_dict['seasonal_order'][1]
                                                              ,res_dict['seasonal_order'][2],res_dict['seasonal_order'][3])],
                                            "aic" : res_dict['aic']})
        df_auto_model.to_csv('data/meta/auto_model.csv',index=False)
        st.success('model berhasil disimpan')
