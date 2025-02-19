import pandas as pd
import tratamentoDados as td

# Caminho dos arquivos
arquivo_referencia = 'C:\\Users\\gesbarreto\\Downloads\\FindStatus\\src\\Tabelas\\.TabelaReferencia\\Suplementos Aracaju com Endereco.csv'
arquivo_consulta   = 'C:\\Users\\gesbarreto\\Downloads\\FindStatus\\src\\Tabelas\\TabelaConsulta\\estabelecimentos_suplemento em Aracaju.csv'


# 1. ABRIR O ARQUIVO
tabela_referencia = pd.read_csv(arquivo_referencia, sep=';', on_bad_lines='skip')

# 2. FAZER ALTERAÇÕES
# Aplicar a função em cada linha do DataFrame
tabela_referencia[["LOGRADOURO-TEXTO", "NUMERO"]] = tabela_referencia["LOGRADOURO"].apply(
    lambda x: pd.Series(td.extrair_endereco(x))
)

# 3. SALVAR O ARQUIVO ATUALIZADO
tabela_referencia.to_csv(arquivo_referencia, index=False, sep=';')

# 4. REABRIR O ARQUIVO PARA CONTINUAR O PROCESSAMENTO
tabela_referencia = pd.read_csv(arquivo_referencia, sep=';', on_bad_lines='skip')
tabela_consulta = pd.read_csv(arquivo_consulta, sep=';', on_bad_lines='skip')




# Faz a Comparação de cada item da Tabala, nivel de compatibilidade 100%

resultados = []

for index_b, linha_b in tabela_consulta.iterrows():
    encontrado = False
    for index_a, linha_a in tabela_referencia.iterrows():
        
        if ((linha_b['CEP'] == linha_a['CEP']) and 
            (linha_b['BAIRRO'] == linha_a ['BAIRRO']) and 
            (linha_b['LOGRADOURO'] in linha_a['LOGRADOURO-TEXTO'])):
            print('Encontrado: ', linha_b['LOGRADOURO'])     
            encontrado = True
            break
    
    
    if encontrado:
        resultados.append({'NOME DO ESTABELECIMENTO': linha_b['NOME DO ESTABELECIMENTO'],
                           'LOGRADOURO': linha_b['LOGRADOURO'],
                           'NUMERO': linha_b['NUMERO'],
                           'BAIRRO': linha_b['BAIRRO'],
                           'CEP': linha_b['CEP'],
                           'ENCONTRADO': 'Encontrado'})
    else:
        resultados.append({'NOME DO ESTABELECIMENTO': linha_b['NOME DO ESTABELECIMENTO'],
                           'LOGRADOURO': linha_b['LOGRADOURO'],
                           'NUMERO': linha_b['NUMERO'],
                           'BAIRRO': linha_b['BAIRRO'],
                           'CEP': linha_b['CEP'],
                           'ENCONTRADO': 'Não Encontrado'})
        
        

# Salvar dados processados
tabela_resultado = pd.DataFrame(resultados)
td.save_data(tabela_resultado, 'Suplementos Aracaju com Endereço')


print('Comparação concluída. O resultado foi salvo em Resultados/CSV/')



