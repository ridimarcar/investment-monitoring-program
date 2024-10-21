import centralized_imports

def dicionario_anos_interesse(parametros_funcoes):

    print()
    print("-" * 90)
    print("THIS IS THE dic_anos_interesse FUNCTION")

    year_interest = parametros_funcoes.get("year_interest")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_movimentacoes_mensais_atual = parametros_funcoes.get("filepath_movimentacoes_mensais")

    year_interest_str = str(year_interest)

    # Open the current file containing monthly values
    movimentacoes_mensais_atual = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais_atual))

    dic_anos_interesse = {}
    for investment, value in movimentacoes_mensais_atual.items():
        print(f"THIS IS INVESTMENT {investment}")
        # Extract the 'DATA COMPRA' field and convert it to a date
        data_compra = value.get("DATA COMPRA")
        # Check if 'DATA COMPRA' exists and is not None
        if data_compra:
            # Convert it to a date
            try:
                data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, "%Y-%m-%d")
                print(f"Data Compra: {data_compra_date}")
            except ValueError as e:
                print(f"Error parsing date for investment {investment}: {e}")
        else:
            print(f"'DATA COMPRA' not found or is None for investment {investment}")

        year_data_compra = data_compra_date.year
        anos_interesse = [year_interest]
        if year_data_compra < year_interest:
            for ano in range(year_data_compra, year_interest):
                anos_interesse.append(ano)
        else:
            print("No need to import extra files")

        dic_anos_interesse[investment] = anos_interesse

    return dic_anos_interesse

# ----------------------------------------------------------------------------
def somar_historico_variacoes_patrimoniais_mensais(parametros_funcoes):
    print("-" * 90)
    print("THIS IS THE somar_historico_variacoes_patrimoniais_mensais FUNCTION")

    filepath_variacoes_patrimoniais_anuais = parametros_funcoes.get("filepath_variacoes_patrimoniais_anuais")
    variacoes_patrimoniais_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_variacoes_patrimoniais_anuais))

    # Fetch relevant years per investment
    investment_years_interest = dicionario_anos_interesse(parametros_funcoes)

    # print()
    # print("THIS IS dic_anos_interesse:")
    # for investment, anos in investment_years_interest.items():
    #     print(f"{investment} -> {anos}")

    for investment, value in variacoes_patrimoniais_anuais.items():
        # Safeguard with .get() in case of missing investment
        relevant_years = investment_years_interest.get(investment, [])

        soma_investimentos = 0.0

        for year in relevant_years:
            year_str = str(year)
            try:
                # Ensure that year_str and keys "TOTAL ENTRADA" and "TOTAL SAIDA" exist
                if year_str in variacoes_patrimoniais_anuais[investment]:
                    soma_investimentos += variacoes_patrimoniais_anuais[investment].get(year_str, 0)
                else:
                    print(f"Warning: Year {year_str} missing for investment {investment}.")
            except KeyError as e:
                print(f"KeyError encountered: {e} for investment {investment}, year {year_str}")

        # Check if "TOTAL INTERESSE ENTRADA" exists, if not, create it
        if "TOTAL INTERESSE" not in variacoes_patrimoniais_anuais[investment]:
            variacoes_patrimoniais_anuais[investment]["TOTAL INTERESSE"] = 0.0

        # Save the results to the variacoes_patrimoniais_anuais dict
        variacoes_patrimoniais_anuais[investment]["TOTAL INTERESSE"] = soma_investimentos

    # print()
    # for investment, value in variacoes_patrimoniais_anuais.items():
    #     print(f"{investment} -> {value}")

    # Save the updated variacoes_patrimoniais_anuais
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_variacoes_patrimoniais_anuais,
                                                                                   variacoes_patrimoniais_anuais)

    # Optionally display the updated file
    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_variacoes_patrimoniais_anuais)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def atualizar_variacoes_patrimoniais_anuais(parametros_funcoes):
    print("&" * 90)
    print("THIS IS THE atualizar_variacoes_patrimoniais_anuais FUNCTION.")

    # Extract relevant parameters
    filepath_variacoes_patrimoniais_mensais = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")
    filepath_variacoes_patrimoniais_anuais = parametros_funcoes.get("filepath_variacoes_patrimoniais_anuais")
    # filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    # Decouple year_month_interest_end into its base components
    year_interest = year_month_interest_end.year
    year_interest_str = str(year_interest)
    month_interest_numeric = year_month_interest_end.month
    valid_months = centralized_imports.investimentos_btg.months_list[:month_interest_numeric]

    print(f"Processing data up to {year_month_interest_end} (year: {year_interest}, months: {valid_months})")

    # Load files
    try:
        variacoes_patrimoniais_mensais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_variacoes_patrimoniais_mensais))
        if not variacoes_patrimoniais_mensais:
            print("Empty or invalid variacoes_patrimoniais_mensais.")
            return
    except Exception as e:
        print(f"Error loading variacoes_patrimoniais_mensais: {e}")
        return

    try:
        variacoes_patrimoniais_anuais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_variacoes_patrimoniais_anuais))
        if variacoes_patrimoniais_anuais is None:
            variacoes_patrimoniais_anuais = {}
    except FileNotFoundError:
        print(f"File not found: {filepath_variacoes_patrimoniais_anuais}. Creating a new dictionary.")
        variacoes_patrimoniais_anuais = {}

    # try:
    #     dados_financeiros_historicos = (
    #         centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
    #             filepath_dados_financeiros_historicos))
    # except FileNotFoundError:
    #     print(f"File not found: {filepath_variacoes_patrimoniais_anuais}")

    # Iterate over investments, including "MERCADOS", "MODALIDADES", and "TOTAL"
    print()
    print("-" * 90)
    for investment, details in variacoes_patrimoniais_mensais.items():
        print("-" * 90)
        print(f"{investment} -> {details}")
        if investment not in variacoes_patrimoniais_anuais:
            variacoes_patrimoniais_anuais[investment] = {}
            variacoes_patrimoniais_anuais[investment][year_interest_str] = 0
            variacoes_patrimoniais_anuais[investment]["TOTAL INTERESSE"] = 0

        # Convert "DATA COMPRA" string to datetime (adjusting format to YYYY-MM-DD)
        data_compra_str = variacoes_patrimoniais_mensais[investment].get("DATA COMPRA", None)
        if data_compra_str:
            try:
                data_compra = (
                    centralized_imports.datetime.datetime.strptime(data_compra_str,
                                                                   "%Y-%m-%d"))
            except ValueError as e:
                print(f"Error parsing 'DATA COMPRA' for {investment}: {e}")
                continue
        else:
            data_compra = centralized_imports.datetime.datetime.min  # Use minimum date if "DATA COMPRA" doesn't exist

        total_for_year = 0.0
        total_all_years = 0.0

        # Loop through the years and sum values
        for year in range(data_compra.year, year_interest + 1):
            year_str = str(year)

            if year == year_interest:
                # Sum values only up to the selected month in the current year
                for month in valid_months:
                    key_short = f"{month.upper()}"
                    key_full = f"{month.upper()} {year_str}"
                    total_for_year += variacoes_patrimoniais_mensais[investment].get(key_short, 0.0)
                    total_for_year += variacoes_patrimoniais_mensais[investment].get(key_full, 0.0)
            else:
                # Sum values for previous years
                for month in centralized_imports.investimentos_btg.months_list:
                    key_full = f"{month.upper()} {year_str}"
                    total_for_year += variacoes_patrimoniais_mensais[investment].get(key_full, 0.0)

            # Add the yearly total to the grand total (all years)
            total_all_years += total_for_year

        # Save the yearly and total interest values in variacoes_patrimoniais_anuais
        variacoes_patrimoniais_anuais[investment][year_interest_str] = total_for_year
        variacoes_patrimoniais_anuais[investment]["TOTAL INTERESSE"] = total_all_years

        print(f"Total for {investment} up to {year_month_interest_end}: {total_for_year}")
        print(f"Total for {investment} (all years): {total_all_years}")

    # Save the updated variacoes_patrimoniais_anuais
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_variacoes_patrimoniais_anuais,
        variacoes_patrimoniais_anuais)

    print("Updated variacoes_patrimoniais_anuais saved.")



