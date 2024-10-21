import centralized_imports

def historico_movimentacoes_mensais(parametros_funcoes):

    print()
    print("-" * 90)
    print("THIS IS THE historico_movimentacoes_mensais FUNCTION")

    year_interest = parametros_funcoes.get("year_interest")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_movimentacoes_mensais_atual = parametros_funcoes.get("filepath_movimentacoes_mensais")

    year_interest_str = str(year_interest)

    # Open the current file containing monthly values
    movimentacoes_mensais_atual = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais_atual))

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

        # Loop through the years from the purchase year up to (but not including) the year of interest
        # print("year_interest = ", year_interest_str)
        # print("year_data_compra = ", year_data_compra)

        anos = [year_interest_str]
        if year_data_compra < year_interest:
            base_filepath = "movimentacoes_mensais_"

            # Generate file paths for each year from the year of purchase to the year of interest
            for ano in range(year_data_compra, year_interest):
                anos.append(ano)
                filepath_valores_mensais_ano = base_filepath + str(ano) + ".pickle"
                print(f"Generated filepath: {filepath_valores_mensais_ano}")

                # If you need to load the file for each year, you can add the code to open it here
                try:
                    valores_mensais_ano = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais_ano)
                    # print(f"Not too bad! I could load the pickle file for ano {ano}")
                except FileNotFoundError:
                    pass
                    # print(f"File not found: {filepath_valores_mensais_ano}")
        else:
            pass
            # print("No need to import extra files")

    return anos

    # ++++++++++++++++++++++++++++++++++++++++++++++++++


