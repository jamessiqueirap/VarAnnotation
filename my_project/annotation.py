from xml.dom.expatbuilder import Namespaces
from easy_entrez import EntrezAPI
from easy_entrez.parsing import xml_to_string
from easy_entrez.parsing import parse_dbsnp_variants
import pandas as pd
from pandas import DataFrame
from pandas import Series

class annotationvcf:
    def __init__(self, input = None, db = None):
        self.input = input
        self.db = db
    def annotation(self):
        
        #Gerar o entrez
        entrez_api = EntrezAPI(
            'snp_var_find',
            'jamessiqueirap@usp.br',
            # optional
            return_type='json'
        )

        #recuperar os id's a partir da posição
        vcf = self.input
        
        #Retirando as variantes com '.' no rs
        tmp = vcf[vcf.ID == '.']

        dbsnp_ids = []
        for CHROM, POS in zip(tmp.CHROM, tmp.POS):
            
            rsids = entrez_api.search(
                dict(chromosome=CHROM, organism='human', POSITION_GRCH37=POS),
                database='snp',
                max_results=1
            )
            try:
                dbsnp_ids.append(rsids.data['esearchresult']['idlist'][0])
            except:
                pass

        tmp = vcf[vcf.ID != '.']
        l=list(tmp.ID)
        dbsnp_ids.extend(l)
        #del tmp

        #Anota os ids com base no banco
        result = entrez_api.fetch(dbsnp_ids, max_results=10_000, ignore_max_results_limit=True, database='snp')

        namespaces = {'ns0': 'https://www.ncbi.nlm.nih.gov/SNP/docsum'}
        geneidspaces = {'ns0': 'https://www.ncbi.nlm.nih.gov/SNP/docsum'}
        
        #identifica os genes associados as variantes
        gene_names = {
            'rs' + document_summary.get('uid'): [
                element.text
                for element in document_summary.findall('.//ns0:GENE_E/ns0:NAME', namespaces)
            ]
            for document_summary in result.data
        }

        gene_ids = {
            'rs' + document_summary.get('uid'): [
                element.text
                for element in document_summary.findall('.//ns0:GENE_E/ns0:GENE_ID', geneidspaces)
            ]
            for document_summary in result.data
        }

        toremove = [ i for i in gene_names.keys() if gene_names[i] == [] ]
        _ = [ gene_names.pop(i) for i in toremove ]
        _ = [ gene_ids.pop(i) for i in toremove ]

        #extrai as coordenadas das variantes
        variants = parse_dbsnp_variants(result)
        
        #gera o dataframe com as coordenadas associado as informacoes dos genes anotados
        coordinate = variants.coordinates.reset_index(inplace=False)
        coordinate['Gene_Name'] = [None] * len(coordinate)
        coordinate['Gene_ids'] = [None] * len(coordinate)
        
        for i, k in zip(range(len(coordinate)), coordinate.rs_id):
            try:
                coordinate.loc[i, 'Gene_Name'] = gene_names[k]
                coordinate.loc[i, 'Gene_ids'] = gene_ids[k]
            except:
                pass

        if self.db is not None:
            #filtra o dataframe de frequencia com base em um banco de dados
            variantfreq = variants.alt_frequencies[variants.alt_frequencies.study == self.db]
        else:
            #Capta todos os bancos de dados
            variantfreq = variants.alt_frequencies


        #Une todas as informações de anotação com as informações dos genes 
        merged = pd.merge(coordinate, variantfreq)
        
        self.merged = merged