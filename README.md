# Filtragem e Anotação de Variantes

Esta aplicação oferece uma maneira conveniente de filtrar e anotar variantes genéticas a partir de arquivos no formato VCF (Variant Call Format). Ela é útil em análises genômicas para identificar variantes relevantes em estudos de associação genética, mapeamento de genes e outros tipos de análises.

O Dockerfile incluído neste repositório permite a criação de um ambiente isolado com todas as dependências necessárias pré-configuradas. 

## Funcionalidades Principais:

- **Filtragem Personalizada:** A aplicação permite filtrar variantes com base nos critérios de profundidade mínima de leitura (`-dp`) e frequência mínima (`-af`) das variantes. 
- **Anotação Genômica:** Além da filtragem, a aplicação também oferece a funcionalidade de anotar as variantes com informações adicionais, como frequência populacional. 
- **Flexibilidade de Banco de Dados:** Você pode escolher o banco de dados a partir do qual deseja realizar a anotação das frequências populacionais, ou então, deixar que todas as frequências disponíveis sejam retornadas.
- **Saída em Formato TSV:** As variantes filtradas e anotadas são salvas em um arquivo TSV (tab-separated values), facilitando sua análise posterior.

## Como Usar:

1. **Construção da imagem:**
- Para construção da imagem utilize o comando abaixo dentro da pasta baixada
   ```
     sudo docker build -t variantsearch .
   ```
2. **Execução:**
- Para executar a aplicação basta substituir as variáveis input e output pelos nomes dos seus arquivos, respectivamente, no comando abaixo:
     ```
     sudo docker run -it -v $(pwd):/input variantsearch -input /input/<arquivo.vcf> -output /input/<saida.tsv> -dp <valor de dp>
     ```

5. **Argumentos:**
   - `-input`: Caminho para o arquivo vcf de entrada.
   - `-output`: Nome do arquivo de saída no formato tsv contendo as variantes filtradas e anotadas.
   - `-dp`: Valor mínimo de profundidade para filtragem das variantes.
   - `-af`: Valor mínimo de frequência para filtragem das variantes (padrão: 0.5).
   - `-db`: Banco de dados para a anotação da frequência populacional (opcional).

6. **Saída:**
   - O arquivo TSV resultante conterá as variantes filtradas e anotadas.
   
Esta aplicação foi desenvolvida para simplificar o processo de análise de variantes genéticas em estudos genômicos. 
