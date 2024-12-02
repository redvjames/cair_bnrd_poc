# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

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

poc_option = st.sidebar.radio(
    "POC",
    ["Option 1", "Option 2"],
    caption=['Compare from database', 'Compare Words']
    , horizontal=True
)

threshold_spell = st.sidebar.slider(
    "Spelling Similarity Threshold Score", min_value=0, max_value=100, step=5, value=[60,80])

threshold_sound = st.sidebar.slider(
    "Phonetics Similarity Threshold Score", min_value=0, max_value=100, step=5, value=[60,80])

if poc_option == 'Option 1':
    df_data = pd.read_csv('./data/company_v3.csv')[['Dominant_Name']]\
                                .rename(columns={'Dominant_Name': 'Company Name'})
    df_data['Business Name'] = df_data['Company Name'].str.lower().apply(clean_text)
    
    epi = epitran.Epitran('tgl-Latn')
    df_data['ipa'] = df_data['Business Name'].apply(lambda x: epi.transliterate(x))
    
    # Create columns for the title and logo
    col1, col2 = st.columns([3.5, 1])  # Adjust the ratio as needed
    
    # Title in the first column
    with col1:
        st.title("📋 BNRD Business Name Validation")
        st.write(
            "This app checks for similarity of an input business name with existing registered business names."
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
    
    text_input = st.text_input(
            "Input Business Name 👇",
        )
    input_bn = re.sub(r'[^A-Za-z0-9 ]', '', text_input.lower())
    
    if st.button('Validate Business Name'):
        df_bn = df_data.copy()
        df_bn['levenshtein'] = df_bn['Business Name'].apply(lambda x: fuzz.ratio(input_bn, x))
    
        if 100 in df_bn['levenshtein'].values:
            st.title(f"Business Name already exists")
        else:
            # df_bn['soundex'] = df_bn['Business Name'].apply(lambda x: fuzz.ratio(jellyfish.soundex(input_bn), 
            #                                                                      jellyfish.soundex(x)))
            # df_bn['metaphone'] = df_bn['Business Name'].apply(lambda x: fuzz.ratio(jellyfish.metaphone(input_bn), 
            #                                                                        jellyfish.metaphone(x)))
            df_bn['epitran'] = df_bn['ipa'].apply(lambda x: fuzz.ratio(epi.transliterate(input_bn), x))
    
            
            if (df_bn['levenshtein'] < threshold_spell[0]).all() & (df_bn['epitran'] < threshold_sound[0]).all():
                st.title(f"Approved Business Name")
            elif (df_bn['levenshtein'] >= threshold_spell[1]).any() & (df_bn['epitran'] >= threshold_sound[1]).any():
                df_spell = df_bn.loc[df_bn['levenshtein'] >= threshold_spell[1]].sort_values('levenshtein', 
                                                                                          ascending=False)[['Company Name', 
                                                                                                            'levenshtein']].reset_index(drop=True)
                df_sound = df_bn.loc[df_bn['epitran'] >= threshold_sound[1]].sort_values('epitran', 
                                                                                          ascending=False)[['Company Name', 
                                                                                                            'epitran']].reset_index(drop=True)
                st.title(f"Business Name is too similar with an exisiting Busines Name")
                col2, col3 = st.columns([2.5, 2.5])  # Adjust the ratio as needed
                with col2:
                    st.write("Spelling Similarity")
                    st.dataframe(df_spell, height=300, width=300)
                with col3:
                    st.write("Phonetic Similarity")
                    st.dataframe(df_sound, height=300, width=300)
            else:
                df_spell = df_bn.loc[df_bn['levenshtein'] >= threshold_spell[0]].sort_values('levenshtein', 
                                                                                          ascending=False)[['Company Name', 
                                                                                                            'levenshtein']].reset_index(drop=True)
                df_sound = df_bn.loc[df_bn['epitran'] >= threshold_sound[0]].sort_values('epitran', 
                                                                                          ascending=False)[['Company Name', 
                                                                                                            'epitran']].reset_index(drop=True)
                st.title(f"For Post Evaluation")
                col2, col3 = st.columns([2.5, 2.5])  # Adjust the ratio as needed
                with col2:
                    st.write("Spelling Similarity")
                    st.dataframe(df_spell, height=300, width=300)
                with col3:
                    st.write("Phonetic Similarity")
                    st.dataframe(df_sound, height=300, width=300)

else:

     # Create columns for the title and logo
    col1, col2 = st.columns([3.5, 1])  # Adjust the ratio as needed
    
    # Title in the first column
    with col1:
        st.title("📋 BNRD Business Name Validation")
        st.write(
            "This app checks for spelling and phonetic similarity of an input word with the other input word/s."
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
    
    text_input = st.text_input(
            "Input Business Name 👇",
        )
    input_bn = re.sub(r'[^A-Za-z0-9 ]', '', text_input.lower())

    st.dataframe(pd.Dataframe(columns=['Business Name']), height=300, width=300)

    if st.button('Validate Business Name'):
        None
