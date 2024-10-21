# import modules and functions
import centralized_imports

# Set the locale once, globally
centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')

# Giving Path a chance
centralized_imports.Path.cwd()
centralized_imports.Path.home()

# Set environment variable using Path
centralized_imports.os.environ['FONTCONFIG_PATH'] = (
    str(centralized_imports.Path(r'C:/Users/ridim/anaconda3/Library/etc/fonts')))

# Define the base directory for the project
BASE_DIR = centralized_imports.Path(__file__).resolve().parent.parent

# Paths relative to the base directory
TEMPLATE_DIR = BASE_DIR / 'MODULOS_TERCIARIOS'
OUTPUT_DIR = BASE_DIR / 'RELATORIOS'
template_path = TEMPLATE_DIR / 'report_template.html'
output_path = OUTPUT_DIR / f"{centralized_imports.datetime.datetime.now().strftime('%Y-%m')}_relatorio_mensal.pdf"


# IMAGE FILEPATHS
# Valores mensais
image_tab_valores_mensais_investimentos = OUTPUT_DIR / 'tab_valores_mensais_investimentos.png'
image_graf_mercados_pie_chart = OUTPUT_DIR / 'graf_mercados_pie_chart.png'
image_graf_modalidades_pie_chart = OUTPUT_DIR / 'graf_modalidades_pie_chart.png'

# Movimentacoes mensais
image_tab_movimentacoes_mensais_investimentos = OUTPUT_DIR / 'tab_movimentacoes_mensais_investimentos.png'

# Rentabilidade e representatividade
image_tab_rent_rep_investimentos = OUTPUT_DIR / 'tab_rent_rep_investimentos.png'
image_graf_rent_rep_investimentos = OUTPUT_DIR / 'graf_rent_rep_investimentos.png'
image_graf_rent_rep_mercados = OUTPUT_DIR / 'graf_rent_rep_mercados.png'
image_graf_rent_rep_modalidades = OUTPUT_DIR / 'graf_rent_rep_modalidades.png'
image_graf_rent_carteira = OUTPUT_DIR / 'graf_rent_carteira.png'

# Variacoes patrimoniais
image_tab_variacao_patrimonial_investimentos = OUTPUT_DIR / 'tab_variacao_patrimonial_investimentos.png'
image_graf_variacao_patrimonial_acumulada = OUTPUT_DIR / 'graf_variacao_patrimonial_acumulada.png'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def gerar_relatorio_mensal(parametros_funcoes):
    try:
        print("&" * 90)
        print("THIS IS THE gerar_relatorio_mensal FUNCTION.")

        # Set the locale for Brazilian currency
        centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')

        # Extract relevant parameters from the function arguments
        filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")
        filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
        filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
        filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
        filepath_variacoes_patrimoniais_anuais = parametros_funcoes.get("filepath_variacoes_patrimoniais_anuais")
        filepath_variacoes_patrimoniais_mensais = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")
        month_bruto_key = parametros_funcoes.get("month_bruto_key")
        month_interest = parametros_funcoes.get("month_interest")
        month_liquido_key = parametros_funcoes.get("month_liquido_key")
        month_entrada_key = parametros_funcoes.get("month_entrada_key")
        month_saida_key = parametros_funcoes.get("month_saida_key")
        month_year_label = parametros_funcoes.get("month_year_label")
        year_interest = str(parametros_funcoes.get("year_interest"))
        year_month_interest = parametros_funcoes.get("year_month_interest")
        year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
        year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
        year_month_interest_end_str = str(year_month_interest_end)

        # Report date
        print("year_month_interest_end = ", year_month_interest_end)
        print("year_interest = ", year_interest)
        print("month_interest = ", month_interest)
        report_date = f"{year_month_interest_end.day} de {month_interest.lower()} de {year_interest}"
        print("report_date = ", report_date)

        # Load files with error handling
        try:
            dados_financeiros_historicos = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                    filepath_dados_financeiros_historicos))
            variacoes_patrimoniais_mensais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_variacoes_patrimoniais_mensais))
            variacoes_patrimoniais_anuais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                    filepath_variacoes_patrimoniais_anuais))
            valores_mensais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))
            movimentacoes_mensais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))
            rentabilidade_representatividade = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_rentabilidade_representatividade))
        except FileNotFoundError as e:
            print(f"Error loading files: {e}")
            return

        # Print loaded files for checking
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "dados_financeiros_historicos",dados_financeiros_historicos)
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "variacoes_patrimoniais_mensais", variacoes_patrimoniais_mensais)
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "variacoes_patrimoniais_anuais", variacoes_patrimoniais_anuais)
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "valores_mensais", valores_mensais)
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "movimentacoes_mensais", movimentacoes_mensais)
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "rentabilidade_representatividade", rentabilidade_representatividade)

        def safe_extract(key, dictionary, sub_key):
            try:
                return centralized_imports.locale.currency(float(dictionary[key][sub_key]), grouping=True, symbol=True)
            except KeyError:
                print(f"KeyError: {key} or {sub_key} not found. Returning R$ 0,00.")
                return centralized_imports.locale.currency(0.0, grouping=True, symbol=True)

        def safe_extract_percent(key, dictionary, sub_key):
            try:
                value = float(dictionary[key][sub_key]) * 100
                return f"{value:.2f}%"
            except KeyError:
                print(f"KeyError: {key} or {sub_key} not found. Returning 0.00%.")
                return 0.0

        # VALORES POR MERCADO
        print()
        print("EXTRAINDO VALORES POR MERCADO")
        mercados_list = centralized_imports.investimentos_btg.mercados_list
        investimentos_por_mercado = {}
        for mercado in mercados_list:
            investimentos_por_mercado[mercado] = safe_extract(mercado, valores_mensais, month_bruto_key)
        # Print investimentos_por_mercado
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "investimentos_por_mercado",investimentos_por_mercado)

        # VALORES POR MODALIDADE
        print()
        print("EXTRAINDO VALORES POR MODALIDADE")
        modalidades_list = centralized_imports.investimentos_btg.modalidades_list
        investimentos_por_modalidade = {}
        for modalidade in modalidades_list:
            investimentos_por_modalidade[modalidade] = safe_extract(modalidade, valores_mensais, month_bruto_key)
        # Print investimentos_por_modalidade
        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "investimentos_por_modalidade", investimentos_por_modalidade)

        # VALORES PATRIMONIO
        print()
        print("EXTRAINDO VALORES PATRIMONIO")
        patrimonio_total_bruto = safe_extract("TOTAL", valores_mensais, month_bruto_key)
        patrimonio_total_liquido = safe_extract("TOTAL", valores_mensais, month_liquido_key)

        print()
        print("VALORES PATRIMONIO")
        print("patrimonio_total_bruto = ", patrimonio_total_bruto)
        print("patrimonio_total_liquido = ", patrimonio_total_liquido)

        # MOVIMENTACOES POR MERCADO
        # --------------------------------
        # Entrada
        print()
        print("EXTRAINDO MOVIMENTACOES ENTRADA POR MERCADO")
        movimentacoes_entrada_renda_fixa = (
            safe_extract("RENDA FIXA", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_renda_variavel = (
            safe_extract("RENDA VARIAVEL", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_coe = (
            safe_extract("COE", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_fi = (
            safe_extract("FUNDOS DE INVESTIMENTO", movimentacoes_mensais, month_entrada_key))

        print()
        print("MOVIMENTACOES ENTRADA POR MERCADO")
        print("movimentacoes_entrada_renda_fixa = ", movimentacoes_entrada_renda_fixa)
        print("movimentacoes_entrada_renda_variavel = ", movimentacoes_entrada_renda_variavel)
        print("movimentacoes_entrada_coe = ", movimentacoes_entrada_coe)
        print("movimentacoes_entrada_fi = ", movimentacoes_entrada_fi)
        
        # --------------------------------
        # Saida
        print()
        print("EXTRAINDO MOVIMENTACOES SAIDA POR MERCADO")
        movimentacoes_saida_renda_fixa = (
            safe_extract("RENDA FIXA", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_renda_variavel = (
            safe_extract("RENDA VARIAVEL", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_coe = (
            safe_extract("COE", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_fi = (
            safe_extract("FUNDOS DE INVESTIMENTO", movimentacoes_mensais, month_saida_key))

        print()
        print("MOVIMENTACOES SAIDA POR MERCADO")
        print("movimentacoes_saida_renda_fixa = ", movimentacoes_saida_renda_fixa)
        print("movimentacoes_saida_renda_variavel = ", movimentacoes_saida_renda_variavel)
        print("movimentacoes_saida_coe = ", movimentacoes_saida_coe)
        print("movimentacoes_saida_fi = ", movimentacoes_saida_fi)
       
        # MOVIMENTACOES POR MODALIDADE
        # --------------------------------
        # Entrada
        print()
        print("EXTRAINDO MOVIMENTACOES ENTRADA POR MODALIDADE")
        movimentacoes_entrada_cdb = (
            safe_extract("CDB", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_cra = (
            safe_extract("CRA", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_deb = (
            safe_extract("DEBENTURES", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_lca = (
            safe_extract("LCA", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_lci = (
            safe_extract("LCI", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_acoes = (
            safe_extract("ACOES", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_fundos_imobiliarios = (
            safe_extract("FUNDOS IMOBILIARIOS", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_carteiras_recomendadas = (
            safe_extract("CARTEIRAS RECOMENDADAS", movimentacoes_mensais, month_entrada_key))

        print()
        print("MOVIMENTACOES POR MODALIDADE")
        print("movimentacoes_entrada_cdb = ", movimentacoes_entrada_cdb)
        print("movimentacoes_entrada_cra = ", movimentacoes_entrada_cra)
        print("movimentacoes_entrada_deb = ", movimentacoes_entrada_deb)
        print("movimentacoes_entrada_lca = ", movimentacoes_entrada_lca)
        print("movimentacoes_entrada_lci = ", movimentacoes_entrada_lci)
        print("movimentacoes_entrada_acoes = ", movimentacoes_entrada_acoes)
        print("movimentacoes_entrada_fundos_imobiliarios = ", movimentacoes_entrada_fundos_imobiliarios)
        print("movimentacoes_entrada_carteiras_recomendadas = ", movimentacoes_entrada_carteiras_recomendadas)

        # --------------------------------
        # Saida
        print()
        print("EXTRAINDO MOVIMENTACOES SAIDA POR MODALIDADE")
        movimentacoes_saida_cdb = (
            safe_extract("CDB", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_cra = (
            safe_extract("CRA", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_deb = (
            safe_extract("DEBENTURES", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_lca = (
            safe_extract("LCA", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_lci = (
            safe_extract("LCI", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_acoes = (
            safe_extract("ACOES", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_fundos_imobiliarios = (
            safe_extract("FUNDOS IMOBILIARIOS", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_carteiras_recomendadas = (
            safe_extract("CARTEIRAS RECOMENDADAS", movimentacoes_mensais, month_saida_key))

        print()
        print("MOVIMENTACOES POR MODALIDADE")
        print("movimentacoes_saida_cdb = ", movimentacoes_saida_cdb)
        print("movimentacoes_saida_cra = ", movimentacoes_saida_cra)
        print("movimentacoes_saida_deb = ", movimentacoes_saida_deb)
        print("movimentacoes_saida_lca = ", movimentacoes_saida_lca)
        print("movimentacoes_saida_lci = ", movimentacoes_saida_lci)
        print("movimentacoes_saida_acoes = ", movimentacoes_saida_acoes)
        print("movimentacoes_saida_fundos_imobiliarios = ", movimentacoes_saida_fundos_imobiliarios)
        print("movimentacoes_saida_carteiras_recomendadas = ", movimentacoes_saida_carteiras_recomendadas)

        # --------------------------------
        # Saida
        print()
        print("EXTRAINDO MOVIMENTACAO TOTAL")
        movimentacao_total_entrada = (
            safe_extract("TOTAL", movimentacoes_mensais,month_entrada_key))
        movimentacao_total_saida = (
            safe_extract("TOTAL", movimentacoes_mensais, month_saida_key))

        print()
        print("MOVIMENTACAO TOTAL")
        print("movimentacao_total_entrada = ", movimentacao_total_entrada)
        print("movimentacao_total_saida = ", movimentacao_total_entrada)

        # DADOS FINANCEIROS HISTORICOS
        # --------------------------------
        print()
        print("EXTRAINDO DADOS FINANCEIROS HISTORICOS")
        patrimonio_bruto_medio = (
            safe_extract("PATRIMONIO BRUTO MEDIO", dados_financeiros_historicos, year_month_interest_end_str))
        patrimonio_liquido_medio = (
            safe_extract("PATRIMONIO LIQUIDO MEDIO", dados_financeiros_historicos, year_month_interest_end_str))

        print()
        print("DADOS FINANCEIROS HISTORICOS")
        print("patrimonio_bruto_medio = ", patrimonio_bruto_medio)
        print("patrimonio_liquido_medio = ", patrimonio_liquido_medio)
        # check_patrimonio_bruto_medio = dados_financeiros_historicos[year_month_interest_end_str]["PATRIMONIO BRUTO MEDIO"]
        # check_patrimonio_liquido_medio = dados_financeiros_historicos[year_month_interest_end_str]["PATRIMONIO LIQUIDO MEDIO"]
        print("Checking dados_financeiros_historicos:")
        print("year_month_interest_end type:", type(year_month_interest_end))
        print("year_month_interest_end_str type:", type(year_month_interest_end_str))
        # print("check_patrimonio_bruto_medio = ", check_patrimonio_bruto_medio)
        # print("check_patrimonio_liquido_medio = ", check_patrimonio_liquido_medio)

        # RENTABILIDADE
        # --------------------------------
        # Rentabilidade mercados
        rentabilidade_renda_fixa = safe_extract_percent("RENDA FIXA", rentabilidade_representatividade,
                                                        "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_renda_variavel = safe_extract_percent("RENDA VARIAVEL", rentabilidade_representatividade,
                                                        "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_fi = safe_extract_percent("FUNDOS DE INVESTIMENTO", rentabilidade_representatividade,
                                                            "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_coe = safe_extract_percent("COE", rentabilidade_representatividade,
                                                                 "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_carteira = safe_extract_percent("TOTAL", rentabilidade_representatividade,
                                                 "RENTABILIDADE ANUAL MEDIA")

        print()
        print("RENTABILIDADE POR MERCADO")
        print("rentabilidade_renda_fixa = ", rentabilidade_renda_fixa)
        print("rentabilidade_renda_variavel = ", rentabilidade_renda_variavel)
        print("rentabilidade_coe = ", rentabilidade_coe)
        print("rentabilidade_fi = ", rentabilidade_fi)
        print("rentabilidade_carteira = ", rentabilidade_carteira)
        
        # Representatividade
        representatividade_renda_fixa = safe_extract_percent("RENDA FIXA", rentabilidade_representatividade,
                                                        "REPRESENTATIVIDADE")

        representatividade_renda_variavel = safe_extract_percent("RENDA VARIAVEL", rentabilidade_representatividade,
                                                            "REPRESENTATIVIDADE")
        representatividade_fi = safe_extract_percent("FUNDOS DE INVESTIMENTO",
                                                                 rentabilidade_representatividade,
                                                                 "REPRESENTATIVIDADE")
        representatividade_coe = safe_extract_percent("COE", rentabilidade_representatividade,
                                                 "REPRESENTATIVIDADE")

        print()
        print("REPRESENTAVIDADE POR MERCADO")
        print("representatividade_renda_fixa = ", representatividade_renda_fixa)
        print("representatividade_renda_variavel = ", representatividade_renda_variavel)
        print("representatividade_coe = ", representatividade_coe)
        print("representatividade_fi = ", representatividade_fi)
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # VARIACAO PATRIMONIAL POR MERCADO
        variacao_patrimonial_renda_fixa = safe_extract("RENDA FIXA", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_renda_variavel = safe_extract("RENDA VARIAVEL", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_coe = safe_extract("COE", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_fi = safe_extract("FUNDOS DE INVESTIMENTO", variacoes_patrimoniais_mensais, month_interest)

        print()
        print("VARIACAO PATRIMONIAL POR MERCADO")
        print("variacao_patrimonial_renda_fixa = ", variacao_patrimonial_renda_fixa)
        print("variacao_patrimonial_renda_variavel = ", variacao_patrimonial_renda_variavel)
        print("variacao_patrimonial_coe = ", variacao_patrimonial_coe)
        print("variacao_patrimonial_fi = ", variacao_patrimonial_fi)
        
        # VARIACAO PATRIMONIAL POR MODALIDADE
        variacao_patrimonial_cdb = safe_extract("CDB", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_cra = safe_extract("CRA", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_deb = safe_extract("DEBENTURES", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_lca = safe_extract("LCA", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_lci = safe_extract("LCI", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_acoes = safe_extract("ACOES", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_fundos_imobiliarios = safe_extract("FUNDOS IMOBILIARIOS", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_carteiras_recomendadas = safe_extract("CARTEIRAS RECOMENDADAS", variacoes_patrimoniais_mensais, month_interest)

        print()
        print("VARIACAO PATRIMONIAL POR MODALIDADE")
        print("variacao_patrimonial_cdb = ", variacao_patrimonial_cdb)
        print("variacao_patrimonial_cra = ", variacao_patrimonial_cra)
        print("variacao_patrimonial_deb = ", variacao_patrimonial_deb)
        print("variacao_patrimonial_lca = ", variacao_patrimonial_lca)
        print("variacao_patrimonial_lci = ", variacao_patrimonial_lci)
        print("variacao_patrimonial_acoes = ", variacao_patrimonial_acoes)
        print("variacao_patrimonial_fundos_imobiliarios = ", variacao_patrimonial_fundos_imobiliarios)
        print("variacao_patrimonial_carteiras_recomendadas = ", variacao_patrimonial_carteiras_recomendadas)
        
        # VARIACAO PATRIMONIAL TOTAL
        variacao_patrimonial_carteira_mensal = safe_extract("TOTAL", variacoes_patrimoniais_mensais, month_interest)
        variacao_patrimonial_carteira_acumulada = (
            safe_extract("TOTAL", variacoes_patrimoniais_anuais, "TOTAL INTERESSE"))

        print()
        print("VARIACAO PATRIMONIAL TOTAL")
        print("variacao_patrimonial_carteira_mensal = ", variacao_patrimonial_carteira_mensal)
        print("variacao_patrimonial_carteira_acumulada = ", variacao_patrimonial_carteira_acumulada)
        
        # Open the template file with error handling
        try:
            template = template_path.read_text(encoding='utf-8')
            print(f"Loaded HTML template from: {template_path}")
        except FileNotFoundError:
            print(f"Template file not found: {template_path}")
            return

        # Prepare data for template rendering
        data_valores_mensais = {
            "investimentos_renda_fixa": investimentos_renda_fixa,
            "investimentos_renda_variavel": investimentos_renda_variavel,
            "investimentos_coe": investimentos_coe,
            "investimentos_fi": investimentos_fi,
            "investimentos_cdb": investimentos_cdb,
            "investimentos_cra": investimentos_cra,
            "investimentos_deb": investimentos_deb,
            "investimentos_lca": investimentos_lca,
            "investimentos_lci": investimentos_lci,
            "investimentos_acoes": investimentos_acoes,
            "investimentos_fundos_imobiliarios": investimentos_fundos_imobiliarios,
            "investimentos_carteiras_recomendadas": investimentos_carteiras_recomendadas
        }

        data_patrimonio = {
            "patrimonio_total_bruto": patrimonio_total_bruto,
            "patrimonio_total_liquido": patrimonio_total_liquido,
        }

        data_movimentacoes_mensais = {
            "movimentacao_total_entrada": movimentacao_total_entrada,
            "movimentacao_total_saida": movimentacao_total_saida,
            "movimentacoes_entrada_fi": movimentacoes_entrada_fi,
            "movimentacoes_entrada_coeE": movimentacoes_entrada_coe,
            "movimentacoes_entrada_acoes": movimentacoes_entrada_acoes,
            "movimentacoes_entrada_carteiras_recomendadas": movimentacoes_entrada_carteiras_recomendadas,
            "movimentacoes_entrada_cra": movimentacoes_entrada_cra,
            "movimentacoes_entrada_deb": movimentacoes_entrada_deb,
            "movimentacoes_entrada_fundos_imobiliarios": movimentacoes_entrada_fundos_imobiliarios,
            "movimentacoes_entrada_lca": movimentacoes_entrada_lca,
            "movimentacoes_entrada_lci": movimentacoes_entrada_lci,
            "movimentacoes_entrada_renda_fixa": movimentacoes_entrada_renda_fixa,
            "movimentacoes_entrada_renda_variavel": movimentacoes_entrada_renda_variavel,
            "movimentacoes_saida_FI": movimentacoes_saida_fi,
            "movimentacoes_saida_COE": movimentacoes_saida_coe,
            "movimentacoes_saida_acoes": movimentacoes_saida_acoes,
            "movimentacoes_saida_carteiras_recomendadas": movimentacoes_saida_carteiras_recomendadas,
            "movimentacoes_saida_cra": movimentacoes_saida_cra,
            "movimentacoes_saida_deb": movimentacoes_saida_deb,
            "movimentacoes_saida_fundos_imobiliarios": movimentacoes_saida_fundos_imobiliarios,
            "movimentacoes_saida_lca": movimentacoes_saida_lca,
            "movimentacoes_saida_lci": movimentacoes_saida_lci,
            "movimentacoes_saida_renda_fixa": movimentacoes_saida_renda_fixa,
            "movimentacoes_saida_renda_variavel": movimentacoes_saida_renda_variavel,
        }
        
        data_rentabilidade_representavidade = {
            "rentabilidade_carteira": rentabilidade_carteira,
            "rentabilidade_coe": rentabilidade_coe,
            "rentabilidade_fi": rentabilidade_fi,
            "rentabilidade_renda_fixa": rentabilidade_renda_fixa,
            "rentabilidade_renda_variavel": rentabilidade_renda_variavel
        }
        
        data_variacoes_patrimoniais = {
            "variacao_patrimonial_renda_fixa": variacao_patrimonial_renda_fixa,
            "variacao_patrimonial_renda_variavel": variacao_patrimonial_renda_variavel,
            "variacao_patrimonial_fi": variacao_patrimonial_fi,
            "variacao_patrimonial_coe": variacao_patrimonial_coe,
            "variacao_patrimonial_acoes": variacao_patrimonial_acoes,
            "variacao_patrimonial_carteiras_recomendadas": variacao_patrimonial_carteiras_recomendadas,
            "variacao_patrimonial_cdb": variacao_patrimonial_cdb,
            "variacao_patrimonial_cra": variacao_patrimonial_cra,
            "variacao_patrimonial_deb": variacao_patrimonial_deb,
            "variacao_patrimonial_fundos_imobiliarios": variacao_patrimonial_fundos_imobiliarios,
            "variacao_patrimonial_lca": variacao_patrimonial_lca,
            "variacao_patrimonial_lci": variacao_patrimonial_lci,
        }

        data_financial_history = {
            "patrimonio_bruto_medio": patrimonio_bruto_medio,
            "patrimonio_liquido_medio": patrimonio_liquido_medio,
        }

        data_miscellanea = {
            "report_date": report_date,
            "year_month_interest_end": year_month_interest_end
        }

        report_data = centralized_imports.ChainMap(
            data_valores_mensais,
            data_patrimonio,
            data_movimentacoes_mensais,
            data_rentabilidade_representavidade,
            data_financial_history,
            data_miscellanea
        )

        centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
            "data", report_data)

        template_content = template_path.read_text(encoding='utf-8')
        rendered_content = centralized_imports.Template(template_content).render(report_data)

        # Generate PDF
        try:
            pdf_filename = f"{year_month_interest_end}_relatorio_mensal.pdf"
            output_path = OUTPUT_DIR / pdf_filename
            centralized_imports.HTML(string=rendered_content).write_pdf(output_path)
            print(f"PDF report generated: {output_path}")
        except Exception as e:
            print(f"Error generating PDF: {e}")

    except Exception as e:
        print(f"An error occurred in gerar_relatorio_mensal: {e}")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




