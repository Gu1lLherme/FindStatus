import pandas as pd
import re
from unidecode import unidecode
from difflib import SequenceMatcher
import tratamentoDados as td

# =============================================================================
# Funções auxiliares
# =============================================================================

def normalize_text(texto):
    """
    Remove acentos, pontuação e espaços extras, deixando o texto em maiúsculas.
    """
    if pd.isna(texto):
        return ""
    # Remove acentos e coloca em maiúsculas
    texto = unidecode(texto).upper()
    # Remove qualquer caractere que não seja letra, número ou espaço
    texto = re.sub(r'[^A-Z0-9\s]', '', texto)
    # Remove espaços duplicados
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def similaridade(texto1, texto2):
    """
    Calcula a similaridade entre dois textos usando SequenceMatcher.
    """
    return SequenceMatcher(None, texto1, texto2).ratio()

# =============================================================================
# Configuração de caminhos dos arquivos
# =============================================================================

arquivo_referencia = 'C:\\Users\\gesbarreto\\Downloads\\FindStatus\\src\\Tabelas\\.TabelaReferencia\Suplementos Aracaju com Endereco.csv'
arquivo_consulta   = 'C:\\Users\\gesbarreto\\Downloads\\FindStatus\\src\\Tabelas\\TabelaConsulta\estabelecimentos_suplemento em Aracaju.csv'

# =============================================================================
# 1. ABRIR OS ARQUIVOS
# =============================================================================

tabela_referencia = pd.read_csv(arquivo_referencia, sep=';', on_bad_lines='skip')
tabela_consulta   = pd.read_csv(arquivo_consulta, sep=';', on_bad_lines='skip')

# =============================================================================
# 2. TRATAMENTO DOS DADOS - EXTRAÇÃO E PADRONIZAÇÃO DOS ENDEREÇOS
# =============================================================================

# Para a tabela de referência, extraímos os componentes do endereço
# Supondo que a função td.extrair_endereco retorne uma tupla ou lista no formato (logradouro_texto, numero)
tabela_referencia[["LOGRADOURO-TEXTO", "NUMERO"]] = tabela_referencia["LOGRADOURO"].apply(
    lambda x: pd.Series(td.extrair_endereco(x))
)

# Se os dados da consulta estiverem no mesmo formato que a referência,
# é interessante aplicar a mesma extração para garantir a consistência.


# Padroniza os textos (logradouro e bairro) para ambas as tabelas
tabela_referencia["LOGRADOURO-TEXTO"] = tabela_referencia["LOGRADOURO-TEXTO"].apply(normalize_text)
tabela_referencia["BAIRRO"] = tabela_referencia["BAIRRO"].apply(normalize_text)
tabela_consulta["LOGRADOURO-TEXTO"] = tabela_consulta["LOGRADOURO-TEXTO"].apply(normalize_text)
tabela_consulta["BAIRRO"] = tabela_consulta["BAIRRO"].apply(normalize_text)

# Se necessário, também padronize CEP (removendo espaços ou pontos, por exemplo)
tabela_referencia["CEP"] = tabela_referencia["CEP"].astype(str).str.replace('[\s.-]', '', regex=True)
tabela_consulta["CEP"]   = tabela_consulta["CEP"].astype(str).str.replace('[\s.-]', '', regex=True)

# =============================================================================
# 3. COMPARAÇÃO ENTRE AS TABELAS USANDO SIMILARIDADE
# =============================================================================

# Aqui definimos um limiar para a similaridade do logradouro. 
# Por exemplo, 0.8 (80% de similaridade) pode ser um bom ponto de partida.
LIMIAR_SIMILARIDADE = 0.5

resultados = []

for _, linha_consulta in tabela_consulta.iterrows():
    encontrado = False
    # Primeiro, filtra os possíveis matches pela igualdade de CEP e BAIRRO
    possiveis_matches = tabela_referencia[
        (tabela_referencia["CEP"] == linha_consulta["CEP"]) &
        (tabela_referencia["BAIRRO"] == linha_consulta["BAIRRO"])
    ]
    
    for _, linha_ref in possiveis_matches.iterrows():
        # Calcula a similaridade entre os logradouros padronizados
        sim = similaridade(linha_consulta["LOGRADOURO-TEXTO"], linha_ref["LOGRADOURO-TEXTO"])
        if sim >= LIMIAR_SIMILARIDADE:
            encontrado = True
            break  # Caso encontre um match aceitável, encerra a busca para este registro
    
    resultados.append({
        'NOME DO ESTABELECIMENTO': linha_consulta['NOME DO ESTABELECIMENTO'],
        'LOGRADOURO ORIGINAL': linha_consulta['LOGRADOURO'],
        'LOGRADOURO PADRONIZADO': linha_consulta['LOGRADOURO-TEXTO'],
        'NUMERO': linha_consulta['NUMERO'],
        'BAIRRO': linha_consulta['BAIRRO'],
        'CEP': linha_consulta['CEP'],
        'ENCONTRADO': 'Encontrado' if encontrado else 'Não Encontrado'
    })

# =============================================================================
# 4. SALVAR OS RESULTADOS
# =============================================================================

tabela_resultado = pd.DataFrame(resultados)
td.save_data(tabela_resultado, 'Suplementos Aracaju com Endereço')

print('Comparação concluída. O resultado foi salvo em Resultados/CSV/')
