from filter import filtervcf
from annotation import annotationvcf
import argparse
import os
def main():
    #Processa os argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Filtra e anota variantes a partir de um arquivo VCF.")
    parser.add_argument("-input", type=str, required=True, help="arquivo vcf")
    parser.add_argument("-output", type=str, required=True, help='nome da saida em formato tsv')
    parser.add_argument("-dp", type=float, dest='profundidade', required=True, help="Valor mínimo de profundidade para filtrar as variantes")
    parser.add_argument("-af", type=float, dest='frequencia', default=0.5, help="Valor mínimo de frequência para filtrar as variantes, por padrão é 0.5")
    parser.add_argument("-db", type=str, dest='database', help="Banco de dados para retornar a anotação da frequencia populacional, por padrão retorna todos")
    
    args = parser.parse_args()

    #Chama o script de filtragem com base na profundidade e frequencia determinadas
    filtered = filtervcf(input = args.input, output = args.output, dp = args.profundidade, af = args.frequencia)
    filtered.filter()

    filtered.filtered_vcf
    
    # Chama o script de anotação informando o banco de dados de onde devem ser anotadas as frequencias populacionais
    if args.database:
        annotated = annotationvcf(input = filtered.filtered_vcf, db = args.database)
        annotated.annotation()
   
    # Chama o script de anotação e todos os bancos de todas as frequencias populacionais disponiveis são retornados
    else:
        annotated = annotationvcf(input = filtered.filtered_vcf)
        annotated.annotation()
    
    annotated.merged

    



    # Editar o nome do arquivo de saída com base na string fornecida:
    base, ext, = os.path.splitext(args.output)
    args.output = base + "_annotated" + ext
    
    # Salvar as variantes filtradas em um novo arquivo VCF
    annotated.merged.to_csv(args.output, sep='\t', index=False)
    print("Variantes anotadas salvas em: ", args.output)

if __name__ == "__main__":
    main()