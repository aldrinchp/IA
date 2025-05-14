import streamlit as st
from openai import OpenAI
import pandas as pd
import os

# Título de la aplicación
st.title("🤖 Analizador de Juegos Olímpicos con GPT")

# Sidebar para ingresar clave
with st.sidebar:
    st.header("🔐 Configuración")
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    api_input = st.text_input("Ingresa tu API Key de OpenAI:", type="password")
    if api_input:
        st.session_state.api_key = api_input
        st.success("🔓 Clave almacenada correctamente.")

# Validación de clave
if not st.session_state.api_key:
    st.warning("🔑 Por favor, ingresa tu clave API en la barra lateral.")
    st.stop()

# Entrada de texto
pregunta = st.text_area("✍️ Escribe tu pregunta sobre los Juegos Olímpicos:")

# Cargar el dataset
dataset_path = '/athlete_events_reduced_rows.csv'
try:
    df = pd.read_csv(dataset_path)

    # Mostrar el dataset completo como tabla
    st.markdown("### 📊 Vista previa del dataset:")
    st.dataframe(df)

    # Crear un contexto resumido del dataset para el modelo
    columnas = ", ".join(df.columns)
    resumen = df.describe(include='all').transpose().fillna("").to_string()

    df_context = f"""Este dataset contiene información sobre atletas olímpicos con las siguientes columnas:
{columnas}

Resumen estadístico y de valores únicos por columna:
{resumen}
"""

except Exception as e:
    st.error(f"❌ Error al cargar el dataset: {e}")
    df_context = ""

# Botón para enviar la pregunta
if st.button("📤 Enviar pregunta al modelo"):
    if pregunta.strip() == "":
        st.warning("⚠️ Escribe una pregunta antes de enviarla.")
    else:
        with st.spinner("Consultando al modelo..."):
            try:
                client = OpenAI(api_key=st.session_state.api_key)

                system_prompt = (
                    "Actúa como un historiador experto en los Juegos Olímpicos. "
                    "Responde de forma clara y precisa cualquier pregunta relacionada con los países, atletas, deportes o estadísticas de los Juegos Olímpicos. "
                    "Si una pregunta no está relacionada con los Juegos Olímpicos, responde solamente con: "
                    "'❌ Lo siento, esta pregunta no está relacionada con los Juegos Olímpicos.'\n\n"
                    f"{df_context}"
                )

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": pregunta}
                    ]
                )

                respuesta = response.choices[0].message.content
                st.markdown("### 🧠 Respuesta del modelo:")
                st.write(respuesta)

            except Exception as e:
                st.error(f"❌ Error al conectarse con la API de OpenAI: {e}")
