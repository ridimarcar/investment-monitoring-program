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
def criar_matriz_numpy(investment_dict, sort_key):

    if not investment_dict:
        raise ValueError("The investment dictionary is empty.")

    # Extract the keys from the first nested dictionary to use as headers
    headers = ["investment"] + list(next(iter(investment_dict.values())).keys())
    print("Headers: ", headers)

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

    print()
    print("-" * 90)
    print("Checking data type in numerical data - first check")
    for i, data in enumerate(numerical_data):
        print(f"Row {i}: {data}, Type: {type(data)}")

    # Convert to NumPy arrays
    investment_names = centralized_imports.np.array(investment_names)
    numerical_data = centralized_imports.np.array(numerical_data)
    print("Numerical data before sorting: \n", numerical_data)

    # Try converting to float if possible
    try:
        numerical_data = numerical_data.astype(float)
    except ValueError as e:
        print(f"Error converting data to floats: {e}")
        print(f"Problematic data: {numerical_data}")
        return None  # Exit the function if conversion fails

    print()
    print("-" * 90)
    print("Checking data type in numerical data - second check")
    for i, data in enumerate(numerical_data):
        print(f"Row {i}: {data}, Type: {type(data)}")

    # try:
    #     numerical_data = numerical_data.astype(float)
    # except ValueError as e:
    #     print(f"Error converting data to floats: {e}")
    #     print(f"Problematic data: {numerical_data}")

    # Get the index of the sort_key in the headers
    if sort_key not in headers:
        raise ValueError(f"The sort_key '{sort_key}' is not in the headers: {headers}")
    sort_index = headers.index(sort_key)
    print()
    print("Sort index: ", sort_index)

    # Ensure all data is numeric
    print(f"Numerical data before conversion: {numerical_data}")

    # # Try converting to floats if necessary
    # try:
    #     numerical_data = numerical_data.astype(float)
    # except ValueError:
    #     print("Error: Some elements in numerical_data are not numbers!")

    # Check if the sort_index is valid for the number of columns
    if numerical_data.shape[1] > 1:
        sorted_indices = centralized_imports.np.argsort(-numerical_data[:, sort_index])
    else:
        print(f"Sorting by the only available column (index 0) since numerical_data has only one column.")
        sorted_indices = centralized_imports.np.argsort(-numerical_data[:, 0])  # Sort by the first and only column

    # Sort based on the specified key in decreasing order
    sorted_investment_names = investment_names[sorted_indices]
    sorted_numerical_data = numerical_data[sorted_indices]

    # Return as a tuple
    return (headers, sorted_investment_names, sorted_numerical_data)

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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# def criar_grafico_barras_horizontais(parametros_funcoes):
#
#     # Set up necessary parameters
#     filepath_rentabilidade_representatividade = (
#         parametros_funcoes.get("filepath_rentabilidade_representatividade"))
#     skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
#
#     # Load files
#     rentabilidade_representatividade = (
#         centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
#             filepath_rentabilidade_representatividade))
#
#     # Create reduced dictionary
#     rent_rep_reduzido = (
#         centralized_imports.investimentos_functions.InvestimentosFunctions.criar_dicionario_reduzido(
#             rentabilidade_representatividade, parametros_funcoes))
#
#     # Delete unnecessary keys (mercados, modalidades, and total)
#     for investment in rent_rep_reduzido.copy():
#         if investment in skip_investment_list or investment == "TOTAL":
#             del rent_rep_reduzido[investment]
#
#     sort_key = "RENTABILIDADE ANUAL MEDIA"
#     numpy_arrays = centralized_imports.gerar_graficos.criar_matriz_numpy(rent_rep_reduzido, sort_key)
#     headers = numpy_arrays[0]
#     sorted_names = numpy_arrays[1]
#     sorted_numerical_data = numpy_arrays[2]
#
#     # Create a grouped horizontal bar chart
#     rentabilidade_index = headers.index("RENTABILIDADE ANUAL MEDIA") - 1
#     representatividade_index = headers.index("REPRESENTATIVIDADE") - 1
#
#     rentabilidade_data = sorted_numerical_data[:, rentabilidade_index] * 100
#     representatividade_data = sorted_numerical_data[:, representatividade_index] * 100
#
#     # Print headers neatly
#     print("=" * 50)
#     print("DEBUGGING BAR GRAPH OUTPUT")
#     print("Headers:")
#     print(", ".join(headers))  # Prints headers in a single line, separated by commas
#
#     # Print sorted_names and sorted_numerical_data neatly
#     print("-" * 50)
#     print("Sorted Data (Names and Numerical Values):")
#     print(f"{'Investment':<20} {' | '.join(headers[1:])}")  # Align headers with the data columns
#
#     for i, (name, data_row) in enumerate(zip(sorted_names, sorted_numerical_data)):
#         # Print investment name and corresponding data row with 2 decimal precision
#         formatted_row = " | ".join([f"{value * 100:.2f}" for value in data_row])
#         print(f"{name:<20} {formatted_row}")
#
#     print("=" * 50)
#     # Print rentabilidade_data neatly
#     print("=" * 50)
#     print("DEBUGGING OUTPUT")
#     print("Rentabilidade Anual Média (in %):")
#     for i, value in enumerate(rentabilidade_data):
#         print(f"Investment {i + 1}: {value:.2f}%")
#
#     # Print representatividade_data neatly
#     print("-" * 50)
#     print("Representatividade (in %):")
#     for i, value in enumerate(representatividade_data):
#         print(f"Investment {i + 1}: {value:.2f}%")
#     print("=" * 50)
#
#     bar_width = 0.4
#     y_positions = centralized_imports.np.arange(len(sorted_names))
#
#     # Reverse the order of y_positions, sorted_names, and data arrays to have the highest values on top
#     y_positions = centralized_imports.np.arange(len(sorted_names))[::-1]
#     sorted_names = sorted_names[::-1]  # Reverse names
#     rentabilidade_data = rentabilidade_data[::-1]  # Reverse the data for rentabilidade
#     representatividade_data = representatividade_data[::-1]  # Reverse the data for representatividade
#
#     fig, ax = centralized_imports.plt.subplots(figsize=(10, len(sorted_names) * 0.5))
#
#     # Create the bars side by side
#     ax.barh(y_positions + bar_width, rentabilidade_data, height=bar_width, color='darkblue',
#             label='Rentabilidade Anual Média')
#     ax.barh(y_positions, representatividade_data, height=bar_width, color='red',
#             label='Representatividade')
#
#     # Add faint dotted horizontal lines to separate the bars
#     ax.hlines(y=y_positions + bar_width / 2, xmin=0, xmax=50, colors='gray', linestyles='dotted', linewidth=0.8)
#
#     # Set labels and title
#     ax.set_yticks(y_positions + bar_width / 2)
#     ax.set_yticklabels(sorted_names)
#     ax.set_xlabel('RENTABILIDADE E REPRESENTATIVIDADE')
#     ax.set_title('Rentabilidade Anual Média e Representatividade')
#     ax.legend()
#
#     # Format the x-axis to show percentages
#     ax.xaxis.set_major_formatter(centralized_imports.plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
#
#     # Save the plot to the specified filepath
#     filepath_graf_rent_rep_investimentos = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_rep_investimentos.png"
#     centralized_imports.plt.tight_layout()
#     centralized_imports.plt.savefig(filepath_graf_rent_rep_investimentos)
#
#     # Show the plot (optional)
#     centralized_imports.plt.show()
#
#     # Close the plot
#     centralized_imports.plt.close()

def criar_grafico_barras_horizontais(parametros_funcoes):

    # Set up necessary parameters
    filepath_rentabilidade_representatividade = (
        parametros_funcoes.get("filepath_rentabilidade_representatividade"))
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Load files
    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # Create reduced dictionary
    rent_rep_reduzido = (
        centralized_imports.investimentos_functions.InvestimentosFunctions.criar_dicionario_reduzido(
            rentabilidade_representatividade, parametros_funcoes))

    # Delete unnecessary keys (mercados, modalidades, and total)
    for investment in rent_rep_reduzido.copy():
        if investment in skip_investment_list or investment == "TOTAL":
            del rent_rep_reduzido[investment]

    # Sort data by "RENTABILIDADE ANUAL MEDIA" in descending order
    sort_key = "RENTABILIDADE ANUAL MEDIA"
    numpy_arrays = centralized_imports.gerar_graficos.criar_matriz_numpy(rent_rep_reduzido, sort_key)
    headers = numpy_arrays[0]
    sorted_names = numpy_arrays[1]
    sorted_numerical_data = numpy_arrays[2]

    # Sort data explicitly in descending order by "Rentabilidade Anual Média"
    rentabilidade_index = headers.index("RENTABILIDADE ANUAL MEDIA") - 1
    representatividade_index = headers.index("REPRESENTATIVIDADE") - 1

    # Extract the data and sort by rentabilidade in descending order
    rentabilidade_data = sorted_numerical_data[:, rentabilidade_index] * 100
    representatividade_data = sorted_numerical_data[:, representatividade_index] * 100

    # Sort the data in descending order based on "Rentabilidade Anual Média"
    sorted_indices = centralized_imports.np.argsort(-rentabilidade_data)
    rentabilidade_data = rentabilidade_data[sorted_indices]
    representatividade_data = representatividade_data[sorted_indices]
    sorted_names = sorted_names[sorted_indices]

    # Create the bar chart without reversing
    bar_width = 0.4
    y_positions = centralized_imports.np.arange(len(sorted_names))  # Keep y_positions as is, no need to reverse

    fig, ax = centralized_imports.plt.subplots(figsize=(10, len(sorted_names) * 0.5))

    # Create the bars side by side
    ax.barh(y_positions + bar_width, rentabilidade_data, height=bar_width, color='darkblue',
            label='Rentabilidade Anual Média')
    ax.barh(y_positions, representatividade_data, height=bar_width, color='red',
            label='Representatividade')

    # Add faint dotted horizontal lines to separate the bars
    ax.hlines(y=y_positions + bar_width / 2, xmin=0, xmax=100, colors='gray', linestyles='dotted', linewidth=0.8)

    # Add faint dotted vertical lines at every 10% increment
    ax.vlines(x=centralized_imports.np.arange(0, 110, 10), ymin=-0.5, ymax=len(sorted_names)-0.5,
              colors='gray', linestyles='dotted', linewidth=0.8)

    # Set labels and title
    ax.set_yticks(y_positions + bar_width / 2)
    ax.set_yticklabels(sorted_names)
    ax.set_xlabel('RENTABILIDADE E REPRESENTATIVIDADE')
    ax.set_title('Rentabilidade Anual Média e Representatividade')

    # Adjust x-axis ticks to show increments of 10%
    ax.set_xticks(centralized_imports.np.arange(0, 110, 10))  # Ticks from 0% to 100% in increments of 10%
    ax.xaxis.set_major_formatter(centralized_imports.plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

    ax.legend()

    # Save the plot to the specified filepath
    filepath_graf_rent_rep_investimentos = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\RELATORIOS\graf_rent_rep_investimentos.png"
    centralized_imports.plt.tight_layout()
    centralized_imports.plt.savefig(filepath_graf_rent_rep_investimentos)

    # Show the plot (optional)
    centralized_imports.plt.show()

    # Close the plot
    centralized_imports.plt.close()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pedir_pizza(parametros_funcoes, sabor_pizza, sort_key, filtered_dict):

    print("-" * 90)
    print("THIS IS THE pedir_pizza FUNCTION")

    # Set up parameters
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    print("month_bruto_key = ", month_bruto_key)

    # Create numpy arrays from filtered_dicts
    numpy_arrays = (
        centralized_imports.gerar_graficos.criar_matriz_numpy(filtered_dict, sort_key))

    headers = numpy_arrays[0]
    sorted_names = numpy_arrays[1]
    sorted_numerical_data = numpy_arrays[2]

    print("headers = ", headers)
    print("sorted_names = ", sorted_names)
    print("sorted_numerical_data = ", sorted_numerical_data)
    print("sort_key = ", sort_key)

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

