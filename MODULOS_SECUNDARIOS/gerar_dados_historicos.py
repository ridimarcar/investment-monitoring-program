import centralized_imports

def gerar_dados_historicos(parametros_funcoes):
    print("&" * 90)
    print("THIS IS THE gerar_dados_historicos FUNCTION.")

    # -----------------------------------------------------------
    # EXTRACT RELEVANT PARAMETERS
    filepaths_dict = centralized_imports.investimentos_btg.filepaths_dictionary
    filepath_dados_financeiros_historicos = (
        parametros_funcoes.get("filepath_dados_financeiros_historicos"))
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    filepath_variacoes_patrimoniais_anuais = (
        parametros_funcoes.get("filepath_variacoes_patrimoniais_anuais"))
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_bruto_key")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    print("filepath_dados_financeiros_historicos =", filepath_dados_financeiros_historicos)

    # -----------------------------------------------------------
    # LOAD FILES
    try:
        dados_financeiros_historicos = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_dados_financeiros_historicos)
    except FileNotFoundError:
        print("File not found. Creating a new dict.")
        dados_financeiros_historicos = {}
    except Exception as e:
        print(f"An error occurred: {e}")
        dados_financeiros_historicos = {}

    if not isinstance(dados_financeiros_historicos, dict):
        print("Invalid data. Initializing as an empty dictionary.")
        dados_financeiros_historicos = {}

    valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_valores_mensais)

    variacoes_patrimoniais_anuais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_variacoes_patrimoniais_anuais)

    rentabilidade_representatividade = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_rentabilidade_representatividade)

    # +++++++++++++++++++++++++++++++++++++++++++
    # Initialize lists to store the values for "PATRIMONIO BRUTO" and "PATRIMONIO LIQUIDO"
    patrimonio_bruto_values = []
    patrimonio_liquido_values = []

    # Iterate through the dictionary keys (dates)
    for key in dados_financeiros_historicos:
        # Convert the key (string) into a datetime object
        # key_date = centralized_imports.datetime.datetime.strptime(key, "%Y-%m-%d").date()
        # Only consider dates that are earlier than or equal to year_month_interest_end
        if key <= year_month_interest_end:
            # Get the 'PATRIMONIO BRUTO' and 'PATRIMONIO LIQUIDO' for this date and append to the lists
            patrimonio_bruto_values.append(dados_financeiros_historicos[key]["PATRIMONIO BRUTO"])
            patrimonio_liquido_values.append(dados_financeiros_historicos[key]["PATRIMONIO LIQUIDO"])

    # Calculate the averages
    print()
    print("patrimonio_bruto_values")
    print(patrimonio_bruto_values)
    print("len(patrimonio_bruto_values) = ", len(patrimonio_bruto_values))
    print()
    print("patrimonio_liquido_values")
    print(patrimonio_liquido_values)
    print("len(patrimonio_liquido_values) = ", len(patrimonio_liquido_values))
    patrimonio_bruto_medio = sum(patrimonio_bruto_values) / len(
        patrimonio_bruto_values) if patrimonio_bruto_values else 0
    patrimonio_liquido_medio = sum(patrimonio_liquido_values) / len(
        patrimonio_liquido_values) if patrimonio_liquido_values else 0

    # Calculate all-time profitability
    all_time_profitability = rentabilidade_historica_carteira(parametros_funcoes)
    print("all_time_profitability = ", all_time_profitability)
    print("rentabilidade_representatividade[TOTAL][RENTABILIDADE TOTAL]", rentabilidade_representatividade["TOTAL"]["RENTABILIDADE TOTAL"])

    # Get all-time gains
    variacao_patrimonial_acumulada = (
        variacoes_patrimoniais_anuais["TOTAL"]["TOTAL INTERESSE"])

    # Check parameters
    rentabilidade_mensal_carteira = rentabilidade_representatividade["TOTAL"]["RENTABILIDADE MENSAL MEDIA"]
    rentabilidade_anual_carteira = rentabilidade_representatividade["TOTAL"]["RENTABILIDADE ANUAL MEDIA"]

    # Update the dictionary
    if year_month_interest_end in dados_financeiros_historicos:
        # Valores do patrimonio
        dados_financeiros_historicos[year_month_interest_end]["PATRIMONIO BRUTO"] = (
            valores_mensais["TOTAL"][month_bruto_key])
        dados_financeiros_historicos[year_month_interest_end]["PATRIMONIO LIQUIDO"] = (
            valores_mensais["TOTAL"][month_liquido_key])
        dados_financeiros_historicos[year_month_interest_end]["PATRIMONIO BRUTO MEDIO"] = (
            patrimonio_bruto_medio)
        dados_financeiros_historicos[year_month_interest_end]["PATRIMONIO LIQUIDO MEDIO"] = (
            patrimonio_liquido_medio)
        # Valores de rentabilidade
        dados_financeiros_historicos[year_month_interest_end]["RENTABILIDADE TOTAL CARTEIRA"] = (
            rentabilidade_representatividade["TOTAL"]["RENTABILIDADE TOTAL"])
        dados_financeiros_historicos[year_month_interest_end]["RENTABILIDADE ANUAL CARTEIRA"] = (
            rentabilidade_representatividade["TOTAL"]["RENTABILIDADE ANUAL MEDIA"])
        dados_financeiros_historicos[year_month_interest_end]["RENTABILIDADE MENSAL CARTEIRA"] = (
            rentabilidade_representatividade["TOTAL"]["RENTABILIDADE MENSAL MEDIA"])
        # Variacoes patrimoniais
        dados_financeiros_historicos[year_month_interest_end]["VARIACAO PATRIMONIAL ACUMULADA"] = (
            variacao_patrimonial_acumulada)
    else:
        # If year_month_interest_end does not exist in the dictionary, create it
        dados_financeiros_historicos[year_month_interest_end] = {
            "PATRIMONIO BRUTO": valores_mensais["TOTAL"][month_bruto_key],
            "PATRIMONIO LIQUIDO": valores_mensais["TOTAL"][month_liquido_key],
            "PATRIMONIO BRUTO MEDIO": patrimonio_bruto_medio,
            "PATRIMONIO LIQUIDO MEDIO": patrimonio_liquido_medio,
            "RENTABILIDADE MENSAL CARTEIRA": rentabilidade_mensal_carteira,
            "RENTABILIDADE ANUAL CARTEIRA": rentabilidade_anual_carteira,
            "RENTABILIDADE TOTAL CARTEIRA": all_time_profitability,
            "VARIACAO PATRIMONIAL ACUMULADA": variacao_patrimonial_acumulada
        }

    # Print the results for debugging
    print(f"Averages up to {year_month_interest_end}:")
    print(f"  PATRIMONIO BRUTO MEDIO: {patrimonio_bruto_medio}")
    print(f"  PATRIMONIO LIQUIDO MEDIO: {patrimonio_liquido_medio}")
    # ++++++++++++++++++++++++++++++++++++++++++++

    # -----------------------------------------------------------
    # SAVE DICTIONARY TO PICKLE FILE
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_dados_financeiros_historicos, dados_financeiros_historicos
    )

    # DISPLAY PICKLE FILE
    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(
        filepath_dados_financeiros_historicos)

    # CREATE SCATTER PLOTS
    tipo_grafico = "VARIACAO PATRIMONIAL ACUMULADA"
    centralized_imports.gerar_graficos.criar_grafico_xy(tipo_grafico, parametros_funcoes)

    tipo_grafico = "VARIACAO PATRIMONIAL ACUMULADA"
    centralized_imports.gerar_graficos.criar_grafico_xy_pandas(tipo_grafico, parametros_funcoes)

    tipo_grafico = "RENTABILIDADE CARTEIRA"
    centralized_imports.gerar_graficos.criar_grafico_xy_pandas(tipo_grafico, parametros_funcoes)

    # tipo_grafico = "RENTABILIDADE CARTEIRA"
    # centralized_imports.gerar_graficos.criar_grafico_xy(tipo_grafico, parametros_funcoes)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def rentabilidade_historica_carteira(parametros_funcoes):

    # Set up parameters
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")

    # Load files
    try:
        movimentacoes_anuais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_movimentacoes_anuais)
        )
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        valores_mensais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_valores_mensais)
        )
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Calculate profitability
    total_key = "TOTAL"
    total_entrada_subkey = "TOTAL INTERESSE ENTRADA"
    total_saida_subkey = "TOTAL INTERESSE SAIDA"
    valor_atual_liquido = valores_mensais[total_key][month_liquido_key]
    print("movimentacoes_anuais[total_key][total_entrada_subkey]")
    print(movimentacoes_anuais[total_key][total_entrada_subkey])
    print("movimentacoes_anuais[total_key][total_saida_subkey]")
    print(movimentacoes_anuais[total_key][total_saida_subkey])
    movimentacao_historica_entrada = movimentacoes_anuais[total_key][total_entrada_subkey]
    movimentacao_historica_saida = movimentacoes_anuais[total_key][total_saida_subkey]
    diferenca_movimentacoes = movimentacao_historica_saida - movimentacao_historica_entrada

    all_time_profitability = (valor_atual_liquido - diferenca_movimentacoes) / movimentacao_historica_entrada

    return all_time_profitability


