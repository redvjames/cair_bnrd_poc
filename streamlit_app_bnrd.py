__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import time
import jellyfish
from fuzzywuzzy import fuzz
import epitran

df_bn = pd.read_csv('./data/company.csv', on_bad_lines='skip')[['Company Name ']]

# Create columns for the title and logo
col1, col2 = st.columns([3.5, 1])  # Adjust the ratio as needed

# Title in the first column
with col1:
    st.title("📋 BNRD Business Name Validation")
    st.write(
        "This app checks for similarity of an input business name with existing registered businesses."
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
    )

if st.button('Validate Business Name'):
    df_bn['levenshtein'] = df_bn['Company Name '].apply(lambda x: jellyfish.levenshtein_distance(text_input, x))
    df_bn['soundex'] = df_bn['Company Name '].apply(lambda x: fuzz.ratio(jellyfish.soundex(text_input), 
                                                                         jellyfish.soundex(x)))
    df_bn['metaphone'] = df_bn['Company Name '].apply(lambda x: fuzz.ratio(jellyfish.metaphone(text_input), 
                                                                           jellyfish.metaphone(x)))

    # Create columns for the title and logo
    col2, col3 = st.columns([3.5, 1])  # Adjust the ratio as needed
    
    # Title in the first column
    with col2:
        st.write("Spelling Similarity")
        df_spell = df_bn.loc[df_bn['levenshtein'] <= 10].sort_values('levenshtein')[['Company Name ']].reset_index(drop=True)
        st.dataframe(df_spell, height=100, width=200)
    # Logo and "Developed by CAIR" text in the second column
    with col3:
        st.write("Phonetic Similarity")
        df_sound = df_bn.loc[df_bn['metaphone'] >= 70].sort_values('metaphone', ascending=False)[['Company Name ']].reset_index(drop=True)
        st.dataframe(df_sound, height=100, width=200)
