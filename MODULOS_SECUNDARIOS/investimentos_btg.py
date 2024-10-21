# MEUS INVESTIMENTOS BTG
# ===============================================================================
import centralized_imports

# CHAPTER 1: GENERAL LISTS
# ===============================================================================
floats_list = ['ENTRADA', 'SAIDA', 'BRUTO', 'LIQUIDO']

table_type_list = [
    "TABELA VALORES MENSAIS INVESTIMENTOS",
    "TABELA MOVIMENTACOES MENSAIS INVESTIMENTOS",
    "TABELA RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS",
    "TABELA VARIACOES PATRIMONIAIS INVESTIMENTOS"
                    ]

plot_type_list = [
    "PIZZA VALORES MENSAIS MERCADOS",
    "PIZZA VALORES MENSAIS MODALIDADES",
    "BARRAS RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS",
    "BARRAS RENTABILIDADE REPRESENTATIVIDADE MERCADOS",
    "BARRAS RENTABILIDADE REPRESENTATIVIDADE MODALIDADES",
    "VARIACAO PATRIMONIAL ACUMULADA",
    "RENTABILIDADE MENSAL CARTEIRA"
                    ]

# CHAPTER 2: MONTHS AND YEARS LISTS
# ===============================================================================
months_list = [
    "JANEIRO", "FEVEREIRO", "MARCO", "ABRIL",
    "MAIO", "JUNHO", "JULHO", "AGOSTO",
    "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]

# Dictionary to map month names to month numbers
month_name_mapping = {
    "JANEIRO": 1, "FEVEREIRO": 2, "MARCO": 3, "ABRIL": 4,
    "MAIO": 5, "JUNHO": 6, "JULHO": 7, "AGOSTO": 8,
    "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12
}

month_number_mapping = {1: "JANEIRO", 2: "FEVEREIRO", 3: "MARCO", 4: "ABRIL",
                        5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
                        9: "SETEMBRO",10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"}

years_list = [
    "2020", "2021", "2022", "2023",
    "2024", "2025"
]


# CHAPTER 3: CREATE INVESTMENTS TYPES LISTS
# ===============================================================================

# SECT. 2.1: MERCADOS LIST
# -------------------------------------------------------------------------------
mercados_list = ['RENDA FIXA',
                 'RENDA VARIAVEL',
                 'COE',
                 'FUNDOS DE INVESTIMENTO',
                 'OUTROS'
                 ]


# SECT. 2.2: MODALIDADES LIST
# -------------------------------------------------------------------------------

# Create the MODALIDADES RENDA FIXA list
modalidadesRF = ["CDB", "CRA", "DEBENTURES", "LCA", "LCI"]

# Create the MODALIDADES RENDA VARIAVEL list
modalidadesRV = ["ACOES", "FUNDOS IMOBILIARIOS", "CARTEIRAS RECOMENDADAS"]

# Create the MODALIDADES FUNDOS DE INVESTIMENTO list
modalidadesFI = ["FUNDOS DE INVESTIMENTO"]

# Create the COE list
modalidadesCOE = ["COE"]

# Create the OUTROS list
modalidadesOUTROS = ["BENEFICIOS CARTAO"]


# Complete Modalidades List
modalidades_list = (modalidadesRF +
                    modalidadesRV +
                    modalidadesFI +
                    modalidadesCOE +
                    modalidadesOUTROS
                    )

# Create tax exempt MODALIDADES list
tax_exempt_modalidades = ['CRA', 'LCA', 'LCI', 'DEBENTURES',
                          'ACOES', 'FUNDOS IMOBILIARIOS', 'CARTEIRAS RECOMENDADAS',
                          'BENEFICIOS CARTAO']

# This is a special purpose list related to TOTALS summations. Only investments are left.
skip_investment_list = mercados_list + modalidades_list


# CHAPTER 4: CREATE INVESTMENTS LISTS
# ===============================================================================

# SECT. 4.1: RENDA FIXA
# -------------------------------------------------------------------------------

# Create the investimentosCDB list
investimentosCDB = ["BTG PACTUAL 150% CDIE",
                    "BTG PACTUAL 104% CDIE",
                    "BTG PACTUAL 104,25% CDIE",
                    "21-12-13 / BANCO SEGURO",
                    "22-03-21 / BANCO MASTER (CDB122JY2EY)",
                    "22-03-30 / BANCO MASTER (CDB122M9N36)",
                    "22-04-14 / BANCO MASTER (CDB2224QT2I)",
                    "21-09-10 / BANCO ORIGINAL (CDB321IZUFY)",
                    "23-03-30 / BANCO DIGIMAIS (CDB123TMUHH)",
                    "22-11-22 / BANCO ARBI (CDB422GU5YV)"]

# Create the investimentosCRA list
investimentosCRA = ["21-03-30 / TEREOS ACUCAR E ENERGIA",
                    "21-03-30 / VERT CIA SECURITIZADORA"]

# Create the investimentosLCA list
investimentosLCA = ["BTG 106% CDIE",
                    "BTG 103% CDIE",
                    "22-11-22 / COOPERATIVA (LCA-22K01262726)",
                    "22-11-01 / COOPERATIVA (LCA-22K00018947)",
                    "23-03-30 / BTG (LCA-23C02705202)",
                    "23-03-30 / BANCO VOTORANTIM (LCA-23C02714265)",
                    "23-10-05 / BTG (LCA-23J01085256)"]

# Create the investimentosLCI list
investimentosLCI = ["22-05-13 / LCI BANCO ORIGINAL"]

# Create the investimentosDebentures list
investimentosDebentures = ["20-06-03 / LIGHT - LIGHA5 (IPCA + 4,05%)",
                           "2020-11-26 / LIGHT - LIGHA5 (IPCA + 3,80%)",
                           "21-02-03 / RUMO S.A. - RUMOA5",
                           "21-06-15 / LIGHT - LIGHD2 (IPCA + 4,75%)"]


# SECT. 3.2: RENDA VARIAVEL
# -------------------------------------------------------------------------------

# Create the investimentosAcoes list
investimentosAcoes = ["21-05-14 / G2DI33 - G2D INVEST DR3",
                     "21-08-31 / BHIA3 - VIA VAREJO"]

# Create the investimentosCarteirasRecomendadas list
investimentosCarteirasRecomendadas = ["21-08-09 / 10SIM"]

# Create the investimentosFundosImobiliarios list
investimentosFundosImobiliarios = ["21-03-31 / BDIF11 - FIC INFR BTGCI ER",
                                   "24-03-26 / BDIF15 - FIC INFR BTGREC",
                                   "24-04-26 / BPML15 - FII BTG SHOPREC"]


# SECT. 3.3: COE
# -------------------------------------------------------------------------------

# Create the investimentosCOE list
investimentosCOE = ["CREDIT SUISSE",
                    "22-03-30 / BNP PARIBAS (PB0122C4OWI)",
                    "20-07-20 / BTG (BT0520G34Q7)",
                    "21-06-28 / BTG (BT0821F3NXE)",
                    "21-07-30 / BTG (BT0221G3QRZ)",
                   "20-09-16 / BTG (BT1120I36XY)",
                   "20-09-01 / BTG (BT5620I36B4)",
                   "21-11-16 / BTG (BT1821K44DS)",
                   "21-10-29 / CREDIT SUISSE (B80121J42LX)",
                   "22-03-31 / GLD UP (BT0122C4PC1)",
                   "22-04-28 / GOLDMAN SACHS (GS0122D4WV8)"]


# SECT. 3.4: FUNDOS DE INVESTIMENTO
# -------------------------------------------------------------------------------
# Create the investimentosFI list
investimentosFI = ["Tesouro Simples RF",
                   "BTG DIGIT FI CAMBIAL",
                   "BTG S&P 500 BRL FIM",
                   "ACS OCCAM EQ FIC",
                   "ACS JGP STRATEGY FIC FIM",
                   "ACS GENOA FIC FIM","DAHLIA FIC FIM PRO",
                   "MOAT EQUITY CAP PRO",
                   "21-02-05 / ARX ELBRUS DEB INCENTIVADAS FIM CP",
                   "22-10-24 / SUL AMERICA EXCELLENCE FIRP",
                   "23-03-02 / BTG CDB PLUS FI"]

# SECT. 4.1: OUTROS
# -------------------------------------------------------------------------------
# Create the investimentosBeneficiosCartao list
investimentosBeneficiosCartao = ["RESTITUICAO IOF",
                                 "PONTOS LIVELO"]


# SECT. 3.5: CAMINHOS PARA OS ARQUIVOS CONTENDO ESTES INVESTIMENTOS
# -------------------------------------------------------------------------------

# Define individual file paths
filepath_config_json = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\config\config.json"))
filepath_dados_financeiros_historicos = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\dados_financeiros_historicos.pickle"))
filepath_movimentacoes_anuais = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_anuais.pickle"))
filepath_movimentacoes_mensais_2020 = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_2020.pickle"))
filepath_movimentacoes_mensais_2021 = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_2021.pickle"))
filepath_movimentacoes_mensais_padrao = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_padrao.pickle"))
filepath_rentabilidade_mercados_modalidades = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\rentabilidade_mercados_modalidades.pickle"))
filepath_rentabilidade_representatividade = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\rentabilidade_representatividade.pickle"))
filepath_valores_mensais_2020 = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2020.pickle"))
filepath_valores_mensais_2021 = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2021.pickle"))
filepath_valores_mensais_padrao = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_padrao.pickle"))
filepath_variacoes_patrimoniais_anuais = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_anuais.pickle"))
filepath_variacoes_patrimoniais_mensais_2020 = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_mensais_2020.pickle"))
filepath_variacoes_patrimoniais_mensais_2021 = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_mensais_2021.pickle"))

# Define the dictionary using the variables
filepaths_dictionary_Path = {
    "filepath_config_json": filepath_config_json,
    "filepath_dados_financeiros_historicos": filepath_dados_financeiros_historicos,
    "filepath_movimentacoes_anuais": filepath_movimentacoes_anuais,
    "filepath_movimentacoes_mensais_2020": filepath_movimentacoes_mensais_2020,
    "filepath_movimentacoes_mensais_2021": filepath_movimentacoes_mensais_2021,
    "filepath_movimentacoes_mensais_padrao": filepath_movimentacoes_mensais_padrao,
    "filepath_rentabilidade_mercados_modalidades": filepath_rentabilidade_mercados_modalidades,
    "filepath_rentabilidade_representatividade": filepath_rentabilidade_representatividade,
    "filepath_valores_mensais_2020": filepath_valores_mensais_2020,
    "filepath_valores_mensais_2021": filepath_valores_mensais_2021,
    "filepath_valores_mensais_padrao": filepath_valores_mensais_padrao,
    "filepath_variacoes_patrimoniais_anuais": filepath_variacoes_patrimoniais_anuais,
    "filepath_variacoes_patrimoniais_mensais_2020": filepath_variacoes_patrimoniais_mensais_2020,
    "filepath_variacoes_patrimoniais_mensais_2021": filepath_variacoes_patrimoniais_mensais_2021
}


filepaths_dictionary = {
    "filepath_base_dados_investimentos": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\base_dados_investimentos.pickle",
    "filepath_config_json": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\config\config.json",
    "filepath_dados_financeiros_historicos": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\dados_financeiros_historicos.pickle",
    "filepath_movimentacoes_anuais": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_anuais.pickle",
    "filepath_movimentacoes_mensais_2020": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_2020.pickle",
    "filepath_movimentacoes_mensais_2021": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_2021.pickle",
    "filepath_movimentacoes_mensais_padrao": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_padrao.pickle",
    "filepath_rentabilidade_mercados_modalidades": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\rentabilidade_mercados_modalidades.pickle",
    "filepath_rentabilidade_representatividade": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\rentabilidade_representatividade.pickle",
    "filepath_valores_mensais_2020": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2020.pickle",
    "filepath_valores_mensais_2021": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2021.pickle",
    "filepath_valores_mensais_padrao": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_padrao.pickle",
    "filepath_movimentacoes_mensais_padrao": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_padrao.pickle",
    "filepath_variacoes_patrimoniais_anuais": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_anuais.pickle",
    "filepath_variacoes_patrimoniais_mensais_2020": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_mensais_2020.pickle",
    "filepath_variacoes_patrimoniais_mensais_2021": r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_mensais_2021.pickle"

}

filepaths_list = [
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\base_dados_investimentos.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\dados_financeiros_historicos.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_anuais.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_2020.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_2021.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_padrao.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\rentabilidade_mercados_modalidades.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\rentabilidade_representatividade.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2020.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2021.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_padrao.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_anuais.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_mensais_2020.pickle",
    r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\variacoes_patrimoniais_mensais_2021.pickle"
]


# CHAPTER 4: LISTAS DE CABECALHOS
# ===============================================================================
# Sec. 4.1 - CABECALHO VALORES MENSAIS
# -------------------------------------------------------------------------------
cabecalho_valores_mensais = [
        "DATA COMPRA", "DATA VENCIMENTO",
        "JANEIRO BRUTO", "JANEIRO LIQUIDO",
        "FEVEREIRO BRUTO", "FEVEREIRO LIQUIDO",
        "MARCO BRUTO", "MARCO LIQUIDO",
        "ABRIL BRUTO", "ABRIL LIQUIDO",
        "MAIO BRUTO", "MAIO LIQUIDO",
        "JUNHO BRUTO", "JUNHO LIQUIDO",
        "JULHO BRUTO", "JULHO LIQUIDO",
        "AGOSTO BRUTO", "AGOSTO LIQUIDO",
        "SETEMBRO BRUTO", "SETEMBRO LIQUIDO",
        "OUTUBRO BRUTO", "OUTUBRO LIQUIDO",
        "NOVEMBRO BRUTO", "NOVEMBRO LIQUIDO",
        "DEZEMBRO BRUTO", "DEZEMBRO LIQUIDO",
        "CODIGO"]

# Sec. 4.2 - CABECALHO MOVIMENTACOES MENSAIS
# -------------------------------------------------------------------------------
cabecalho_movimentacoes_mensais = [
        "DATA COMPRA", "DATA VENCIMENTO",
        "JANEIRO ENTRADA", "JANEIRO SAIDA",
        "FEVEREIRO ENTRADA", "FEVEREIRO SAIDA",
        "MARCO ENTRADA", "MARCO SAIDA",
        "ABRIL ENTRADA", "ABRIL SAIDA",
        "MAIO ENTRADA", "MAIO SAIDA",
        "JUNHO ENTRADA", "JUNHO SAIDA",
        "JULHO ENTRADA", "JULHO SAIDA",
        "AGOSTO ENTRADA", "AGOSTO SAIDA",
        "SETEMBRO ENTRADA", "SETEMBRO SAIDA",
        "OUTUBRO ENTRADA", "OUTUBRO SAIDA",
        "NOVEMBRO ENTRADA", "NOVEMBRO SAIDA",
        "DEZEMBRO ENTRADA", "DEZEMBRO SAIDA",
        "CODIGO"]

# Sec. 4.3 - CABECALHO SALDOS ANUAIS RENTABILIDADE
# -------------------------------------------------------------------------------
cabecalho_saldos_anuais_rentabilidade = [
        "DATA COMPRA", "DATA VENCIMENTO", "CODIGO",
        "2020 ENTRADA", "2020 SAIDA",
        "2021 ENTRADA", "2021 SAIDA",
        "2022 ENTRADA", "2022 SAIDA",
        "2023 ENTRADA", "2023 SAIDA",
        "2024 ENTRADA", "2024 SAIDA"
        ]

# Sec. 4.4 - CABECALHO SALDOS ANUAIS RENTABILIDADE
# -------------------------------------------------------------------------------
mapa_cabecalhos = {
    "valores_mensais": cabecalho_valores_mensais,
    "movimentacoes_mensais": cabecalho_movimentacoes_mensais,
    "saldos_anuais_rentabilidade": cabecalho_saldos_anuais_rentabilidade
}


# CHAPTER 4: CREATE INVESTMENTS CLASS
# ===============================================================================
class InvestimentosBTG:
    data_structure = {
        'RENDA FIXA': {
            'CDB': investimentosCDB,
            'CRA': investimentosCRA,
            'DEBENTURES': investimentosDebentures,
            'LCA': investimentosLCA,
            'LCI': investimentosLCI
        },
        'RENDA VARIAVEL': {
            'ACOES': investimentosAcoes,
            'CARTEIRAS RECOMENDADAS': investimentosCarteirasRecomendadas,
            'FUNDOS IMOBILIARIOS': investimentosFundosImobiliarios
        },
        'FUNDOS DE INVESTIMENTO': {
            'FUNDOS DE INVESTIMENTO': investimentosFI
        },
        'COE': {
            'COE': investimentosCOE
        },
        'OUTROS': {
            'OUTROS': investimentosBeneficiosCartao
        }
    }

    def __init__(self):
        pass

    # ===========================================================================
    @staticmethod
    def all_investments_list():
        all_investments_list = []
        for investment_category in InvestimentosBTG.data_structure.values():
            for investment_type, investment_class in investment_category.items():
                if callable(investment_class):
                    all_investments_list.append(investment_class())
                else:
                    all_investments_list.extend(investment_class)
        return all_investments_list

    # ===========================================================================
    def iterate_investments(self):
        for category, subcategories in self.data_structure.items():
            print(f'Category: {category}')
            for subcategory, investments in subcategories.items():
                print(f'Subcategory: {subcategory}')
                for investment in investments:
                    print(investment)

    # ===========================================================================
    @staticmethod
    def get_selected_list(mercado, modalidade):
        # print("mercado = ", mercado)
        # print("modalidade = ", modalidade, end='\n\n')
        selected_list = []

        for category, subcategories in InvestimentosBTG.data_structure.items():
            if category == mercado:
                for subcategory, investments in subcategories.items():
                    if subcategory.lower() == modalidade.lower():
                        selected_list.extend(investments)
                        break
                if not selected_list:
                    print(f"Warning: No '{modalidade}' investments found in category '{mercado}'.")
                break

        return selected_list

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



