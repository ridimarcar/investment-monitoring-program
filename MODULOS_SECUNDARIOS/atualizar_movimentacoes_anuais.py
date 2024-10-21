import centralized_imports

def dicionario_anos_interesse(parametros_funcoes):

    print()
    print("-" * 90)
    print("THIS IS THE dic_anos_interesse FUNCTION")

    year_interest = parametros_funcoes.get("year_interest")
    year_interest_str = str(year_interest)
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_movimentacoes_mensais_atual = parametros_funcoes.get("filepath_movimentacoes_mensais")

    # Open the current file containing monthly values
    movimentacoes_mensais_atual = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais_atual))

    dic_anos_interesse = {}
    for investment, value in movimentacoes_mensais_atual.items():
        # print(f"THIS IS INVESTMENT {investment}")
        # Extract the 'DATA COMPRA' field and convert it to a date
        data_compra = value.get("DATA COMPRA")
        # Check if 'DATA COMPRA' exists and is not None
        if data_compra:
            # Convert it to a date
            try:
                data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, "%Y-%m-%d")
                # print(f"Data Compra: {data_compra_date}")
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
            pass
            # print("No need to import extra files")

        dic_anos_interesse[investment] = anos_interesse

    # print()
    # print("THIS IS dic_anos_interesse:")
    # for investment, anos in dic_anos_interesse.items():
    #     print(f"{investment} -> {anos}")

    return dic_anos_interesse

def somar_historico_movimentacoes_anuais(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE somar_historico_movimentacoes_anuais FUNCTION")

    year_interest = parametros_funcoes.get("year_interest")
    year_interest_str = str(year_interest)

    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais)
    )

    # Fetch relevant years per investment
    investment_years_interest = dicionario_anos_interesse(parametros_funcoes)

    print()
    print("THIS IS dic_anos_interesse:")
    for investment, anos in investment_years_interest.items():
        print(f"{investment} -> {anos}")

    print()
    print("-" * 90)
    # Loop through each investment and calculate totals
    for investment, value in movimentacoes_anuais.items():
        print(investment)
        # print(f"{investment} - > {value}")
        relevant_years = investment_years_interest.get(investment, [])
        print("relevant_years = ", relevant_years)

        soma_entrada = 0
        soma_saida = 0
        for year in relevant_years:
            year_str = str(year)
            year_interest_entrada = f"{year_str} ENTRADA"
            year_interest_saida = f"{year_str} SAIDA"
            # print("year = ", year)
            print("year_interest_entrada = ", year_interest_entrada)
            print("year_interest_saida = ", year_interest_saida)

            try:
                # Retrieve "ENTRADA" and "SAIDA" values for this year
                entrada_value = movimentacoes_anuais[investment].get(year_interest_entrada, 0)
                saida_value = movimentacoes_anuais[investment].get(year_interest_saida, 0)

                # Add to cumulative totals
                soma_entrada += entrada_value
                soma_saida += saida_value

                print("soma_entrada = ", soma_entrada)
                print("soma_saida = ", soma_saida)
                print("-" * 90)

            except KeyError as e:
                print(f"KeyError encountered: {e} for investment {investment}, year {year_interest_str}")

        # Check if "TOTAL INTERESSE ENTRADA" and "TOTAL INTERESSE SAIDA" exist, if not, create them
        if "TOTAL INTERESSE ENTRADA" not in movimentacoes_anuais[investment]:
            movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"] = 0
            movimentacoes_anuais[investment]["TOTAL INTERESSE SAIDA"] = 0

        # Save the results to the movimentacoes_anuais dict
        movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"] = soma_entrada
        movimentacoes_anuais[investment]["TOTAL INTERESSE SAIDA"] = soma_saida

        print(f"Updated 'TOTAL INTERESSE ENTRADA' for {investment}: {soma_entrada}")
        print(f"Updated 'TOTAL INTERESSE SAIDA' for {investment}: {soma_saida}")

    print()
    print("Final movimentacoes_anuais:")
    for investment, value in movimentacoes_anuais.items():
        print(f"{investment} -> {value}")

    # Save the updated movimentacoes_anuais
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_movimentacoes_anuais, movimentacoes_anuais
    )

    # Optionally display the updated file
    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_movimentacoes_anuais)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def atualizar_movimentacoes_anuais(parametros_funcoes, config):
    print()
    print("&" * 90)
    print("THIS IS THE atualizar_movimentacoes_anuais FUNCTION.")

    # --------------------------------------------------------------------------------
    # Extract relevant parameters from the function arguments
    year_interest_str = str(parametros_funcoes.get("year_interest"))
    # month_interest = parametros_funcoes.get("month_interest")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")
    month_saida_key = parametros_funcoes.get("month_saida_key")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    months_list = centralized_imports.investimentos_btg.months_list
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Extract year and month from year_month_interest_end
    year_interest = year_month_interest_end.year
    year_interest_str = str(year_interest)
    year_interest_entrada = f"{year_interest_str} ENTRADA"
    year_interest_saida = f"{year_interest_str} SAIDA"
    month_interest = year_month_interest_end.month
    valid_months = months_list[:month_interest]  # Restrict valid months up to year_month_interest_end

    # --------------------------------------------------------------------------------
    # Handle automatic mode configuration
    input_mode = config.get("input_mode", "manual")
    if input_mode == "automatic":
        year_interest = config.get("selected_year")
        month_interest = config.get("selected_month")
        month_entrada_key = f"{month_interest} ENTRADA"
        month_saida_key = f"{month_interest} SAIDA"
        year_month_interest_start = centralized_imports.datetime.datetime.strptime(
            config.get("year_month_interest_start"), '%Y-%m-%d').date()
        year_month_interest_end = centralized_imports.datetime.datetime.strptime(
            config.get("year_month_interest_end"), '%Y-%m-%d').date()
        filepath_movimentacoes_mensais = config.get("filepath_movimentacoes_mensais")
        filepath_valores_mensais = config.get("filepath_valores_mensais")

    # --------------------------------------------------------------------------------
    print("-" * 90)
    print("LOADING FILES:")

    try:
        # Try to open the existing pickle file
        movimentacoes_anuais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_movimentacoes_anuais)
        # If the file is empty or corrupted and returns None, initialize an empty dictionary
        if movimentacoes_anuais is None:
            movimentacoes_anuais = {}
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty dictionary
        print(f"File not found: {filepath_movimentacoes_anuais}. Creating a new dictionary in memory.")
        movimentacoes_anuais = {}

    try:
        movimentacoes_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_movimentacoes_mensais)
        if movimentacoes_mensais is None or not isinstance(movimentacoes_mensais, dict) or not movimentacoes_mensais:
            print("Invalid or empty movimentacoes_mensais.")
            return
    except Exception as e:
        print(f"An error occurred while loading movimentacoes_mensais: {e}")
        return

    try:
        valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_valores_mensais)
        if valores_mensais is None or not isinstance(valores_mensais, dict) or not valores_mensais:
            print("Invalid or empty valores_mensais.")
            return
    except Exception as e:
        print(f"An error occurred while loading valores_mensais: {e}")
        return

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print("-" * 90)
    print("COPYING AND PASTING THE INVESTMENT INITIAL DATA")
    try:
        for investment in valores_mensais.keys():
            try:
                # Debugging: Print the current investment and its structure
                # print(f"Processing investment: {investment}")
                # print(f"valores_mensais[{investment}] = {valores_mensais[investment]}")

                # Check if the investment structure is as expected
                if not isinstance(valores_mensais[investment], dict):
                    print(
                        f"Warning: Expected a dictionary for {investment}, but got {type(valores_mensais[investment])}")
                    continue

                # Get investment initial data from valores_mensais
                mercado_valores_mensais = valores_mensais[investment].get('MERCADO', '')
                modalidade_valores_mensais = valores_mensais[investment].get('MODALIDADE', '')
                codigo_valores_mensais = valores_mensais[investment].get('CODIGO', '')
                data_compra_valores_mensais = valores_mensais[investment].get('DATA COMPRA', '')
                data_vencimento_valores_mensais = valores_mensais[investment].get('DATA VENCIMENTO', '')

                #Debugging: Print the values being copied
                # print("mercado_valores_mensais =", mercado_valores_mensais)
                # print("modalidade_valores_mensais =", modalidade_valores_mensais)
                # print("codigo_valores_mensais =", codigo_valores_mensais)
                # print("data_compra_valores_mensais =", data_compra_valores_mensais)
                # print("data_vencimento_valores_mensais =", data_vencimento_valores_mensais)

                # Ensure that movimentacoes_anuais[investment] is initialized as a dictionary if it doesn't exist
                if investment not in movimentacoes_anuais:
                    movimentacoes_anuais[investment] = {}

                # Save investment initial data to movimentacoes_anuais
                movimentacoes_anuais[investment]["MERCADO"] = mercado_valores_mensais
                movimentacoes_anuais[investment]["MODALIDADE"] = modalidade_valores_mensais
                movimentacoes_anuais[investment]["CODIGO"] = codigo_valores_mensais
                movimentacoes_anuais[investment]["DATA COMPRA"] = data_compra_valores_mensais
                movimentacoes_anuais[investment]["DATA VENCIMENTO"] = data_vencimento_valores_mensais

                # Debugging: Confirm that the data was copied correctly
                # print(f"Updated movimentacoes_anuais for investment '{investment}':")
                # print(movimentacoes_anuais[investment])

            except KeyError as e:
                print(f"KeyError: Missing key {e} in valores_mensais for investment '{investment}'")
            except Exception as e:
                print(f"An unexpected error occurred while processing investment '{investment}': {e}")

    except Exception as e:
        print(f"An unexpected error occurred in the outer block: {e}")
    print("movimentacoes_anuais initial data updated")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_movimentacoes_anuais,
                                                                                   movimentacoes_anuais)

    # ------------------------------------------------------------------
    print("UPDATING ENTRADA AND SAIDA TOTALS FOR ALL INVESTMENTS")
    print("-" * 95)

    contador_investimentos = 0
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
    investimentos_entrada_saida = {}
    for investment, details in movimentacoes_mensais.items():
        if investment in skip_investment_list or investment == "TOTAL":
            continue

        contador_investimentos += 1
        # print("-" * 90)
        # print(f"Processing investment {investment} (#{contador_investimentos})")

        # Initialize totals
        total_entrada = 0
        total_saida = 0

        for key, value in details.items():
            if "ENTRADA" in key or "SAIDA" in key:
                try:
                    value = float(value)
                except ValueError:
                    continue  # Skip non-numeric values

                # Extract the month from the key
                month_name = key.split()[0].upper()
                month_num = centralized_imports.investimentos_btg.month_name_mapping.get(month_name)

                # Create a date for the current key's month
                key_date = centralized_imports.datetime.date(year_month_interest_end.year, month_num, 1)

                # Perform summations for all months up to year_month_interest_end
                if key_date <= year_month_interest_end:
                    if "ENTRADA" in key and "TOTAL" not in key:
                        total_entrada += value
                    elif "SAIDA" in key and "TOTAL" not in key:
                        total_saida += value

        print(f"Total ENTRADA for {investment}: {total_entrada}")
        print(f"Total SAIDA for {investment}: {total_saida}")
        print("-" * 90)

        # Initialize the investment entry if it doesn't exist
        if investment not in investimentos_entrada_saida:
            investimentos_entrada_saida[investment] = {}

        investimentos_entrada_saida[investment]["ENTRADA"] = total_entrada
        investimentos_entrada_saida[investment]["SAIDA"] = total_saida

    # print("Final investimentos_entrada_saida:", investimentos_entrada_saida)

    # Save results
    for investment in movimentacoes_anuais.keys():
        if investment in skip_investment_list or investment == "TOTAL":
            continue
        if investment in investimentos_entrada_saida:
            if year_interest_entrada not in movimentacoes_anuais[investment]:
                movimentacoes_anuais[investment][year_interest_entrada] = 0
            movimentacoes_anuais[investment][year_interest_entrada] = investimentos_entrada_saida[investment][
                "ENTRADA"]
            movimentacoes_anuais[investment][year_interest_saida] = investimentos_entrada_saida[investment]["SAIDA"]

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_movimentacoes_anuais,
                                                                                   movimentacoes_anuais)

    # --------------------------------------------------------------------------------
    print("UPDATING TOTALS FOR EACH MERCADO AND MODALIDADE")
    print("-" * 95)

    # Initialize total variables
    month_total_entrada = 0
    month_total_saida = 0

    # Ensure 'TOTAL' key exists
    if 'TOTAL' not in movimentacoes_anuais:
        movimentacoes_anuais['TOTAL'] = {}
    movimentacoes_anuais['TOTAL'][year_interest_entrada] = 0
    movimentacoes_anuais['TOTAL'][year_interest_saida] = 0

    # Initialize totals for each mercado and modalidade
    mercado_totals = {}
    modalidade_totals = {}

    for investment, data in movimentacoes_anuais.items():
        if investment in skip_investment_list or investment == "TOTAL":
            continue
        print(f"Processing {investment} for MERCADO/MODALIDADE totals")
        # print(f"{investment} -> {data}")

        mercado = data.get('MERCADO', 'UNKNOWN')
        modalidade = data.get('MODALIDADE', 'UNKNOWN')

        if mercado not in mercado_totals:
            mercado_totals[mercado] = {}
            mercado_totals[mercado][year_interest_entrada] = 0
            mercado_totals[mercado][year_interest_saida] = 0
        if modalidade not in modalidade_totals:
            modalidade_totals[modalidade] = {}
            modalidade_totals[modalidade][year_interest_entrada] = 0
            modalidade_totals[modalidade][year_interest_saida] = 0

        entrada = data.get(year_interest_entrada, 0)
        saida = data.get(year_interest_saida, 0)

        mercado_totals[mercado][year_interest_entrada] += entrada
        mercado_totals[mercado][year_interest_saida] += saida
        modalidade_totals[modalidade][year_interest_entrada] += entrada
        modalidade_totals[modalidade][year_interest_saida] += saida

        month_total_entrada += entrada
        month_total_saida += saida

    # print("Final MERCADO totals:", mercado_totals)
    # print("Final MODALIDADE totals:", modalidade_totals)
    # print("Final TOTAL ENTRADA:", month_total_entrada)
    # print("Final TOTAL SAIDA:", month_total_saida)

    # Save the summation by MERCADO as separate keys
    # for mercado, totals in mercado_totals.items():
    #     if mercado not in movimentacoes_anuais:
    #         movimentacoes_anuais[mercado] = {}
    #     movimentacoes_anuais[mercado][year_interest_str] = totals

    print()
    print("-" * 90)
    for key, value in mercado_totals.items():
        print(f"{key} -> {value}")

    print()
    print("-" * 90)
    for key, value in modalidade_totals.items():
        print(f"{key} -> {value}")

    # Save the summation by MERCADO as separate keys
    for mercado, totals in mercado_totals.items():
        if mercado not in movimentacoes_anuais:
            movimentacoes_anuais[mercado] = {}
        movimentacoes_anuais[mercado][year_interest_entrada] = (
            mercado_totals)[mercado][year_interest_entrada]
        movimentacoes_anuais[mercado][year_interest_saida] = (
            mercado_totals)[mercado][year_interest_saida]

    # Save the summation by MODALIDADE as separate keys
    for modalidade, totals in modalidade_totals.items():
        if modalidade not in movimentacoes_anuais:
            movimentacoes_anuais[modalidade] = {}
        movimentacoes_anuais[modalidade][year_interest_entrada] = (
            modalidade_totals)[modalidade][year_interest_entrada]
        movimentacoes_anuais[modalidade][year_interest_saida] = (
            modalidade_totals)[modalidade][year_interest_saida]

    # Save the TOTALS
    movimentacoes_anuais['TOTAL'][year_interest_entrada] = month_total_entrada
    movimentacoes_anuais['TOTAL'][year_interest_saida] = month_total_saida

    # print("Saving the final movimentacoes_anuais with all totals")
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_movimentacoes_anuais,
                                                                                   movimentacoes_anuais)

    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_movimentacoes_anuais)
