import pandas as pd
import os
class filtervcf:
    def __init__(self, input = None, output = None, dp = None, af = 0.5):
        self.input = input
        self.output = output
        self.dp = dp           
        self.af = af
    def filter(self):
        
        # Função para extrair informações relevantes do INFO
        def extract_info(info_str):
            info_dict = {}
            info_list = info_str.split(";")
            for item in info_list:
                key_value = item.split("=")
                if len(key_value) == 2:
                    info_dict[key_value[0]] = key_value[1]
            return info_dict

        # Função para lidar com o formato de frequência (AF) em lista separada por vírgulas
        def process_af(af_str):
            af_list = af_str.split(",")
            return max(map(float, af_list))

        
        vcf_df = pd.read_csv(self.input, sep='\t', comment='#', header=None)

        # Renomear as colunas
        vcf_df.columns = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "SAMPLE"]

        # Extrair as informações relevantes do INFO
        vcf_df["INFO_DICT"] = vcf_df["INFO"].apply(extract_info)

        # Converter tipos de dados
        vcf_df["DP"] = vcf_df["INFO_DICT"].apply(lambda x: int(x["DP"]) if "DP" in x else None)
        vcf_df["AF"] = vcf_df["INFO_DICT"].apply(lambda x: process_af(x["AF"]) if "AF" in x else None)

        # Filtrar com base na frequência e profundidade
        self.filtered_vcf = vcf_df[(vcf_df["AF"] is not None) & (vcf_df["DP"] is not None) & (vcf_df["AF"] >= self.af) & (vcf_df["DP"] >= self.dp)]

        # Editar o nome do arquivo de saída com base na string fornecida:
        base, ext, = os.path.splitext(self.output)
        self.output = base + "_filtred" + ext

        # Salvar as variantes filtradas em um novo arquivo VCF
        self.filtered_vcf.to_csv(self.output, sep='\t', index=False)
        print("Variantes filtradas salvas em: ", self.output)

        #return filtered_vcf
