import streamlit as st
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import matplotlib.pyplot as plt


def app():
    st.text('Data master')
    column = pd.read_csv('data/meta/column_data.csv')
    df_model_data = pd.read_csv('data/meta/manual_model.csv')
    # pengambilan nilai differencing
    model_data=df_model_data.loc[0][0][1:-1]
    model_data=  str(model_data).split(',')
    model_data = [int(x) for x in model_data]
    time_series = column['time series'][0]
    df = pd.read_csv('data/data_stasioner.csv',parse_dates=[time_series],index_col=time_series)
    fig, ax = plt.subplots(figsize=(10,4))
    lags_acf = st.number_input('Masukkan jumlah lags acf yang ingin di tampilkan',min_value=10,value=30,max_value=df.shape[0]-1)
    plot_acf(df,lags=lags_acf,ax=ax)
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(10,4))

    lags_pacf = st.number_input('Masukkan jumlah lags pacf yang ingin di tampilkan',min_value=10,value=10,max_value=df.shape[0]-1)
    plot_pacf(df,lags=lags_pacf,ax=ax)
    st.pyplot(fig)

    st.subheader('Buat Model ARMA menggunakan Plot ACF dan PACF')
    num_model = st.number_input('Masukkan berapa banyak model yang akan dibuat:',min_value=0)
    key = 1

    if num_model>0:
        for i in range(1,num_model+1):
            # st.write(len)
            st.caption(f'Model ke - {i}')
            p_start = st.number_input('Masukkan variabel order (p):',key=key+1,min_value=0)
            d_start = st.number_input('Masukkan variabel order (d):',key=key+2,value=model_data[1],disabled=True)
            q_start = st.number_input('Masukkan variabel order (q):',key=key+3,min_value=0)
            p_sea = st.number_input('Masukkan variabel seasonal order (P):',key=key+4,min_value=0)
            d_sea = st.number_input('Masukkan variabel seasonal order (D):',key=key+5,min_value=0)
            q_sea = st.number_input("Masukkan variabel seasonal order (Q):",key=key+6,min_value=0)
            if(key==1):
                df_model_data = df_model_data.drop(index=0)
                s_sea = st.number_input('Masukkan variabel seasonal order (s):',key=key,min_value=0)
            else :
                s_sea = st.number_input('Masukkan variabel (s):',key=key,min_value=0,value=s_sea,disabled=True)
            
            df_model_data.loc[len(df_model_data)] = [(p_start,d_start,q_start),(p_sea,d_sea,q_sea,s_sea)]
            key = key+7
        st.write('Hasil Model yang terbentuk')
        st.write(df_model_data)
        if(st.button('Simpan model untuk forecasting')):
            df_model_data.to_csv('data/meta/manual_model.csv',index=False)
            st.success('Model siap di forecating')

    
    
    



    

