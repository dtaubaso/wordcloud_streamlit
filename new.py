import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Configurar la página con un título y un ícono
st.set_page_config(page_title="Generador de WordCloud", page_icon=":cloud:")
                   
def wordcloud_generator(frec_dict):
  font = "lora.ttf"
  wordcloud = WordCloud(font_path = font, width = 3500, height = 2000, background_color = "white",
                        color_func= lambda *args, **kwargs: "black", 
                        max_words = 100, random_state = 5).generate_from_frequencies(frec_dict)
  fig, ax = plt.subplots(figsize=(30, 15))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.show()
  st.pyplot(fig)

st.title('Generador de WordCloud')
lista = None
frec_dict = None
uploaded_file = st.file_uploader("Sube un archivo")
if uploaded_file is not None:
    lista = uploaded_file.read().decode("utf-8").split("\n")

if lista:
    frec_dict = dict(Counter(lista).most_common())
if st.button("Enviar"):
    wordcloud_generator(frec_dict)