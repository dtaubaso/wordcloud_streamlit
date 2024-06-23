import streamlit as st

uploaded_file = st.file_uploader("Sube un archivo")
if uploaded_file != None:
    print(uploaded_file)
    if uploaded_file.type == 'text/plain':
        print("text")
    elif uploaded_file.type == 'text/csv':
        print("csv")