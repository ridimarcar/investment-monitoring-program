import centralized_imports

def tabela_valores_mensais(parametros_funcoes):

    # Set up necessary parameters
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Load files
    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    # Create reduced dictionary
    valores_mensais_reduzido = centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
        valores_mensais, parametros_funcoes)

    centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
        "valores_mensais_reduzido",valores_mensais_reduzido)

    # Delete unnecessary keys (mercados, modalidades, and total)
    for investment in valores_mensais_reduzido.copy():
        if investment in skip_investment_list or investment == "TOTAL":
            del valores_mensais_reduzido[investment]

    centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
        "valores_mensais_reduzido", valores_mensais_reduzido)

    # Extract only the relevant keys: month_bruto_key and month_liquido_key
    filtered_dict = {}
    for investment, value in valores_mensais_reduzido.items():
        filtered_dict[investment] = {
            month_bruto_key: value.get(month_bruto_key, 0),
            month_liquido_key: value.get(month_liquido_key, 0)
        }

    centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho(
        "filtered_dict", filtered_dict)

    # Create and save the table as an image
    tipo_tabela = "TABELA VALORES MENSAIS INVESTIMENTOS"

    centralized_imports.gerar_tabelas.construir_imagem_tabela(parametros_funcoes,
                                                              tipo_tabela,
                                                              filtered_dict
                                                              )

def tabela_movimentacoes_mensais(parametros_funcoes):

    # Set up necessary parameters
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")
    month_saida_key = parametros_funcoes.get("month_saida_key")
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
    mercados_list = centralized_imports.investimentos_btg.mercados_list
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list

    # Load files
    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    # --------------------------------------------------------------
    # CRIAR TABELA DE MOVIMENTACOES MENSAIS DOS INVESTIMENTOS

    # Check for non-numeric entries
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_movimentacoes_mensais)

    # Create reduced dictionary
    movimentacoes_mensais_reduzido = (
        centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
            movimentacoes_mensais, parametros_funcoes))

    print("Initial movimentacoes_mensais_reduzido =")
    for key, value in movimentacoes_mensais_reduzido.items():
        print(f"{key} - > {value}")

    # Extract only the relevant keys: month_key_bruto and month_key_liquido
    filtered_dict_investimentos = {}
    for investment, value in movimentacoes_mensais_reduzido.items():
        if investment in skip_investment_list or investment == "TOTAL":
            print(f"Skipping {investment}: in skip_investment_list or is TOTAL")
            continue
        entrada_value = value.get(month_entrada_key, 0)
        saida_value = value.get(month_saida_key, 0)

        # Try to convert both values to floats (if they are not already)
        try:
            entrada_value = float(entrada_value)
        except (ValueError, TypeError):
            entrada_value = 0
        try:
            saida_value = float(saida_value)
        except (ValueError, TypeError):
            saida_value = 0

        if entrada_value == 0 and saida_value == 0:
            print(f"Skipping {investment}: Both entrada and saida are zero.")
            continue

        filtered_dict_investimentos[investment] = {}

        # Check if the keys exist in the nested dictionary
        if month_entrada_key in value and month_saida_key in value:
            filtered_dict_investimentos[investment][month_entrada_key] = value[month_entrada_key]
            filtered_dict_investimentos[investment][month_saida_key] = value[month_saida_key]
        else:
            filtered_dict_investimentos[investment][month_entrada_key] = 0 if month_entrada_key not in value else value[month_entrada_key]
            filtered_dict_investimentos[investment][month_saida_key] = 0 if month_saida_key not in value else value[month_saida_key]

    print("Filtered dict before passing:")
    for key, value in filtered_dict_investimentos.items():
        print(f"{key} - > {value}")

    # Create table
    tipo_tabela = "TABELA MOVIMENTACOES MENSAIS INVESTIMENTOS"
    construir_imagem_tabela(parametros_funcoes, tipo_tabela, filtered_dict_investimentos)

# -------------------------------------------------------------------------
def tabela_rentabilidade_representavidade(parametros_funcoes):

    # Set up necessary parameters
    filepath_rentabilidade_representatividade = (
        parametros_funcoes.get("filepath_rentabilidade_representatividade"))
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Load files
    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_rentabilidade_representatividade))

    # --------------------------------------------------------------
    # CRIAR TABELA DE RENTABILIDADE-REPRESENTAVIDADE DOS INVESTIMENTOS

    # Create time reduced dictionary
    rent_rep_reduzido = (
        centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
            rentabilidade_representatividade, parametros_funcoes))

    # Delete unnecessary main keys (mercados, modalidades, and total)
    for investment in rent_rep_reduzido.copy():
        if investment in skip_investment_list and investment == "TOTAL":
            del rent_rep_reduzido[investment]

    # Delete unnecessary subkeys (MERCADO, MODALIDADE, etc.)
    subkey_exists = False
    subkeys_to_delete = [
        "MERCADO",
        "MODALIDADE",
        "CODIGO",
        "DATA COMPRA",
        "DATA VENCIMENTO",
        "GANHOS EFETIVOS",
        "SALDO ATUAL"
    ]

    for main_key, nested_dict in rent_rep_reduzido.items():
        if isinstance(nested_dict, dict):
            # Check and delete each subkey in the subkeys_to_delete list
            for subkey_to_delete in subkeys_to_delete:
                if subkey_to_delete in nested_dict:
                    subkey_exists = True
                    # Delete the subkey from the nested dictionary
                    del nested_dict[subkey_to_delete]

    print()
    for key, value in rent_rep_reduzido.items():
        print(f"{key} -> {value}")

    # Create table
    tipo_tabela = "TABELA RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS"
    construir_imagem_tabela(parametros_funcoes,tipo_tabela, rent_rep_reduzido)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def tabelas_evolucao_patrimonial(parametros_funcoes):

    # Set up necessary parameters
    # filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    filepath_variacoes_patrimoniais_mensais = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")
    month_interest = parametros_funcoes.get("month_interest")
    # month_bruto_key = parametros_funcoes.get("month_bruto_key")
    # month_liquido_key = parametros_funcoes.get("month_liquido_key")
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Check filepath
    print("filepath_variacoes_patrimoniais_mensais = ", filepath_variacoes_patrimoniais_mensais)

    # Load files
    try:
        variacoes_patrimoniais_mensais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_variacoes_patrimoniais_mensais))
        print("File loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{filepath_variacoes_patrimoniais_mensais}' was not found.")
    except EOFError:
        print(f"Error: The file '{filepath_variacoes_patrimoniais_mensais}' appears to be empty or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the file '{filepath_variacoes_patrimoniais_mensais}': {e}")

    # ----------------------------------------------------------------------------
    # CRIAR TABELA DE EVOLUCAO PATRIMONIAL MENSAL DOS INVESTIMENTOS

    # Check for non-numeric entries
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_variacoes_patrimoniais_mensais)

    # There is no need for this to be a time reduced dictionary
    # Delete unnecessary keys (mercados, modalidades, and total)
    for investment in variacoes_patrimoniais_mensais.copy():
        if investment in skip_investment_list or investment == "TOTAL":
            del variacoes_patrimoniais_mensais[investment]

    # Extract only the relevant keys: month_interest
    filtered_dict = {}
    for investment, value in variacoes_patrimoniais_mensais.items():
        if value[month_interest] == 0:
            continue
        filtered_dict[investment] = {
            month_interest: value.get(month_interest, 0)
        }

    # Create table
    tipo_tabela = "TABELA EVOLUCAO PATRIMONIAL INVESTIMENTOS"
    construir_imagem_tabela(parametros_funcoes, tipo_tabela, filtered_dict)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def tabela_variacoes_patrimoniais_mensais(parametros_funcoes):

    # Set up necessary parameters
    # filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    filepath_variacoes_patrimoniais_mensais = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")
    filepath_variacoes_patrimoniais_anuais = parametros_funcoes.get("filepath_variacoes_patrimoniais_anuais")
    month_interest = parametros_funcoes.get("month_interest")
    # month_bruto_key = parametros_funcoes.get("month_bruto_key")
    # month_liquido_key = parametros_funcoes.get("month_liquido_key")
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Check filepath
    print("filepath_variacoes_patrimoniais_anuais = ", filepath_variacoes_patrimoniais_anuais)

    # Load files
    try:
        variacoes_patrimoniais_mensais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_variacoes_patrimoniais_mensais))
        print("File loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{filepath_variacoes_patrimoniais_mensais}' was not found.")
    except EOFError:
        print(f"Error: The file '{filepath_variacoes_patrimoniais_mensais}' appears to be empty or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the file '{filepath_variacoes_patrimoniais_mensais}': {e}")

    try:
        variacoes_patrimoniais_anuais = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_variacoes_patrimoniais_anuais))
        print("File loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{filepath_variacoes_patrimoniais_anuais}' was not found.")
    except EOFError:
        print(f"Error: The file '{filepath_variacoes_patrimoniais_anuais}' appears to be empty or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the file '{filepath_variacoes_patrimoniais_anuais}': {e}")

    # There is no need for this to be a time reduced dictionary
    # Delete unnecessary keys (mercados, modalidades, and total)
    for investment in variacoes_patrimoniais_anuais.copy():
        if investment in skip_investment_list or investment == "TOTAL":
            del variacoes_patrimoniais_anuais[investment]

    filtered_dict = {}

    for investment, value in variacoes_patrimoniais_anuais.items():
        # Store the inner dictionary for cleaner code
        investment_data = variacoes_patrimoniais_anuais[investment]

        # Check if "TOTAL INTERESSE" exists and is not zero
        if investment_data.get("TOTAL INTERESSE", 0) == 0:
            continue

        print('variacoes_patrimoniais_anuais[investment][TOTAL INTERESSE] =')
        print(investment_data["TOTAL INTERESSE"])

        # Add the data to the filtered dictionary
        filtered_dict[investment] = investment_data["TOTAL INTERESSE"]

    print()
    print("Checking dict before calling TABELA VARIACOES PATRIMONIAIS INVESTIMENTOS")
    for key, value in filtered_dict.items():
        print(f"{key} -> {value}")

    # Create table
    tipo_tabela = "TABELA VARIACOES PATRIMONIAIS INVESTIMENTOS"
    construir_imagem_tabela(parametros_funcoes, tipo_tabela, filtered_dict)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def construir_imagem_tabela(parametros_funcoes, tipo_tabela, filtered_reduced_dict):
    print()
    print("&" * 90)
    print("THIS IS THE construir_imagem_tabela FUNCTION")

    # SET UP PARAMETERS
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_interest = parametros_funcoes.get("month_interest")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")

    # TAKE CARE OF INDIVIDUAL CASES
    if tipo_tabela == "TABELA VALORES MENSAIS INVESTIMENTOS":
        sort_key = month_bruto_key
        # Create a NumPy array from filtered_dict
        numpy_arrays = (
            centralized_imports.gerar_graficos.criar_matriz_numpy(filtered_reduced_dict,
                                                                  sort_key))
        headers = numpy_arrays[0]
        sorted_names = numpy_arrays[1]
        sorted_numerical_data = numpy_arrays[2]
        # Convert numerical_data to a DataFrame
        df_reduzido = centralized_imports.pd.DataFrame(data=sorted_numerical_data,
                                                       index=sorted_names,
                                                       columns=headers[1:])
        image_filepath = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\valores_mensais_reduzido.png"
        # Adjust column widths manually (starting with 0 for the first actual column)
        col_widths = {0: 0.35, 1: 0.35}
        # Set the locale to Brazilian Portuguese for currency formatting
        centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')
        # Format the numbers as Brazilian currency
        df_reduzido = df_reduzido.applymap(lambda x: centralized_imports.locale.currency(x, grouping=True))

    elif tipo_tabela == "TABELA MOVIMENTACOES MENSAIS INVESTIMENTOS":
        sort_key = month_entrada_key
        # Create a NumPy array from filtered_dict
        print("-" * 90)
        print("Checking TABELA MOVIMENTACOES MENSAIS INVESTIMENTOS")
        print("tipo_tabela = ", tipo_tabela)
        print()
        for key, value in filtered_reduced_dict.items():
            print(f"{key} -> {value}")
        print()
        numpy_arrays = (
            centralized_imports.gerar_graficos.criar_matriz_numpy(filtered_reduced_dict,
                                                                  sort_key))
        headers = numpy_arrays[0]
        sorted_names = numpy_arrays[1]
        sorted_numerical_data = numpy_arrays[2]
        # Convert numerical_data to a DataFrame
        df_reduzido = centralized_imports.pd.DataFrame(data=sorted_numerical_data,
                                                       index=sorted_names,
                                                       columns=headers[1:])
        image_filepath = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\movimentacoes_mensais_investimentos.png"
        # Adjust column widths manually (starting with 0 for the first actual column)
        col_widths = {0: 0.35, 1: 0.35}
        # Set the locale to Brazilian Portuguese for currency formatting
        centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')
        # Format the numbers as Brazilian currency
        # df_reduzido = df_reduzido.applymap(lambda x: centralized_imports.locale.currency(x, grouping=True))
        # Format the numbers as Brazilian currency (ensure the data is numeric)
        df_reduzido = df_reduzido.applymap(
            lambda x: centralized_imports.locale.currency(x, grouping=True) if isinstance(x, (int, float)) else x
        )

    elif tipo_tabela == "TABELA RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS":
        sort_key = "RENTABILIDADE ANUAL MEDIA"
        numpy_arrays = centralized_imports.gerar_graficos.criar_matriz_numpy(filtered_reduced_dict,
                                                                             sort_key)
        headers = numpy_arrays[0]
        sorted_names = numpy_arrays[1]
        sorted_numerical_data = numpy_arrays[2]
        # Convert numerical_data to a DataFrame
        df_reduzido = centralized_imports.pd.DataFrame(data=sorted_numerical_data,
                                                       index=sorted_names,
                                                       columns=headers[1:])
        df_reduzido = df_reduzido * 100
        # Format the numbers as percentages with two decimal places
        df_reduzido = df_reduzido.applymap(lambda x: f"{x:.2f}%")
        # Save the table as an image
        image_filepath = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\rent_rep_investimentos.png"
        col_widths = {0: 0.20, 1: 0.35, 2: 0.35, 3: 0.20, 4: 0.35}

    elif tipo_tabela == "TABELA VARIACOES PATRIMONIAIS INVESTIMENTOS":
        # sort_key_evolucao_investimentos = "TOTAL INTERESSE"
        # Create a NumPy array from filtered_dict
        # numpy_arrays = (
        #     centralized_imports.gerar_graficos.criar_matriz_numpy(filtered_reduced_dict,
        #                                                           sort_key_evolucao_investimentos))

        # Create lists for investment names and corresponding values from the dictionary
        investment_names = []
        investment_values = []

        for investment, value in filtered_reduced_dict.items():
            # Append the investment name and the corresponding value
            investment_names.append(investment)
            investment_values.append(value)

        # Convert to numpy arrays
        investment_names_array = centralized_imports.np.array(investment_names)
        investment_values_array = centralized_imports.np.array(investment_values)

        # Sort the numerical values in descending order
        sorted_indices = centralized_imports.np.argsort(-investment_values_array)
        sorted_names = investment_names_array[sorted_indices]
        sorted_numerical_data = investment_values_array[sorted_indices]

        # Create the headers
        headers = ['Investimento', 'Valor']

        # Output sorted data
        print("Headers: ", headers)
        print("Sorted Names: ", sorted_names)
        print("Sorted Values: ", sorted_numerical_data)

        print()
        print("Checking numpy array")
        print("headers")
        print(headers)
        print()
        print("sorted_names")
        print(sorted_names)
        print()
        print("sorted_numerical_data")
        print(sorted_numerical_data)

        # Convert numerical_data to a DataFrame
        df_reduzido = centralized_imports.pd.DataFrame(data=sorted_numerical_data,
                                                       index=sorted_names,
                                                       columns=headers[1:])
        # Set the locale to Brazilian Portuguese for currency formatting
        centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')
        # Format the numbers as Brazilian currency
        df_reduzido = df_reduzido.applymap(lambda x: centralized_imports.locale.currency(x, grouping=True))
        # Save the table as an image
        image_filepath = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\tab_variacoes_patrimoniais_investimentos.png"
        # Adjust column widths manually (starting with 0 for the first actual column)
        col_widths = {0: 0.35, 1: 0.35}  # Adjust this dict for each column number and width

    # RELAX WITH COMMON CODE SNIPPET
    # Check if dataframe is empty
    if df_reduzido.empty:
        print("The DataFrame is empty. No data to display.")

    # Save the DataFrame as an image file with improved font size and uniform row height
    fig, ax = centralized_imports.plt.subplots(figsize=(12, len(df_reduzido) * 0.6))
    ax.axis('tight')
    ax.axis('off')

    # Create a table with larger fonts
    table = ax.table(cellText=df_reduzido.values,
                     colLabels=[f"{col}" for col in df_reduzido.columns],
                     rowLabels=[f"{row}" for row in df_reduzido.index],
                     cellLoc='center',
                     loc='center')

    # Apply larger font size to the table cells
    table.auto_set_font_size(False)  # Disable auto-adjusting the font size
    table.set_fontsize(16)  # Set a larger font size for all cells

    # Set uniform row height for all cells
    for (i, j), cell in table.get_celld().items():
        cell.set_height(0.15)  # Uniform height for all cells (adjust this value as needed)
        if i == 0 or j == -1:  # Header row (i==0) or Row labels (j==-1)
            cell.set_text_props(fontweight='bold')
            cell.set_fontsize(16)  # Make headers larger

    for col_idx in col_widths:
        for (i, j), cell in table.get_celld().items():
            if j == col_idx:
                cell.set_width(col_widths[col_idx])

    # Save the table as an image with a tight bounding box
    centralized_imports.plt.savefig(image_filepath,
                                    bbox_inches='tight',
                                    dpi=300)

    # Optionally, show the image if you want to verify it
    centralized_imports.plt.show()


