import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def app():
    column = pd.read_csv('data/meta/column_data.csv')
    time_series = column['time series'][0]
    df_resample = pd.read_csv('data/data_resample.csv',parse_dates=[time_series],index_col=time_series)
    st.write('Plot Data Master')
    st.line_chart(df_resample)
    from statsmodels.tsa.seasonal import seasonal_decompose
    decomposition = seasonal_decompose(df_resample, model='additive')
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
    decomposition.trend.plot(ax=ax1)
    decomposition.seasonal.plot(ax=ax2)
    decomposition.resid.plot(ax=ax3)
    decomposition.observed.plot(ax=ax4)
    st.pyplot(fig)
    diff = st.number_input('Masukkan Banyak different (jika data sudah stasioner masukkan nilai 0)',min_value=0,value=1,max_value=50)
    if(st.button('Ubah Data menjadi Stasioner',key=2)):
        df_diff = df_resample
        if diff > 0 :
            for i in range(diff):
                df_diff = df_diff.diff()[1:]
        st.line_chart(df_diff)
        st.success('Data Stasioner Siap Diproses di PLOT ACF dan PACF')
        df_diff.to_csv('data/data_stasioner.csv')
        model_data = pd.DataFrame(data={'order': [(0,diff,0)],'seasonal_order':[(0,0,0,0)]})
        model_data.to_csv('data/meta/manual_model.csv',index=False)
        model_data = pd.read_csv('data/meta/manual_model.csv')



        
        


        



