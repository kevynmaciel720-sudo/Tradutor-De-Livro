import streamlit as st
import pdfplumber
from deep_translator import GoogleTranslator
import io

# Configuração inicial da página web
st.set_page_config(page_title="Tradutor de Livros PDF", page_icon="📚", layout="wide")

st.title("📚 Tradutor de Livros e PDFs")
st.write("Faça o upload do seu livro em PDF, escolha o idioma e baixe a versão traduzida.")

# Barra lateral para configurações
st.sidebar.header("Configurações")

# Definição clara dos idiomas usando os códigos padrão que o tradutor exige
idiomas_suportados = {
    "Português": "pt",
    "Inglês": "en",
    "Espanhol": "es",
    "Francês": "fr",
    "Alemão": "de",
    "Italiano": "it"
}

idioma_destino_nome = st.sidebar.selectbox("Selecione o idioma de destino:", list(idiomas_suportados.keys()))
codigo_destino = idiomas_suportados[idioma_destino_nome]

# Upload do arquivo
uploaded_file = st.file_uploader("Selecione o arquivo PDF do livro", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF carregado com sucesso!")
    
    if st.button("Iniciar Tradução do Livro"):
        try:
            # Inicializa o tradutor com detecção automática de origem e o destino correto
            translator = GoogleTranslator(source='auto', target=codigo_destino)
            
            texto_traduzido_completo = ""
            
            with pdfplumber.open(uploaded_file) as pdf:
                total_paginas = len(pdf.pages)
                st.info(f"O livro possui {total_paginas} páginas. Iniciando processamento...")
                
                progresso = st.progress(0)
                status_text = st.empty()
                
                for i, pagina in enumerate(pdf.pages):
                    status_text.text(f"Processando página {i+1} de {total_paginas}...")
                    
                    texto_original = pagina.extract_text()
                    
                    if texto_original:
                        # Divisão em parágrafos para não estourar o limite de caracteres por requisição
                        paragrafos = texto_original.split("\n")
                        texto_pagina_traduzida = ""
                        
                        for p in paragrafos:
                            if p.strip():
                                try:
                                    # Traduz linha por linha/parágrafo por parágrafo
                                    traducao_linha = translator.translate(p)
                                    texto_pagina_traduzida += traducao_linha + "\n"
                                except:
                                    # Caso falhe em alguma linha específica, mantém a original para não travar
                                    texto_pagina_traduzida += p + "\n"
                        
                        # Mostra o resultado da página em tempo real na tela
                        st.subheader(f"Página {i+1}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Original:**")
                            st.write(texto_original)
                        with col2:
                            st.markdown("**Traduzido:**")
                            st.write(texto_pagina_traduzida)
                        
                        st.markdown("---")
                        
                        texto_traduzido_completo += f"--- PÁGINA {i+1} ---\n\n{texto_pagina_traduzida}\n\n"
                    
                    progresso.progress((i + 1) / total_paginas)
                
                status_text.text("✨ Tradução concluída com sucesso!")
                
                # Cria o arquivo para download
                buffer = io.BytesIO()
                buffer.write(texto_traduzido_completo.encode("utf-8"))
                buffer.seek(0)
                
                st.download_button(
                    label=f"📥 Baixar Livro Traduzido ({idioma_destino_nome})",
                    data=buffer,
                    file_name=f"livro_traduzido_{codigo_destino}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Ocorreu um erro durante a tradução: {e}")
