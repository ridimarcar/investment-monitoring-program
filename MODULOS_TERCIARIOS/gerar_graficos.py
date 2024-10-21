import centralized_imports

def criar_graficos_pizza(parametros_funcoes):

    # CRIAR filtered_dict_mercados
    # -----------------------------------------------------------------------------
    mercados_list = centralized_imports.investimentos_btg.mercados_list
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    # Criar dicionario reduzido temporalmente
    valores_mensais_reduzido = centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
        valores_mensais, parametros_funcoes)

    # Apagar investimentos do dicionario. Nao se trata de uma reducao temporal
    for investment in list(valores_mensais_reduzido.keys()):
        # Check if the investment should be skipped or if it is empty
        if investment not in mercados_list or not valores_mensais_reduzido[investment]:
            del valores_mensais_reduzido[investment]

    # Working with the filtered_dict
    # Extract only the relevant keys: month_key_bruto and month_key_liquido
    filtered_dict_mercados = {}
    mercados_list = centralized_imports.investimentos_btg.mercados_list

    for investment, value in valores_mensais_reduzido.items():
        # Check if the keys exist in the nested dictionary and have non-zero values
        if (month_bruto_key in value and value[month_bruto_key] != 0) or (
                month_liquido_key in value and value[month_liquido_key] != 0):
            # Assign the values to the corresponding keys in the filtered_dict
            if investment in mercados_list:
                filtered_dict_mercados[investment] = {}
                filtered_dict_mercados[investment][month_bruto_key] = value.get(month_bruto_key, 0)
                filtered_dict_mercados[investment][month_liquido_key] = value.get(month_liquido_key, 0)
            else:
                print("Weird! Neither in mercados nor in modalidades.")
        else:
            print(f"Skipping empty or missing data for investment: {investment}")

    # CRIAR filtered_dict_modalidades
    # -----------------------------------------------------------------------------
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list
    # Criar dicionario reduzido temporalmente
    valores_mensais_reduzido = centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
        valores_mensais, parametros_funcoes)

    # Apagar investimentos do dicionario. Nao se trata de uma reducao temporal
    for investment in list(valores_mensais_reduzido.keys()):
        # Check if the investment should be skipped or if it is empty
        if investment not in modalidades_list or not valores_mensais_reduzido[investment]:
            del valores_mensais_reduzido[investment]

    # Extract only the relevant keys: month_key_bruto and month_key_liquido
    filtered_dict_modalidades = {}
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list

    for investment, value in valores_mensais_reduzido.items():
        # Check if the keys exist in the nested dictionary and have non-zero values
        if (month_bruto_key in value and value[month_bruto_key] != 0) or (
                month_liquido_key in value and value[month_liquido_key] != 0):
            # Assign the values to the corresponding keys in the filtered_dict
            if investment in modalidades_list:
                filtered_dict_modalidades[investment] = {}
                filtered_dict_modalidades[investment][month_bruto_key] = value.get(month_bruto_key, 0)
                filtered_dict_modalidades[investment][month_liquido_key] = value.get(month_liquido_key, 0)
            else:
                print("Weird! Neither in modalidades nor in modalidades.")
        else:
            print(f"Skipping empty or missing data for investment: {investment}")

    # CREATE PIE CHARTS
    # ----------------------------------------------------------------------------
    sort_key = month_bruto_key

    # Mercados_pie_chart
    sabor_pizza = "PIZZA VALORES MENSAIS MERCADOS"
    pedir_pizza(parametros_funcoes, sabor_pizza, sort_key, filtered_dict_mercados)

    # modalidades_pie_chart
    sabor_pizza = "PIZZA VALORES MENSAIS MODALIDADES"
    pedir_pizza(parametros_funcoes, sabor_pizza, sort_key, filtered_dict_modalidades)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# def criar_matriz_numpy(investment_dict, sort_key):

    # if not investment_dict:
    #     raise ValueError("The investment dictionary is empty.")

    # Extract the keys from the first nested dictionary to use as headers
    # headers = ["investment"] + list(next(iter(investment_dict.values())).keys())
    # print("Headers: ", headers)

    # if sort_key not in headers:
    #     raise ValueError(f"The sort_key '{sort_key}' is not in the headers: {headers}")
    # sort_index = headers.index(sort_key)

    # Initialize arrays
    # investment_names = []
    # numerical_data = []

    # Populate the arrays
    # for investment, data in investment_dict.items():
    #     investment_names.append(investment)
    #     numerical_data.append(list(data.values()))

    # print()
    # print("&" * 90)
    # print("Checking data type in numerical data - first check")
    # for i, data in enumerate(numerical_data):
    #     print(f"Row {i}: {data}, Type: {type(data)}")

    # Convert to NumPy arrays
    # investment_names = centralized_imports.np.array(investment_names)
    # numerical_data = centralized_imports.np.array(numerical_data)
    # print("Numerical data before sorting: \n", numerical_data)

    # Try converting to float if possible
    # try:
    #     numerical_data = numerical_data.astype(float)
    # except ValueError as e:
    #     print(f"Error converting data to floats: {e}")
    #     print(f"Problematic data: {numerical_data}")
    #     return None  # Exit the function if conversion fails

    # print()
    # print("-" * 90)
    # print("Checking data type in numerical data - second check")
    # for i, data in enumerate(numerical_data):
    #     print(f"Row {i}: {data}, Type: {type(data)}")

    # Get the index of the sort_key in the headers
    # if sort_key not in headers:
    #     raise ValueError(f"The sort_key '{sort_key}' is not in the headers: {headers}")
    # sort_index = headers.index(sort_key)
    # print()
    # print("Sort index: ", sort_index)

    # Check if the sort_index is valid for the number of columns
    # if numerical_data.shape[1] > 1:
    #     sorted_indices = centralized_imports.np.argsort(-numerical_data[:, sort_index])
    # else:
    #     print(f"Sorting by the only available column (index 0) since numerical_data has only one column.")
    #     sorted_indices = centralized_imports.np.argsort(-numerical_data[:, 0])  # Sort by the first and only column

    # Sort based on the specified key in decreasing order
    # sorted_investment_names = investment_names[sorted_indices]
    # sorted_numerical_data = numerical_data[sorted_indices]
    #
    # # Return as a tuple
    # return (headers, sorted_investment_names, sorted_numerical_data)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def gerar_matriz_numpy(dicionario,tipo_dicionario, parametros_funcoes):
    print("THIS IS THE gerar_matriz_numpy FUNCTION")
    # Extract relevant parameters from the function arguments
    year_interest = str(parametros_funcoes.get("year_interest"))
    month_interest = parametros_funcoes.get("month_interest")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    filepath_rentabilidade_mercados_modalidades = parametros_funcoes.get("filepath_rentabilidade_mercados_modalidades")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")
    month_saida_key = parametros_funcoes.get("month_saida_key")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    print(f"Selected Year: {year_interest}")
    print(f"Selected Month: {month_interest}")
    print(f"filepath_movimentacoes_mensais: {filepath_movimentacoes_mensais}")
    print(f"filepath_variacoes_mensais: {filepath_valores_mensais}")
    print(f"month_entrada_key = {month_entrada_key}")
    print(f"month_saida_key = {month_saida_key}")
    print(f"year_month_interest_start = {year_month_interest_start}")
    print(f"year_month_interest_end = {year_month_interest_end}")

    # -----------------------------------------------------------------
    # Create a deep copy if you want to modify rent_rep_reduzido independently of dicionario
    dicionario_temporalmente_reduzido = centralized_imports.copy.deepcopy(dicionario)

    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
    for investment in dicionario_temporalmente_reduzido.copy():
        if tipo_dicionario == "valores_mensais":
            if investment in skip_investment_list:
                del dicionario_temporalmente_reduzido[investment]
        elif tipo_dicionario == "rentabilidade_representatividade":
            if investment in skip_investment_list:
                del dicionario_temporalmente_reduzido[investment]
        elif tipo_dicionario == "rentabilidade_mercados_modalidades":
            if investment not in skip_investment_list:
                del dicionario_temporalmente_reduzido[investment]
        else:
            print("End of the line")

    # -----------------------------------------------------------------

    # Separate the investment names and numerical data
    investment_names = []
    numerical_data = []

    for investment, data in dicionario_temporalmente_reduzido.items():
        investment_names.append(investment)
        numerical_data.append([
            data.get('RENTABILIDADE TOTAL', 0),
            data.get('RENTABILIDADE ANUAL MEDIA', 0),
            data.get('RENTABILIDADE MENSAL MEDIA', 0),
            data.get('REPRESENTATIVIDADE', 0)
        ])

    # Convert the numerical data to a NumPy array
    numerical_data_array = centralized_imports.np.array(numerical_data)
    print()
    print("numerical_data_array = ", numerical_data_array)
    print()
    print("Shape of numerical_data_array:", numerical_data_array.shape)

    # # -------------------------------------------------------------------
    # # SORT THE DATA BY RENTABILIDADE ANUAL MEDIA
    # # Get the indices that would sort the array by 'RENTABILIDADE ANUAL MEDIA'
    # sorted_indices = centralized_imports.np.argsort(numerical_data_array[:, 1])
    #
    # # Sort the investment names and numerical data using the sorted indices
    # sorted_investment_names = centralized_imports.np.array(investment_names)[sorted_indices]
    # sorted_numerical_data_array = numerical_data_array[sorted_indices]

    # -------------------------------------------------------------------
    # SORT THE DATA BY RENTABILIDADE ANUAL MEDIA IN DECREASING ORDER
    # Get the indices that would sort the array by 'RENTABILIDADE ANUAL MEDIA'
    sorted_indices = centralized_imports.np.argsort(numerical_data_array[:, 1])[::-1]

    # Sort the investment names and numerical data using the reversed sorted indices
    sorted_investment_names = centralized_imports.np.array(investment_names)[sorted_indices]
    sorted_numerical_data_array = numerical_data_array[sorted_indices]

    # -------------------------------------------------------------------
    # CREATE A DATAFRAME FOR PRINTING sorted_investment_names AND
    # sorted_numerical_data_array AS A TABLE
    # Assuming df is your DataFrame
    df = centralized_imports.pd.DataFrame(
        sorted_numerical_data_array,
        index=sorted_investment_names,
        columns=[
            'RENTABILIDADE TOTAL',
            'RENTABILIDADE ANUAL MEDIA',
            'RENTABILIDADE MENSAL MEDIA',
            'REPRESENTATIVIDADE'
        ]
    )

    # Format the numerical columns as percentages with two decimal places
    df_formatted = df.style.format({
        'RENTABILIDADE TOTAL': "{:.2%}",
        'RENTABILIDADE ANUAL MEDIA': "{:.2%}",
        'RENTABILIDADE MENSAL MEDIA': "{:.2%}",
        'REPRESENTATIVIDADE': "{:.2%}"
    }).set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}]  # Center align the header
    ).set_properties(**{
        'text-align': 'center'  # Center align the data
    }).set_caption("Investment Performance Metrics")

    # Print the formatted DataFrame
    print("PRINTING THE df OBJECT")
    df['RENTABILIDADE TOTAL'] = df['RENTABILIDADE TOTAL'].apply(lambda x: f"{x:.2%}")
    df['RENTABILIDADE ANUAL MEDIA'] = df['RENTABILIDADE ANUAL MEDIA'].apply(lambda x: f"{x:.2%}")
    df['RENTABILIDADE MENSAL MEDIA'] = df['RENTABILIDADE MENSAL MEDIA'].apply(lambda x: f"{x:.2%}")
    df['REPRESENTATIVIDADE'] = df['REPRESENTATIVIDADE'].apply(lambda x: f"{x:.2%}")
    print(df)

    # Define the file paths
    image_filepath = \
        r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\investments_rent_rep_table.png"
    pdf_filepath = \
        r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\rent_rep_table.pdf"
    csv_filepath = \
        r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\rent_rep_table.csv"
    excel_filepath = \
        r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\rent_rep_table.xlsx"

    # Save the DataFrame to a CSV file (you can open this in Excel, for example)
    df.to_csv(csv_filepath)

    # Export to an Excel file with formatting
    with centralized_imports.pd.ExcelWriter(excel_filepath) as writer:
        df.to_excel(writer, sheet_name='RENT_REP')

    # Optional: Save the DataFrame as an image or PDF
    try:
        # import pdfkit
        # Save as image
        fig, ax = centralized_imports.plt.subplots(figsize=(10, len(df) * 0.3))  # Adjust figure size based on DataFrame length
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center')
        centralized_imports.plt.savefig(image_filepath, bbox_inches='tight')

        # # Save as PDF
        # html = df.to_html()
        # pdfkit.from_string(html, pdf_filepath)

    except ImportError as e:
        print(f"An error occurred while saving the DataFrame as an image or PDF: {e}")

    # return sorted_investment_names, sorted_numerical_data_array

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pedir_pizza(parametros_funcoes, sabor_pizza, sort_key, filtered_dict):

    print("&" * 90)
    print("THIS IS THE pedir_pizza FUNCTION")

    # Set up parameters
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    # print("month_bruto_key = ", month_bruto_key)

    centralized_imports.general_functions.GeneralFunctions.imprimir_dicionario_bonitinho("filtered_dict",filtered_dict)

    # Create numpy arrays from filtered_dicts
    numpy_arrays = (
        centralized_imports.gerar_graficos.criar_matriz_numpy(filtered_dict, sort_key))

    headers = numpy_arrays[0]
    sorted_names = numpy_arrays[1]
    sorted_numerical_data = numpy_arrays[2]

    # print("headers = ", headers)
    # print("sorted_names = ", sorted_names)
    # print("sorted_numerical_data = ", sorted_numerical_data)
    # print("sort_key = ", sort_key)

    if sabor_pizza == "PIZZA VALORES MENSAIS MERCADOS":
        # Extract the bruto values (first column in the numerical_data)
        bruto_values = sorted_numerical_data[:, 0]
        # Calculate percentages
        total = centralized_imports.np.sum(bruto_values)
        percentages = (bruto_values / total) * 100
        # Graph title
        centralized_imports.plt.title(f"Distribution of {sort_key}")
        # Graph file name
        pie_chart_name = "mercados_pie_chart.png"
        # Filepath
        filepath_pie_chart = \
            rf"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\{pie_chart_name}"
    elif sabor_pizza == "PIZZA VALORES MENSAIS MODALIDADES":
        # Extract the bruto values (first column in the numerical_data)
        bruto_values = sorted_numerical_data[:, 0]
        # Calculate percentages
        total = centralized_imports.np.sum(bruto_values)
        percentages = (bruto_values / total) * 100
        # Title
        centralized_imports.plt.title(f"Distribution of {month_bruto_key}")
        # Save the pie chart image with the correct filename and path
        pie_chart_name = "modalidades_pie_chart.png"
        filepath_pie_chart = \
            rf"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\{pie_chart_name}"

    # Plot the pie chart
    fig, ax = centralized_imports.plt.subplots()
    ax.pie(percentages,
           labels=sorted_names,
           autopct='%1.1f%%',
           startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart image
    centralized_imports.plt.savefig(filepath_pie_chart, bbox_inches='tight')

    # Optionally, show the pie chart (for debugging)
    centralized_imports.plt.show()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def criar_grafico_xy(tipo_grafico, parametros_funcoes):

    # Set up parameters
    filepath_dados_financeiros_historicos = (
        parametros_funcoes.get("filepath_dados_financeiros_historicos"))
    # filepath_grafico_evolucao_acumulada = parametros_funcoes.get("filepath_grafico_evolucao_acumulada")

    # Load files
    dados_financeiros_historicos = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_dados_financeiros_historicos))

    # Step 1: Extract the main keys (dates) and corresponding values
    x_values = []
    y_values = []
    z_values = []


    for date_str, data in dados_financeiros_historicos.items():
        # Convert date string to datetime object
        # date_obj = centralized_imports.datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        x_values.append(date_str)

        # Get the 'VARIACAO PATRIMONIAL ACUMULADA' value
        y_values.append(data.get("VARIACAO PATRIMONIAL ACUMULADA", 0.0))

        # Get the 'RENTABILIDADE MENSAL MEDIA' value
        z_values.append(data.get("RENTABILIDADE HISTORICA CARTEIRA", 0.0))

    # Step 2: Combine x_values and y_values into pairs and sort them by date (x-axis)
    sorted_pairs_xy = sorted(zip(x_values, y_values))
    sorted_pairs_xz = sorted(zip(x_values, z_values))

    # Step 3: Separate the sorted pairs into separate x and y lists
    sorted_x_values, sorted_y_values = zip(*sorted_pairs_xy)
    sorted_x_values, sorted_z_values = zip(*sorted_pairs_xz)

    # The sorted_x_values and sorted_y_values are now ready for plotting
    print("Sorted X-values (dates):", sorted_x_values)
    print("Sorted Y-values (VARIACAO PATRIMONIAL ACUMULADA):", sorted_y_values)
    print("Sorted Z-values (RENTABILIDADE MENSAL CARTEIRA):", sorted_z_values)

    # Create matplotlib xy scatter plot
    centralized_imports.plt.figure(figsize=(10, 6))

    if tipo_grafico == "VARIACAO PATRIMONIAL ACUMULADA":
        # Formatting the Y-axis with two decimal places
        ax = centralized_imports.plt.gca()
        ax.yaxis.set_major_formatter(centralized_imports.ticker.FormatStrFormatter('%.0f'))
        centralized_imports.plt.ylabel('VARIACAO PATRIMONIAL ACMUMULADA [R$]')
        filepath_save_scatter_plot = \
            r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_evol_patrimonial_acumulada.png"
        valores_eixo_y = sorted_y_values
    elif tipo_grafico == "RENTABILIDADE HISTORICA CARTEIRA":
        # Formatting the Y-axis with two decimal places
        ax = centralized_imports.plt.gca()
        ax.yaxis.set_major_formatter(centralized_imports.ticker.FormatStrFormatter('%.2f'))
        centralized_imports.plt.ylabel('RENTABILIDADE HISTORICA CARTEIRA  [%]')
        filepath_save_scatter_plot = \
            r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_hist_carteira.png"
        valores_eixo_y = sorted_z_values
    else:
        print("END OF THE LINE")

    centralized_imports.plt.scatter(sorted_x_values,
                                    valores_eixo_y,
                                    color='blue', 
                                    marker='o')


    centralized_imports.plt.xticks(rotation=45)
    centralized_imports.plt.grid(True)
    centralized_imports.plt.tight_layout()

    # Save the pie chart image
    centralized_imports.plt.savefig(filepath_save_scatter_plot)

    # Optionally, show the pie chart (for debugging)
    centralized_imports.plt.show()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def criar_grafico_barras_horizontais(tipo_grafico, parametros_funcoes):
    # Set up necessary parameters
    filepath_rentabilidade_representatividade = (
        parametros_funcoes.get("filepath_rentabilidade_representatividade"))
    mercados_list = centralized_imports.investimentos_btg.mercados_list
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list
    expanded_mercados_list = mercados_list + ["TOTAL"]
    expanded_modalidades_list = modalidades_list + ["TOTAL"]
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Load files
    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # Create time reduced dictionary
    rent_rep_reduzido = (
        centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
            rentabilidade_representatividade, parametros_funcoes))


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

    if tipo_grafico == "BARRAS RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS":
        print("-" * 90)
        print(tipo_grafico)
        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_rep_investimentos.png"
        # Delete unnecessary keys (mercados, modalidades, and total)
        for investment in rent_rep_reduzido.copy():
            if investment in skip_investment_list:
            # if investment in skip_investment_list or investment == "TOTAL":
                del rent_rep_reduzido[investment]
                # print(f"{investment} was deleted.")

    elif tipo_grafico == "BARRAS RENTABILIDADE REPRESENTATIVIDADE MERCADOS":
        print("-" * 90)
        print(tipo_grafico)
        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_rep_mercados.png"
        for investment in rent_rep_reduzido.copy():
            if investment not in expanded_mercados_list:
                del rent_rep_reduzido[investment]
                # print(f"{investment} was deleted.")
            # if investment == "TOTAL":
            #     del rent_rep_reduzido[investment]
        print("Checking data for BARRAS RENTABILIDADE REPRESENTATIVIDADE MERCADOS")
        for key, value in rent_rep_reduzido.items():
            print(f"{key} -> {value}")

    elif tipo_grafico == "BARRAS RENTABILIDADE REPRESENTATIVIDADE MODALIDADES":
        print("-" * 90)
        print(tipo_grafico)
        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_rep_modalidades.png"
        for investment in rent_rep_reduzido.copy():
            if investment not in expanded_modalidades_list:
                del rent_rep_reduzido[investment]
                # print(f"{investment} was deleted.")
            # if investment == "TOTAL":
            #     del rent_rep_reduzido[investment]
        print("Checking data for BARRAS RENTABILIDADE REPRESENTATIVIDADE MODALIDADES")
        for key, value in rent_rep_reduzido.items():
            print(f"{key} -> {value}")

    print("-" * 90)
    for key, value in rent_rep_reduzido.items():
        print(f"{key} -> {value}")

    # Sort data by "RENTABILIDADE ANUAL MEDIA" in descending order
    sort_key = "RENTABILIDADE ANUAL MEDIA"
    numpy_arrays = centralized_imports.gerar_graficos.criar_matriz_numpy(rent_rep_reduzido, sort_key)
    headers = numpy_arrays[0]
    sorted_names = numpy_arrays[1]
    sorted_numerical_data = numpy_arrays[2]

    print("Checking bar chart data: ")
    print("headers:")
    print(headers)
    print()
    print("sorted_names =")
    print(sorted_names)
    print()
    print("sorted_numerical_data")
    print(sorted_numerical_data)


    # Sort data explicitly in descending order by "Rentabilidade Anual Média"
    rentabilidade_index = headers.index("RENTABILIDADE ANUAL MEDIA") - 1
    representatividade_index = headers.index("REPRESENTATIVIDADE") - 1

    # Extract the data and sort by rentabilidade in descending order
    rentabilidade_data = sorted_numerical_data[:, rentabilidade_index]
    representatividade_data = sorted_numerical_data[:, representatividade_index]

    # Sort the data in descending order based on "Rentabilidade Anual Média"
    sorted_indices = centralized_imports.np.argsort(-rentabilidade_data)
    rentabilidade_data = rentabilidade_data[sorted_indices]
    representatividade_data = representatividade_data[sorted_indices]
    sorted_names = sorted_names[sorted_indices]

    # Combine rentabilidade_data and representatividade_data to calculate axis limits
    combined_data = centralized_imports.np.concatenate([rentabilidade_data, representatividade_data])

    # Calculate the min and max, then round them to the nearest multiple of 10
    min_value = centralized_imports.np.floor(min(combined_data) / 10) * 10
    max_value = centralized_imports.np.ceil(max(combined_data) / 10) * 10

    # Create the bar chart
    bar_width = 0.4
    y_positions = centralized_imports.np.arange(len(sorted_names))

    fig, ax = centralized_imports.plt.subplots(figsize=(10, len(sorted_names) * 0.5))

    # Handle color for positive and negative bars
    # colors = ['darkblue' if val >= 0 else 'darkred' for val in rentabilidade_data]

    # Handle color for positive and negative bars, and assign a specific color for "TOTAL"
    colors = []
    for idx, name in enumerate(sorted_names):
        if name == "TOTAL":
            colors.append('lightgreen')  # Use lightgreen for "TOTAL"
        else:
            colors.append('darkblue' if rentabilidade_data[idx] >= 0 else 'darkred')

    # Create the bars side by side
    ax.barh(y_positions + bar_width, rentabilidade_data, height=bar_width, color=colors,
            label='Rentabilidade Anual Média')
    ax.barh(y_positions, representatividade_data, height=bar_width, color='red', label='Representatividade')

    # Add faint dotted horizontal lines to separate the bars
    ax.hlines(y=y_positions + bar_width / 2, xmin=min_value, xmax=max_value,
              colors='gray', linestyles='dotted', linewidth=0.8)

    # Add faint dotted vertical lines at every 10% increment
    ax.vlines(x=centralized_imports.np.arange(min_value, max_value + 10, 10), ymin=-0.5, ymax=len(sorted_names) - 0.5,
              colors='gray', linestyles='dotted', linewidth=0.8)

    # Create font properties for bold and normal text
    bold_font = centralized_imports.fm.FontProperties(weight='bold')
    normal_font = centralized_imports.fm.FontProperties(weight='normal')

    # Set labels and title
    ax.set_yticks(y_positions + bar_width / 2)
    ax.set_yticklabels(sorted_names)
    ax.set_xlabel('RENTABILIDADE E REPRESENTATIVIDADE')
    # ax.set_title('Rentabilidade Anual Média e Representatividade')

    # Apply bold font to the "TOTAL" label
    for label, name in zip(ax.get_yticklabels(), sorted_names):
        if name == "TOTAL":
            label.set_fontproperties(bold_font)
        else:
            label.set_fontproperties(normal_font)

    # Adjust x-axis ticks to show increments of 10%
    ax.set_xticks(centralized_imports.np.arange(min_value, max_value + 10, 10))
    ax.xaxis.set_major_formatter(centralized_imports.plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

    ax.legend()

    # Save the plot to the specified filepath
    centralized_imports.plt.tight_layout()
    centralized_imports.plt.savefig(filepath_save_graph)

    # Show the plot (optional)
    centralized_imports.plt.show()

    # Close the plot
    centralized_imports.plt.close()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
def criar_grafico_barras_ganhos_saldos(tipo_grafico, parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE criar_grafico_barras_ganhos_saldos FUNCTION")

    # Set up necessary parameters
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_rentabilidade_representatividade = (
        parametros_funcoes.get("filepath_rentabilidade_representatividade"))
    mercados_list = centralized_imports.investimentos_btg.mercados_list
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list
    expanded_mercados_list = mercados_list + ["TOTAL"]
    expanded_modalidades_list = modalidades_list + ["TOTAL"]
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Load files
    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # Create time reduced dictionary
    rent_rep_reduzido = (
        centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(
            rentabilidade_representatividade, parametros_funcoes))

    # Sort data according to "vencidas" or "em vigor"
    rent_rep_vencidas = centralized_imports.copy.deepcopy(rent_rep_reduzido)
    rent_rep_vigor = centralized_imports.copy.deepcopy(rent_rep_reduzido)

    # Loop through rent_rep_vencidas
    for investment in list(rent_rep_vencidas):
        data_vencimento = rent_rep_vencidas[investment].get('DATA VENCIMENTO')
        if data_vencimento:
            data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
            if data_vencimento_date > year_month_interest_end:
                del rent_rep_vencidas[investment]

    # Loop through rent_rep_vigor
    for investment in list(rent_rep_vigor):
        data_vencimento = rent_rep_vigor[investment].get('DATA VENCIMENTO')
        if data_vencimento:
            data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
            if data_vencimento_date <= year_month_interest_end:
                del rent_rep_vigor[investment]

    # Print files for checking
    print("-" * 90)
    print("This is rent_rep_vencidas right after the vencidas-vigor sorting procedure")
    print()
    for key, value in rent_rep_vencidas.items():
        print(f"{key} -> {value}")

    print("-" * 90)
    print("This is rent_rep_vigor right after the vencidas-vigor sorting procedure")
    print()
    for key, value in rent_rep_vigor.items():
        print(f"{key} -> {value}")

    # Define the subkeys to keep
    subkeys_to_keep = ["GANHOS EFETIVOS", "SALDO ATUAL"]

    # Create filtered dictionaries
    filtered_rent_rep_vencidas = {}
    filtered_rent_rep_vigor = {}

    # Filter rent_rep_vencidas
    for main_key_vencidas, nested_dict_vencidas in rent_rep_vencidas.items():
        if isinstance(nested_dict_vencidas, dict):
            # Create a new dictionary with only the subkeys we want to keep
            filtered_rent_rep_vencidas[main_key_vencidas] = {
                key: value for key, value in nested_dict_vencidas.items() if key in subkeys_to_keep
            }

    # Check if the dictionary is empty
    # Default state
    vencidas_vazio = False
    if not rent_rep_vencidas:
        vencidas_vazio = True

    # Filter rent_rep_vigor
    for main_key_vigor, nested_dict_vigor in rent_rep_vigor.items():
        if isinstance(nested_dict_vigor, dict):
            # Create a new dictionary with only the subkeys we want to keep
            filtered_rent_rep_vigor[main_key_vigor] = {
                key: value for key, value in nested_dict_vigor.items() if key in subkeys_to_keep
            }

    # Print files for checking
    print("-" * 90)
    print("This is rent_rep_vencidas right after deleting unnecessary keys")
    for key, value in filtered_rent_rep_vencidas.items():
        print(f"{key} -> {value}")

    print("-" * 90)
    print("This is rent_rep_vigor right after deleting the unnecesary keys")
    for key, value in filtered_rent_rep_vigor.items():
        print(f"{key} -> {value}")

    if tipo_grafico == "BARRAS GANHOS SALDOS APLICACOES VENCIDAS":
        if vencidas_vazio:
            print("BARRAS GANHOS SALDOS APLICACOES VENCIDAS cannot be created. Dict is empty")
            return  # Exit the function
        print("-" * 90)
        print(tipo_grafico)
        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_ganhos_saldos_vencidas.png"
        rent_rep_geral = centralized_imports.copy.deepcopy(filtered_rent_rep_vencidas)
    elif tipo_grafico == "BARRAS GANHOS SALDOS APLICACOES EM VIGOR":
        print("-" * 90)
        print(tipo_grafico)
        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_ganhos_saldos_vigor.png"
        rent_rep_geral = centralized_imports.copy.deepcopy(filtered_rent_rep_vigor)

    print("-" * 90)
    print("This is rent_rep_geral right before creating the bar graph")
    for key, value in rent_rep_geral.items():
        print(f"{key} -> {value}")

    # Sort data by "RENTABILIDADE ANUAL MEDIA" in descending order
    sort_key = "GANHOS EFETIVOS"
    numpy_arrays = centralized_imports.gerar_graficos.criar_matriz_numpy(rent_rep_geral, sort_key)
    headers = numpy_arrays[0]
    sorted_names = numpy_arrays[1]
    sorted_numerical_data = numpy_arrays[2]

    print("Checking bar chart data: ")
    print("headers:")
    print(headers)
    print()
    print("sorted_names =")
    print(sorted_names)
    print()
    print("sorted_numerical_data")
    print(sorted_numerical_data)


    # Sort data explicitly in descending order by "ganhos efetivos"
    ganhos_index = headers.index("GANHOS EFETIVOS") - 1
    saldos_index = headers.index("SALDO ATUAL") - 1

    # Extract the data and sort by rentabilidade in descending order
    ganhos_data = sorted_numerical_data[:, ganhos_index]
    saldos_data = sorted_numerical_data[:, saldos_index]

    # Sort the data in descending order based on "Rentabilidade Anual Média"
    sorted_indices = centralized_imports.np.argsort(-ganhos_data)
    ganhos_data = ganhos_data[sorted_indices]
    saldos_data = saldos_data[sorted_indices]
    sorted_names = sorted_names[sorted_indices]

    # Combine ganhos_data and saldos_data to calculate axis limits
    combined_data = centralized_imports.np.concatenate([ganhos_data, saldos_data])

    # Calculate the min and max, then round them to the nearest multiple of 10
    min_value = centralized_imports.np.floor(min(combined_data) / 10) * 10
    max_value = centralized_imports.np.ceil(max(combined_data) / 10) * 10

    # Create the bar chart
    bar_width = 0.4
    y_positions = centralized_imports.np.arange(len(sorted_names))

    fig, ax = centralized_imports.plt.subplots(figsize=(10, len(sorted_names) * 0.5))

    # Handle color for positive and negative bars
    # colors = ['darkblue' if val >= 0 else 'darkred' for val in ganhos_data]

    # Handle color for positive and negative bars, and assign a specific color for "TOTAL"
    colors = []
    for idx, name in enumerate(sorted_names):
        if name == "TOTAL":
            colors.append('lightgreen')  # Use lightgreen for "TOTAL"
        else:
            colors.append('darkblue' if ganhos_data[idx] >= 0 else 'darkred')

    # Create the bars side by side
    ax.barh(y_positions + bar_width, ganhos_data, height=bar_width, color=colors,
            label='Rentabilidade Anual Média')
    ax.barh(y_positions, saldos_data, height=bar_width, color='red', label='Representatividade')

    # Add faint dotted horizontal lines to separate the bars
    ax.hlines(y=y_positions + bar_width / 2, xmin=min_value, xmax=max_value,
              colors='gray', linestyles='dotted', linewidth=0.8)

    # Add faint dotted vertical lines at every 10% increment
    ax.vlines(x=centralized_imports.np.arange(min_value, max_value + 10, 10), ymin=-0.5, ymax=len(sorted_names) - 0.5,
              colors='gray', linestyles='dotted', linewidth=0.8)

    # Create font properties for bold and normal text
    bold_font = centralized_imports.fm.FontProperties(weight='bold')
    normal_font = centralized_imports.fm.FontProperties(weight='normal')

    # Set labels and title
    ax.set_yticks(y_positions + bar_width / 2)
    ax.set_yticklabels(sorted_names)
    ax.set_xlabel('RENTABILIDADE E REPRESENTATIVIDADE')
    # ax.set_title('Rentabilidade Anual Média e Representatividade')

    # Apply bold font to the "TOTAL" label
    for label, name in zip(ax.get_yticklabels(), sorted_names):
        if name == "TOTAL":
            label.set_fontproperties(bold_font)
        else:
            label.set_fontproperties(normal_font)

    # Adjust x-axis ticks to show increments of 10%
    ax.set_xticks(centralized_imports.np.arange(min_value, max_value + 10, 10))
    ax.xaxis.set_major_formatter(centralized_imports.plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

    ax.legend()

    # Save the plot to the specified filepath
    centralized_imports.plt.tight_layout()
    centralized_imports.plt.savefig(filepath_save_graph)

    # Show the plot (optional)
    centralized_imports.plt.show()

    # Close the plot
    centralized_imports.plt.close()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def criar_matriz_numpy(investment_dict, sort_key):

    if not investment_dict:
        raise ValueError("The investment dictionary is empty.")

    # Extract the keys from the first nested dictionary to use as headers
    headers = ["investment"] + list(next(iter(investment_dict.values())).keys())
    print("Headers: ", headers)

    # Check if sort_key is in headers
    if sort_key not in headers:
        raise ValueError(f"The sort_key '{sort_key}' is not in the headers: {headers}")
    sort_index = headers.index(sort_key)

    # Initialize arrays
    investment_names = []
    numerical_data = []

    # Populate the arrays
    for investment, data in investment_dict.items():
        investment_names.append(investment)
        numerical_data.append(list(data.values()))

    # Convert to NumPy arrays
    investment_names = centralized_imports.np.array(investment_names)
    numerical_data = centralized_imports.np.array(numerical_data)

    # Check if the number of columns in numerical_data matches the headers
    if numerical_data.shape[1] != len(headers) - 1:  # -1 because "investment" is not part of numerical_data
        raise ValueError(f"Mismatch between headers and numerical data: headers={len(headers) - 1}, "
                         f"numerical_data={numerical_data.shape[1]}")

    # Convert numerical_data to float
    try:
        numerical_data = numerical_data.astype(float)
    except ValueError as e:
        print(f"Error converting data to floats: {e}")
        print(f"Problematic data: {numerical_data}")
        return None  # Exit the function if conversion fails

    # Sort the data by the specified sort_key
    sorted_indices = centralized_imports.np.argsort(-numerical_data[:, sort_index])

    # Sort investment names and numerical data
    sorted_investment_names = investment_names[sorted_indices]
    sorted_numerical_data = numerical_data[sorted_indices]

    # Return headers, sorted names, and sorted data
    return (headers, sorted_investment_names, sorted_numerical_data)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def criar_grafico_barras_ganhos_saldos_pandas(tipo_grafico, parametros_funcoes):
    print("&" * 90)
    print("THIS IS THE criar_grafico_barras_ganhos_saldos_pandas FUNCTION")

    # Set up necessary parameters
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    mercados_list = centralized_imports.investimentos_btg.mercados_list
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list

    # Load files
    rentabilidade_representatividade = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_rentabilidade_representatividade)

    # Create time reduced dictionary
    rent_rep_reduzido = centralized_imports.investimentos_functions.InvestimentosFunctions.reduzir_dicionario_temporalmente(rentabilidade_representatividade, parametros_funcoes)

    # Filter out mercados and modalidades
    for investment in list(rent_rep_reduzido):
        if investment in mercados_list or investment in modalidades_list:
            del rent_rep_reduzido[investment]

    # Sort data according to "vencidas" or "em vigor"
    rent_rep_vencidas = centralized_imports.copy.deepcopy(rent_rep_reduzido)
    rent_rep_vigor = centralized_imports.copy.deepcopy(rent_rep_reduzido)

    # Filter vencidas and vigor data
    for investment in list(rent_rep_vencidas):
        data_vencimento = rent_rep_vencidas[investment].get('DATA VENCIMENTO')
        if data_vencimento:
            data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
            if data_vencimento_date > year_month_interest_end:
                del rent_rep_vencidas[investment]

    for investment in list(rent_rep_vigor):
        data_vencimento = rent_rep_vigor[investment].get('DATA VENCIMENTO')
        if data_vencimento:
            data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
            if data_vencimento_date <= year_month_interest_end:
                del rent_rep_vigor[investment]

    # Filter only the relevant subkeys
    subkeys_to_keep = ["GANHOS EFETIVOS", "SALDO ATUAL"]
    filtered_rent_rep_vencidas = {k: {key: value for key, value in v.items() if key in subkeys_to_keep} for k, v in rent_rep_vencidas.items()}
    filtered_rent_rep_vigor = {k: {key: value for key, value in v.items() if key in subkeys_to_keep} for k, v in rent_rep_vigor.items()}

    # Check if dictionary is empty
    vencidas_vazio = not bool(filtered_rent_rep_vencidas)
    vigor_vazio = not bool(filtered_rent_rep_vigor)

    # Handling the first case: "BARRAS GANHOS APLICACOES VENCIDAS"
    if tipo_grafico == "BARRAS GANHOS APLICACOES VENCIDAS":
        if vencidas_vazio:
            print("BARRAS GANHOS SALDOS APLICACOES VENCIDAS cannot be created. Dict is empty")
            return  # Exit the function

        df = centralized_imports.pd.DataFrame.from_dict(filtered_rent_rep_vencidas, orient='index')
        df = df.sort_values(by='GANHOS EFETIVOS', ascending=False)

        # Ensure y_positions is a NumPy array
        y_positions = centralized_imports.np.arange(len(df.index))
        bar_width = 0.4

        # Bar chart
        fig, ax = centralized_imports.plt.subplots(figsize=(10, len(df) * 0.5))
        ax.barh(y_positions, df['GANHOS EFETIVOS'], height=bar_width, color='red', label='Ganho Efetivo')

        # Calculate the min and max for the x-axis limits
        min_value = (df['GANHOS EFETIVOS'].min() // 10) * 10
        max_value = (df['GANHOS EFETIVOS'].max() // 10 + 1) * 10

        # Add dotted lines
        ax.hlines(y=y_positions + bar_width / 2, xmin=min_value, xmax=max_value,
                  colors='gray', linestyles='dotted', linewidth=0.8)
        ax.vlines(x=centralized_imports.np.arange(min_value, max_value + 100, 100), ymin=-0.5, ymax=len(df.index) - 0.5,
                  colors='gray', linestyles='dotted', linewidth=0.8)

        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_ganhos_saldos_vencidas.png"

    # Handling the second case: "BARRAS GANHOS SALDOS APLICACOES EM VIGOR"
    elif tipo_grafico == "BARRAS GANHOS SALDOS APLICACOES EM VIGOR":
        if vigor_vazio:
            print("BARRAS GANHOS SALDOS APLICACOES EM VIGOR cannot be created. Dict is empty")
            return  # Exit the function

        df = centralized_imports.pd.DataFrame.from_dict(filtered_rent_rep_vigor, orient='index')
        df = df.sort_values(by='GANHOS EFETIVOS', ascending=False)

        combined_data = centralized_imports.pd.concat([df['GANHOS EFETIVOS'], df['SALDO ATUAL']])
        min_value = (combined_data.min() // 10) * 10
        max_value = (combined_data.max() // 10 + 1) * 10

        # Ensure y_positions is a NumPy array
        y_positions = centralized_imports.np.arange(len(df.index))
        bar_width = 0.4

        # Bar chart
        fig, ax = centralized_imports.plt.subplots(figsize=(10, len(df) * 0.5))
        ax.barh(y_positions, df['GANHOS EFETIVOS'], height=bar_width, color='red', label='Ganho Efetivo')
        ax.barh(y_positions + bar_width, df['SALDO ATUAL'], height=bar_width, color='lightgreen', label='Saldo Atual')

        # Add dotted lines
        ax.hlines(y=y_positions + bar_width / 2, xmin=min_value, xmax=max_value,
                  colors='gray', linestyles='dotted', linewidth=0.8)
        ax.vlines(x=centralized_imports.np.arange(min_value, max_value + 10000, 10000), ymin=-0.5, ymax=len(df.index) - 0.5,
                  colors='gray', linestyles='dotted', linewidth=0.8)

        filepath_save_graph = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_ganhos_saldos_vigor.png"

    # Set labels and formatting for both cases
    ax.set_yticks(y_positions + bar_width / 2)
    ax.set_yticklabels(df.index)
    ax.set_xlabel('VALORES')

    # Legend and layout
    ax.legend()
    centralized_imports.plt.tight_layout()
    centralized_imports.plt.savefig(filepath_save_graph)
    centralized_imports.plt.show()
    centralized_imports.plt.close()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def criar_grafico_xy_pandas(tipo_grafico, parametros_funcoes):
    # Set up parameters
    filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")

    # Load files
    dados_financeiros_historicos = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_dados_financeiros_historicos))

    # Convert dictionary to DataFrame
    df = centralized_imports.pd.DataFrame.from_dict(dados_financeiros_historicos, orient='index')

    # For debugging purposes
    print("----- TABLE ROWS -----:")
    for index in df.index:
        print(index)

    print("\n----- TABLE COLUMNS -----:")
    for column in df.columns:
        print(column)

    # Sort the DataFrame by index
    df_time_sorted = df.sort_index(ascending=True)

    # Create the scatter plot
    centralized_imports.plt.figure(figsize=(10, 6))

    # Handle different graph types
    if tipo_grafico == "VARIACAO PATRIMONIAL ACUMULADA":
        df_filtered = df_time_sorted[df_time_sorted.index != '2021-01-31']
        centralized_imports.plt.scatter(df_filtered.index, df_filtered['VARIACAO PATRIMONIAL ACUMULADA'],
                                        label='VARIACAO PATRIMONIAL', marker='o')
        ax = centralized_imports.plt.gca()
        ax.yaxis.set_major_formatter(centralized_imports.ticker.FormatStrFormatter('%.0f'))
        centralized_imports.plt.ylabel('VARIACAO PATRIMONIAL ACUMULADA [R$]')
        filepath_save_scatter_plot = (
            r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_variacao_patrimonial_acumulada.png")

    elif tipo_grafico == "RENTABILIDADE CARTEIRA":
        # Multiply profitability values by 100 to convert them to percentages
        df_time_sorted['RENTABILIDADE TOTAL CARTEIRA'] *= 100
        df_time_sorted['RENTABILIDADE ANUAL CARTEIRA'] *= 100
        df_time_sorted['RENTABILIDADE MENSAL CARTEIRA'] *= 100
        # Filter out the outlier for plotting
        df_filtered = df_time_sorted[df_time_sorted.index != '2021-01-31']
        centralized_imports.plt.scatter(df_filtered.index, df_filtered['RENTABILIDADE TOTAL CARTEIRA'],
                                        label='RENTABILIDADE TOTAL', marker='o')
        centralized_imports.plt.scatter(df_filtered.index, df_filtered['RENTABILIDADE ANUAL CARTEIRA'],
                                        label='RENTABILIDADE ANUAL MEDIA', marker='s')
        centralized_imports.plt.scatter(df_filtered.index, df_filtered['RENTABILIDADE MENSAL CARTEIRA'],
                                        label='RENTABILIDADE MENSAL MEDIA', marker='^')
        ax = centralized_imports.plt.gca()
        ax.yaxis.set_major_formatter(centralized_imports.ticker.FormatStrFormatter('%.2f'))
        centralized_imports.plt.ylabel('RENTABILIDADE [%]')
        filepath_save_scatter_plot = (
            r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_carteira.png")
    else:
        print("END OF THE LINE")
        return  # Exit the function since no valid graph type was provided

    # Finalize plot formatting
    centralized_imports.plt.xticks(rotation=45)
    centralized_imports.plt.grid(True)
    centralized_imports.plt.tight_layout()

    # Save the scatter plot image
    centralized_imports.plt.savefig(filepath_save_scatter_plot)

    # Optionally, show the scatter plot (for debugging)
    centralized_imports.plt.show()



