__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime, timezone, timedelta
import time
import jellyfish
from fuzzywuzzy import fuzz
import epitran

def clean_text(text):
    return re.sub(r'[^A-Za-z0-9 ]', '', text)

df_data = pd.read_csv('./data/company.csv', on_bad_lines='skip')[['Company Name ']]
df_data['Business Name'] = df_data['Company Name '].str.lower().apply(clean_text)

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

threshold_spell = st.sidebar.slider(
    "Spelling Similarity Threshold Score", min_value=0, max_value=100, step=5, value=60)


threshold_sound = st.sidebar.slider(
    "Phonetics Similarity Threshold Score", min_value=0, max_value=100, step=5, value=70)


text_input = st.text_input(
        "Input Business Name 👇",
    )
input_bn = re.sub(r'[^A-Za-z0-9 ]', '', text_input.lower())

if st.button('Validate Business Name'):
    df_bn = df_data.copy()
    df_bn['levenshtein'] = df_bn['Business Name'].apply(lambda x: fuzz.ratio(input_bn, x))
    df_bn['soundex'] = df_bn['Business Name'].apply(lambda x: fuzz.ratio(jellyfish.soundex(input_bn), 
                                                                         jellyfish.soundex(x)))
    df_bn['metaphone'] = df_bn['Business Name'].apply(lambda x: fuzz.ratio(jellyfish.metaphone(input_bn), 
                                                                           jellyfish.metaphone(x)))

    # Create columns for the title and logo
    col2, col3 = st.columns([2.5, 2.5])  # Adjust the ratio as needed
    
    # Title in the first column
    with col2:
        st.write("Spelling Similarity")
        df_spell = df_bn.loc[df_bn['levenshtein'] >= threshold_spell].sort_values('levenshtein')[['Company Name ']].reset_index(drop=True)
        st.dataframe(df_spell, height=300, width=300)
    
    with col3:
        st.write("Phonetic Similarity")
        df_sound = df_bn.loc[df_bn['soundex'] >= threshold_sound].sort_values('metaphone', ascending=False)[['Company Name ']].reset_index(drop=True)
        st.dataframe(df_sound, height=300, width=300)
