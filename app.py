import streamlit as st
from main import run_pesquisador

st.title("Agente de IA capaz de utilizar wikipedia para escrever artigos")
st.write(
    "Esse é um projeto de pesquisa automatizada que utiliza API da wikipedia para trazer dados relevantes e importantes sobre determinado tema."
)

pergunta_usuario = st.text_area("Digite sobre um tema do seu interesse:")

if st.button("Pesquisar"):
    if not pergunta_usuario:
        st.warning("Por favor, digite um tema para busca no wikipedia.")
    else:
        st.write("Pesquisando na wikipedia...")
        # Chama a função de pesquisa
        resultado = run_pesquisador(pergunta_usuario)
        
        # Exibe os resultados formatados
        st.subheader(f"Tema: {resultado.tema}")
        
        if resultado.resultados:
            st.write("### Resultados:")
            for res in resultado.resultados:
                st.write(f"**{res.topico}:** {res.descricao}")
        
        st.write("### Resumo:")
        st.write(resultado.resumo)