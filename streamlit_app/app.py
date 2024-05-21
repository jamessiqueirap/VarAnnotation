import streamlit as st
from filter import filtervcf
from annotation import annotationvcf
import os

def main():
    st.title("Filtragem e Anotação de Variantes VCF")

    # Entrada do usuário para o arquivo VCF
    vcf_file = st.file_uploader("Escolha um arquivo VCF", type="vcf")
    if vcf_file is not None:
        input_vcf = vcf_file.name
        with open(input_vcf, "wb") as f:
            f.write(vcf_file.getbuffer())

    # Nome do arquivo de saída
    output_file = st.text_input("Nome do arquivo de saída (formato TSV)", "output.tsv")

    # Parâmetros de filtragem
    profundidade = st.number_input("Valor mínimo de profundidade para filtrar as variantes", min_value=0.0, step=0.1)
    frequencia = st.number_input("Valor mínimo de frequência para filtrar as variantes", value=0.5, min_value=0.0, step=0.01)

    # Banco de dados para anotação
    database = st.text_input("Banco de dados para anotação da frequência populacional (opcional)")

    # Botão para processar o VCF
    if st.button("Processar"):
        if vcf_file is None:
            st.error("Por favor, carregue um arquivo VCF")
        else:
            # Barra de progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Atualiza a barra de progresso e status
                status_text.text("Filtrando variantes...")
                progress_bar.progress(20)
                
                # Chama o script de filtragem com base na profundidade e frequencia determinadas
                filtered = filtervcf(input=input_vcf, output=output_file, dp=profundidade, af=frequencia)
                filtered.filter()

                progress_bar.progress(50)
                
                # Atualiza a barra de progresso e status
                status_text.text("Anotando variantes...")

                # Chama o script de anotação informando o banco de dados de onde devem ser anotadas as frequências populacionais
                if database:
                    annotated = annotationvcf(input=filtered.filtered_vcf, db=database)
                else:
                    annotated = annotationvcf(input=filtered.filtered_vcf)
                
                annotated.annotation()

                progress_bar.progress(80)
                
                # Editar o nome do arquivo de saída com base na string fornecida
                base, ext = os.path.splitext(output_file)
                output_file_annotated = base + "_annotated" + ext

                # Salvar as variantes filtradas em um novo arquivo VCF
                annotated.merged.to_csv(output_file_annotated, sep='\t', index=False)
                progress_bar.progress(100)

                # Mensagem de sucesso
                st.success(f"Variantes anotadas salvas em: {output_file_annotated}")
                st.download_button(
                    label="Download arquivo anotado",
                    data=open(output_file_annotated, "rb").read(),
                    file_name=output_file_annotated,
                    mime='text/tsv'
                )

            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")
                progress_bar.progress(0)
                status_text.text("")

if __name__ == "__main__":
    main()
