import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator

def main():
    st.set_page_config(page_title="Tradutor de Livro", layout="wide")
    st.title("📖 Tradutor de Livro")
    
    # Sidebar
    st.sidebar.header("Configurações")
    idioma_destino = st.sidebar.selectbox(
        "Selecione o idioma de destino",
        ["português", "espanhol", "inglês", "francês", "alemão"]
    )
    
    # Upload de arquivo
    arquivo_pdf = st.file_uploader("Escolha um arquivo PDF", type="pdf")
    
    if arquivo_pdf is not None:
        st.success("Arquivo carregado com sucesso!")
        
        try:
            # Extrai texto do PDF
            with pdfplumber.open(arquivo_pdf) as pdf:
                total_paginas = len(pdf.pages)
                st.info(f"Total de páginas: {total_paginas}")
                
                # Processa cada página
                for idx, page in enumerate(pdf.pages, 1):
                    texto = page.extract_text()
                    
                    if texto:
                        st.subheader(f"Página {idx}")
                        
                        # Traduz o texto
                        tradutor = GoogleTranslator(source_language='auto', target_language=idioma_destino[0])
                        texto_traduzido = tradutor.translate(texto)
                        
                        # Exibe lado a lado
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Original:**")
                            st.write(texto)
                        
                        with col2:
                            st.write("**Traduzido:**")
                            st.write(texto_traduzido)
                        
                        st.divider()
        
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")

if __name__ == "__main__":
    main()
