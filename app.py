import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

# Función para generar el WordCloud
def generate_wordcloud(data):
    font = "lora.ttf"
    wordcloud = WordCloud(font_path = font, width = 3500, height = 2000, background_color = "white",
                        color_func= lambda *args, **kwargs: "black", max_words = 100, random_state = 5).generate_from_frequencies(data_dict)
    #plt.figure(figsize = (30,15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()

# Configuración de la app Streamlit
st.title('Generador de WordCloud desde CSV')
st.write('Sube un archivo CSV para generar un WordCloud')

# Cargador de archivos CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Inferir el nombre de las columnas
    cols = data.columns.tolist()
    
    # Si hay dos columnas y una de ellas es numérica, asumimos que es la frecuencia
    if len(cols) == 2:
        keyword_col = cols[0]
        freq_col = cols[1]
        if data[freq_col].dtype in [int, float]:
            data_dict = dict(zip(data[keyword_col], data[freq_col]))
        else:
            # Si el tipo de datos no es numérico, calculamos la frecuencia manualmente
            text = ' '.join(data[keyword_col].astype(str).tolist())
            word_freq = pd.Series(text.split()).value_counts()
            data_dict = word_freq.to_dict()
    # Si hay solo una columna, calculamos la frecuencia manualmente
    else:
        text = ' '.join(data.iloc[:, 0].astype(str).tolist())
        word_freq = pd.Series(text.split()).value_counts()
        data_dict = word_freq.to_dict()
    
    # Preguntar al usuario cuántas palabras clave graficar
    num_keywords = st.number_input("Cantidad de palabras clave a graficar", min_value=1, max_value=len(data_dict), value=10)
    
    # Seleccionar las N palabras clave con mayor frecuencia
    sorted_data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True)[:num_keywords])
    
    # Generar el WordCloud
    generate_wordcloud(sorted_data_dict)