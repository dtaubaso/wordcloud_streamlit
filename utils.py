import pandas as pd
import requests, re
from unicodedata import normalize
from urllib.parse import urlparse
from collections import Counter
from itertools import chain

stopwords = requests.get("https://raw.githubusercontent.com/dtaubaso/aux/main/stopwords").text.split("\n")

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

def generar_frec_dict(df, col_text, col_num, ngrams, num_keywords, stopw):
    if stopw:
       stopwords.extend(stopw)
    if 'http' in df[col_text][0]:
       df['clean_text'] = df[col_text].apply(lambda x: reemplazar_amp(x))
       df['clean_text'] =  df['clean_text'].apply(lambda x: obtener_slug(x))
       df.dropna(inplace=True)
       df['clean_text'] = df['clean_text'].apply(lambda x: clean_url(x))
       df[col_text] = df['clean_text']
    df['text_clean'] = df[col_text].apply(lambda x: normalizar(x))
    df = df.dropna()
    tokens = word_tokenize(df['text_clean'].tolist(), ngrams)
    df['tokens'] = tokens
    if col_num == "Ninguna":
      tokens = list(chain.from_iterable(tokens))
      return dict(Counter(tokens).most_common(num_keywords))
    else:
      df = df[['tokens', col_num]]
      df['len'] = df['tokens'].apply(lambda x: len(x))
      df[f'{col_num}_prom'] = df[col_num]/df['len']
      df = df.explode('tokens', ignore_index=True)
      df = df.dropna()
      df = df.sort_values(f'{col_num}_prom', ascending=False)
      df = df.groupby('tokens').sum(numeric_only=True).reset_index()
      df = df.head(num_keywords)
      df[f'{col_num}_prom'] = df[f'{col_num}_prom'].astype('int')
      return df.set_index('tokens')[f'{col_num}_prom'].to_dict()