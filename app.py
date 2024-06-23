import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import requests, re
from unicodedata import normalize
from urllib.parse import urlparse
from collections import Counter
from itertools import chain

stopwords = requests.get("https://raw.githubusercontent.com/dtaubaso/aux/main/stopwords").text.split("\n")

# Función para generar el WordCloud
def generate_wordcloud(data_dict):
    font = "lora.ttf"
    wordcloud = WordCloud(font_path = font, width = 3500, height = 2000, background_color = "white",
                        color_func= lambda *args, **kwargs: "black", max_words = 100, random_state = 5).generate_from_frequencies(data_dict)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()

def reemplazar_amp(url):
  pattern = r"\/amp\/|\/\?outputType=amp$"
  if re.search("\/amp$", url):
    return re.sub("\/amp$", "", url)
  elif re.search(pattern, url):
    return re.sub(pattern, "/", url)
  else:
    return url

def obtener_slug(url):
    # Parsear la URL
    parsed_url = urlparse(url)
    
    # Obtener el path de la URL
    path = parsed_url.path
    
    # Dividir el path en segmentos
    segments = path.strip('/').split('/')
    
    # Evaluar la longitud de los segmentos
    if len(segments) == 1 and segments[0]:  # Solo hay un segmento no vacío
        return segments[0]
    elif len(segments) > 1:  # Hay uno o más folders antes del slug
        return segments[-1]
    else:
        return float('nan')  # No hay suficiente información para un slug (e.g., "sitio.com/")

def clean_url(url):
   url = re.sub("\.html|\.phtml|id\d\d\d.*\.html|\_\d\_.*\.html|\d+\.html$", "", url)
   url = url.replace("/", " ")
   url = url.replace("-", " ")
   return url

def normalizar(palabra):
  palabra = re.sub(r'[^A-Za-záéíóúÁÉíÓÚüÜÑñ ]+', '', palabra)
  palabra = palabra.replace('ñ', '\001');
  palabra = normalize('NFKD', palabra).encode('ASCII', 'ignore').decode().replace('\001', 'ñ')
  palabra = [a.lower() for a in palabra.split() if a.lower() not in stopwords and len(a.lower())>2]
  palabra = " ".join(palabra)
  return palabra

def word_tokenize(text_list, phrase_len):
  split = [text.split() for text in text_list]
  return [[' '.join(s[i:i + phrase_len])
             for i in range(len(s) - phrase_len + 1)] for s in split]

def generar_frec_dict(df, col_text, col_num, ngrams, num_keywords):
    if 'http' in df[col_text][0]:
       df['clean_text'] = df[col_text].apply(lambda x: obtener_slug(x))
       df['clean_text'] = df['clean_text'].apply(lambda x: clean_url(x))
       df[col_text] = df['clean_text']
    df['text_clean'] = df[col_text].apply(lambda x: normalizar(x))
    df = df.dropna()
    tokens = word_tokenize(df['text_clean'].tolist(), ngrams)
    df['tokens'] = tokens
    if col_num is not "Ninguna":
      df = df[['tokens', col_num]]
      df['len'] = df['tokens'].apply(lambda x: len(x))
      df[f'{col_num}_prom'] = df[col_num]/df['len']
      df = df.explode('tokens', ignore_index=True)
      df = df.sort_values(f'{col_num}_prom', ascending=False)
      df = df.head(num_keywords)
      df = df[f'{col_num}_prom'].astype('int')
      return df.set_index('tokens')[f'{col_num}_prom'].to_dict()
    else:
      tokens = list(chain.from_iterable(tokens))
      return dict(Counter(tokens).most_common(num_keywords))


# Configuración de la app Streamlit
st.title('Generador de WordCloud desde CSV')
st.write('Suba un archivo CSV para generar un WordCloud')

# Cargador de archivos CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    cols = data.columns.tolist()
    col_text = st.radio("Elija la columna que tiene los títulos",
                           cols, horizontal=True)
    col_para_num = cols.copy()
    col_para_num.append("Ninguna")
    col_num = st.radio("Elija la columna que tiene la métrica",
                           col_para_num, horizontal=True)
    
       # Preguntar al usuario cuántas palabras clave graficar
    num_keywords = st.number_input("Cantidad de palabras clave a graficar", min_value=10, max_value=500, value=100)
    
    ngrams = st.radio("Cantidad de ngrams a graficar", [1, 2], horizontal=True)

    ngrams = int(ngrams)

    if st.button("Generar"):

        if len(data)>0 and col_text and col_num and ngrams and num_keywords:

        
            data_dict = generar_frec_dict(data, col_text, col_num, ngrams, num_keywords)

        
            generate_wordcloud(data_dict)
        else:
            st.error("Por favor complete todos los campos.")