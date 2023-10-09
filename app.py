import streamlit as st
import pandas as pd
from halaman import acf_pacf, auto_sarima, uji_stasioner, upload_data,data_split,forecasting
page_names_to_funcs = {
    "Upload Data" : upload_data.app,
    "Uji Stasioner" : uji_stasioner.app,
    "ACF PACF" : acf_pacf.app,
    "Data Split":data_split.app,
    "Auto SARIMA":auto_sarima.app,
    'Forecasting':forecasting.app
    
}

demo_name = st.sidebar.selectbox("halaman", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()