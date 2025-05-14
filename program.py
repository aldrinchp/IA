import streamlit as st
from openai import OpenAI

# Sidebar: entrada de clave API
st.sidebar.title("🔐 Configuración")
api_key = st.sidebar.text_input("Introduce tu clave de API de OpenAI:", type="password")

# Solo continuar si la clave fue ingresada
if api_key:
    # Crear cliente de OpenAI con la clave proporcionada
    client = OpenAI(api_key=api_key)

    # Título de la app
    st.title("🤖 Analizador de Juegos Olímpicos con GPT")

    # Entrada de texto para la pregunta del usuario
    pregunta = st.text_area("Escribe tu pregunta sobre los Juegos Olímpicos:")

    # Botón para enviar la pregunta
    if st.button("📤 Enviar pregunta al modelo"):
        if pregunta.strip() == "":
            st.warning("⚠️ Por favor, escribe una pregunta antes de enviarla.")
        else:
            # Llamada a la API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Actúa como un historiador experto en los Juegos Olímpicos. "
                            "Solo responde preguntas que estén claramente relacionadas con los Juegos Olímpicos. "
                            "Si la pregunta no trata sobre los Juegos Olímpicos (como FIFA, Copa del Mundo, otros deportes no olímpicos, etc.), responde únicamente con el mensaje: "
                            "'❌ Lo siento, esta pregunta no está relacionada con los Juegos Olímpicos.'"

                        )
                    },
                    {
                        "role": "user",
                        "content": pregunta
                    }
                ]
            )
            respuesta = response.choices[0].message.content
            st.markdown("### 🧠 Respuesta del modelo:")
            st.write(respuesta)
else:
    st.warning("🔑 Por favor, introduce tu clave de API de OpenAI en el sidebar para continuar.")
