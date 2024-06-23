import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

# Función para generar el WordCloud
def generate_wordcloud(data_dict):
    font = "lora.ttf"
    wordcloud = WordCloud(font_path=font, width=3500, height=2000, background_color="white",
                          color_func=lambda *args, **kwargs: "black", max_words=100, random_state=5).generate_from_frequencies(data_dict)
    
    fig, ax = plt.subplots(figsize=(30, 15))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    
    # Mostrar la figura en Streamlit
    st.pyplot(fig)


st.set_page_config(page_title="WordCloud con Ngrams desde CSV", page_icon=":penguin:")

# Configuración de la app Streamlit
st.title('Generador de WordCloud con Ngrams desde CSV')
#st.write('Suba un archivo CSV para generar un WordCloud'}
# Cargador de archivos CSV
uploaded_file = st.file_uploader("Suba un archivo CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    cols = data.columns.tolist()
    col_text = st.radio("Elija la columna que tiene los títulos",
                           cols, horizontal=True)
    col_para_num = cols.copy()
    col_para_num.append("Ninguna")
    col_num = st.radio("Elija la columna que tiene las métricas",
                           col_para_num, horizontal=True)
    
       # Preguntar al usuario cuántas palabras clave graficar
    num_keywords = st.number_input("Cantidad de palabras clave a graficar", min_value=10, max_value=500, value=100)
    
    ngrams = st.radio("Cantidad de ngrams a graficar", [1, 2], horizontal=True)

    ngrams = int(ngrams)
    stopw = None
    stopw = st.text_input("Ingrese stopwords de ser necesario (puede ser un término brand)\
                              separadas por coma")
    if stopw:
        stopw = stopw.split(",")

    if st.button("Generar"):

        if len(data)>0 and col_text and col_num and ngrams and num_keywords:
            try:
                with st.spinner('Generando WordCloud...'):
                    data_dict = generar_frec_dict(data, col_text, col_num, ngrams, num_keywords, stopw)
                    generate_wordcloud(data_dict)
            except Exception:
                st.error("Ocurrió un error, intente nuevamente")
        else:
            st.error("Por favor complete todos los campos.")