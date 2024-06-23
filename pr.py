import streamlit as st

# Título de la aplicación
st.title("Mostrar/Ocultar Casilla de Opciones")

# Primera casilla de opciones
option = st.selectbox(
    "Selecciona una opción:",
    ["Mostrar", "Ocultar"]
)

# Mostrar u ocultar la segunda casilla de opciones basada en la selección anterior
if option == "Mostrar":
    sub_option = st.selectbox(
        "Selecciona una sub-opción:",
        ["Sub-opción 1", "Sub-opción 2", "Sub-opción 3"]
    )
    st.write(f"Has seleccionado: {sub_option}")

# Botón para confirmar la selección principal
if st.button("Enviar"):
    st.write(f"Has seleccionado: {option}")