import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

def resample(data,freq):
    df_infreq = pd.infer_freq(data.index)
    dic_freq = {'Harian' : 'D',
            'Mingguan':'W',
            'Bulanan':'M',
            'Tahunan':'A',
            'Pilih Salah Satu jika anda ingin resample data':df_infreq}
    return data.resample(dic_freq[freq]).mean()
    
def app():
    st.title('APLIKASI PERAMALAN JUMLAH PASIEN')
    if (os.path.exists("data/data_master.csv")):
         st.text('Data master')
         column = pd.read_csv('data/meta/column_data.csv')
         time_series = column['time series'][0]
         datamaster = pd.read_csv('data/data_master.csv')
         datamaster[time_series] = pd.to_datetime(datamaster[time_series])
         datamaster = datamaster.set_index(time_series)
         df_infreq = pd.infer_freq(datamaster.index)
         st.write(f"Frequensi time series data anda frequensi ({df_infreq})")
         st.markdown("https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects")
         type_df = st.selectbox('(optional) resample data menjadi data:',["Pilih Salah Satu jika anda ingin resample data",'Harian','Mingguan','Bulanan',"Tahunan"],index=0)
         mis_val_dm = 0
         df_resample = resample(datamaster,type_df)
         mis_val_res = 0
         
         if(mis_val_res > mis_val_dm):
              st.error('Resample tolak, coba frequency yang lebih tinggi dari data asli')
              df_resample = datamaster
              st.write(df_resample)
              # st.write(f'Jumlah missing value {int(df_resample.isna().sum())}')
              st.line_chart(df_resample)
              df_resample.to_csv('data/data_resample.csv')
         else:
              st.write(df_resample)
              # st.write(f'Jumlah missing value {int(df_resample.isna().sum())}')
              st.line_chart(df_resample)
              if(type_df != 'Pilih Salah Satu jika anda ingin resample data'):
                st.success('Data sukses di resample')
              df_resample.to_csv('data/data_resample.csv')
         
         
         

        #  st.error('Data tidak bisa di resample, coba gunakan resample yang lain')
        #  st.line_chart(df_decompose)
        #  st.write(df_decompose.isna().sum())
         
         
         
        #  df_main = pd.read_csv('data/decompose_data.csv',parse_dates=[time_series],index_col=time_series)
        #  df_main = pd.read_csv('data/decompose_data.csv')
        #  st.write(df_main)
        #  st.line_chart(df_main)
        #  st.info(f'Data yang akan di proses adalah data {type_df}')
        #  st.write(dataframe)

         

    

    data = st.file_uploader("upload data berformat csv (untuk mengubah data master)", type=['csv'])
    if data is not None:
            dataframe = pd.read_csv(data)
            # dataframe.columns = dataframe.columns.str.replace("^\s+|\s+$","",regex=True)
            
            # st.write(dataframe)
            col1, col2 = st.columns(2)
            with col1 :
                time_series = st.selectbox("Pilih Kolom yang akan dijadikan timeseries :",
                list(dataframe.columns),index=0)
            with col2 :
                series = st.selectbox("Pilih Kolom yang akan dijadikan series :",
                list(dataframe.columns),index=len(list(dataframe.columns))-1)
             # ubah kolom date menjadi tipe datetime
            dataframe[time_series] = pd.to_datetime(dataframe[time_series])
            # jadikan kolom date sebagai index
            dataframe = dataframe.set_index(time_series)
            # cek missing value

            # st.write(f'Jumlah missing value {int(dataframe.isna().sum())}')
            st.line_chart(dataframe)
            dataframe.to_csv('data/contoh_master.csv',index=False)

            column_data = pd.DataFrame(data={'time series': [time_series], 'series': [series]})
            if st.button('simpan data menjadi data master') :
                # dataframe[label] = dataframe[label].str.replace("^\s+|\s+$","",regex=True)
                dataframe.to_csv('data/data_master.csv')
                column_data.to_csv('data/meta/column_data.csv',index=False)
                with st.spinner('tunggu sebentar ...'):
                    time.sleep(1)
                st.success('data berhasil disimpan silakan refresh aplikasi')
                st.info('column ' + column_data['time series'][0] + ' akan dijadikan time series')
                st.info('column ' + column_data['series'][0] + ' akan dijadikan series')
