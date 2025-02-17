import pandas as pd
import tratamentoDados as td

# Carregar tabelas de referência e consulta
tabela_referencia = pd.read_csv('C:\\Users\\gesbarreto\\Downloads\\FindStatus\\src\\Tabelas\\Suplementos Aracaju com Endereço.csv', sep=';', on_bad_lines='skip')
tabela_consulta = pd.read_csv('C:\\Users\\gesbarreto\\Downloads\\FindStatus\\src\\Tabelas\\estabelecimentos_Veiculos em Aracaju, SE.csv', sep=';', on_bad_lines='skip')

# Aplicar a função em cada linha do DataFrame
tabela_referencia[["LOGRADOURO-TEXTO", "NUMERO"]] = tabela_referencia["LOGRADOURO"].apply(
    lambda x: pd.Series(td.extrair_endereco(x))
)

# Exibir colunas das tabelas
print(tabela_referencia.columns)
print(tabela_consulta.columns)

# Salvar dados processados
td.save_data(tabela_referencia, 'Suplementos Aracaju com Endereço')

