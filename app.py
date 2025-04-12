import streamlit as st
from main import run_pesquisador

st.title("🔍 Pesquisador web com DuckDuckGo")
st.write(
    "Esse é um projeto de pesquisa automatizada que utiliza IA e DuckDuckGo para responder perguntas com base em dados da web."
)

pergunta_usuario = st.text_area("Digite sua pergunta sobre um tema do seu interesse:")

if st.button("Pesquisar"):
    if not pergunta_usuario:
        st.warning("Por favor, digite uma pergunta.")
    else:
        st.write("Pesquisando na web usando DuckDuckGo...")
        # Chama a função de pesquisa
        resultado = run_pesquisador(pergunta_usuario)
        st.subheader("Resultado da pesquisa:")
        st.write(resultado)