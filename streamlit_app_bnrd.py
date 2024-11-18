__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import time

df_bn = pd.read_csv('./data/company.csv', on_bad_lines='skip')[['Company Name ']]

# Create columns for the title and logo
col1, col2 = st.columns([3.5, 1])  # Adjust the ratio as needed

# Title in the first column
with col1:
    st.title("📋 Energy Consumption Forecasting POC")
    st.write(
        "This app check for similarity of an input business name with existing registered businesses."
    )
# Logo and "Developed by CAIR" text in the second column
with col2:
    st.image("images/CAIR_cropped.png", use_column_width=True)
    st.markdown(
        """
        <div style="text-align: center; margin-top: -10px;">
            Developed by CAIR
        </div>
        """, 
        unsafe_allow_html=True)

horizon = st.sidebar.radio(
    "Forecast Length",
    ["1 Day", "1 Week"],
    captions=[
        "24 Hours",
        "168 Hours"
    ], horizontal=True
)

text_input = st.text_input(
        "Input Business Name 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )

if st.button('Validate Business Name'):
    
        st.dataframe(pd.DataFrame(df_plot['Prediction']), height=300, width=400)
