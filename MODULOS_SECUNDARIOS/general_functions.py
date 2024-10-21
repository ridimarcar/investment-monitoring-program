# MEUS MODULOS DE PROGRAMACAO REUTILIZAVEIS
# ===========================================================================
import centralized_imports

yes_list = ["y", "yes", "s", "sim"]

# ----------------------------------------------------------------

class GeneralFunctions:

    @staticmethod
    def imprimir_dicionario_bonitinho(dict_name, dicionario):
        print("-" * 90)
        print(f"Printing {dict_name}")
        print()
        for key, value in dicionario.items():
            print(f"{key}")
            print(f"{value}")
            print()
        print()

    # ===================================================================
    import math

    @staticmethod
    def converter_para_numerico(filepath_arquivo_pickle):
        print()
        print("-" * 90)
        print("THIS IS THE converter_para_numerico FUNCTION.")

        # Load the dictionary from the pickle file
        arquivo_pickle_restaurado = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_arquivo_pickle)

        # Keys to check for conversion
        keys_to_check = centralized_imports.investimentos_btg.floats_list

        def convert_values(d):
            print()
            for key, value in d.items():
                # Check if the key contains any of the words in keys_to_check
                # print("-" * 90)
                # print(f"{key} -> {value}")
                if any(word in key.upper() for word in keys_to_check):
                    try:
                        # Handle cases where value is NaN, None, or empty string
                        if value in [None, '', 'NaN', 'nan'] or (
                                isinstance(value, float) and centralized_imports.math.isnan(value)):
                            d[key] = 0.0
                        # If value is not already a float, attempt to convert it
                        elif not isinstance(value, float):
                            d[key] = float(value)

                    except (ValueError, TypeError):
                        print(f"Warning: Couldn't convert {key}: {value} to float. Setting it to 0.0.")
                        d[key] = 0.0  # Set the value to 0.0 if it fails to convert

                # Recursively process nested dictionaries
                if isinstance(value, dict):
                    convert_values(value)

        # Apply conversion to the dictionary
        convert_values(arquivo_pickle_restaurado)

        # Save the modified dictionary back to the pickle file
        centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_arquivo_pickle,
                                                                                       arquivo_pickle_restaurado)

    @staticmethod
    def recuperar_caminhos_arquivos(year_interest):
        print("=" * 90)
        print("THIS IS THE recuperar_caminhos_arquivos FUNCTION")

        # Ensure that year_interest is treated as a string
        year_interest_str = str(year_interest)
        # print(f"Looking for filepaths for year: {year_interest_str}")

        filepaths_list = centralized_imports.investimentos_btg.filepaths_list
        filepath_movimentacoes_mensais_year_interest = None
        filepath_valores_mensais_year_interest = None
        filepath_variacoes_patrimoniais_mensais_year_interest = None

        for filepath in filepaths_list:
            # print(f"Checking filepath: {filepath}")
            if f"movimentacoes_mensais_{year_interest_str}" in filepath:
                filepath_movimentacoes_mensais_year_interest = filepath
                print("Found movimentacoes_mensais filepath: ", filepath_movimentacoes_mensais_year_interest)
            elif f"valores_mensais_{year_interest_str}" in filepath:
                filepath_valores_mensais_year_interest = filepath
                print("Found valores_mensais filepath: ", filepath_valores_mensais_year_interest)
            elif f"variacoes_patrimoniais_mensais_{year_interest_str}" in filepath:
                filepath_variacoes_patrimoniais_mensais_year_interest = filepath
                print("Found variacoes_patrimoniais_mensais filepath: ",
                      filepath_variacoes_patrimoniais_mensais_year_interest)

            if (
                    filepath_movimentacoes_mensais_year_interest and
                    filepath_valores_mensais_year_interest and
                    filepath_variacoes_patrimoniais_mensais_year_interest
            ):
                break

        # caminhos_arquivos_recuperados = [filepath_movimentacoes_mensais_year_interest,
        #                                  filepath_valores_mensais_year_interest,
        #                                  filepath_variacoes_patrimoniais_mensais_year_interest]
        #
        # print("Caminhos Arquivos Recuperados: ", caminhos_arquivos_recuperados)
        caminhos_arquivos_recuperados = [
            filepath_movimentacoes_mensais_year_interest,
            filepath_valores_mensais_year_interest,
            filepath_variacoes_patrimoniais_mensais_year_interest
        ]

        # Print each item on a new line
        # print("Caminhos Arquivos Recuperados:")
        # for caminho in caminhos_arquivos_recuperados:
        #     print(f"- {caminho}")

        return caminhos_arquivos_recuperados

    # ==================================================================================
    @staticmethod
    def escolher_opcao_lista(options):
        # Generate the input prompt dynamically based on the available options
        prompt = f"Escolha uma destas opções:\n"
        for index, option in enumerate(options, start=1):
            prompt += f"{index}. {option}\n"
        prompt += "Inserir o número correspondente à sua escolha: "

        # Prompt the user to select a choice
        print()
        user_choice_index = input(prompt)

        # Perform actions based on the user's choice
        if user_choice_index.isdigit():
            user_choice_index = int(user_choice_index)
            if 1 <= user_choice_index <= len(options):
                selected_option = options[user_choice_index - 1]
                print(f"You selected {selected_option}.")
                print()
            else:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Please enter a number within the range of available options.")

        return selected_option

    # ===================================================================
    @staticmethod
    def mostrar_tabela_pickle(filepath_pickle):
        arquivo_pickle_restaurado = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle))
        data_flat = []
        for key, value in arquivo_pickle_restaurado.items():
            row = {'investment': key}
            row.update(value)
            data_flat.append(row)
        # Create DataFrame
        df = centralized_imports.pd.DataFrame(data_flat)

        # Format specific columns as percentages
        percentage_columns = [
            'RENTABILIDADE TOTAL',
            'RENTABILIDADE MENSAL MEDIA',
            'RENTABILIDADE ANUAL MEDIA',
            'REPRESENTATIVIDADE'
        ]

        for column in percentage_columns:
            if column in df.columns:
                df[column] = df[column].apply(lambda x: f"{x * 100:.2f}%" if isinstance(x, (int, float)) else x)

        # Select specific columns if specified
        # selected_columns = ['Investment', 'MODALIDADE', 'CODIGO', 'MARCO BRUTO', 'MARCO LIQUIDO']
        selected_columns = None
        if selected_columns is not None:
            df = df[selected_columns]
        # Convert DataFrame to a tabular format with borders
        table = centralized_imports.tabulate(df, headers='keys', tablefmt='fancy_grid')
        # Print the tabulated data
        print(table)

    # =================================================================================
    @staticmethod
    def mostrar_tabela_excel(filepath_pickle, output_excel_path):
        # Load pickle file
        arquivo_pickle_restaurado = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle)

        # Flatten the data into a list of dictionaries
        data_flat = []
        for key, value in arquivo_pickle_restaurado.items():
            row = {'Investment': key}
            row.update(value)
            data_flat.append(row)

        # Create DataFrame
        df = centralized_imports.pd.DataFrame(data_flat)

        # Select specific columns if specified (uncomment and modify if needed)
        selected_columns = ['Investment',
                            'MODALIDADE',
                            'CODIGO',
                            'JANEIRO BRUTO',
                            'JANEIRO LIQUIDO',
                            'FEVEREIRO BRUTO',
                            'FEVEREIRO LIQUIDO',
                            'MARCO BRUTO',
                            'MARCO LIQUIDO',
                            'ABRIL BRUTO',
                            'ABRIL LIQUIDO',
                            'MAIO BRUTO',
                            'MAIO LIQUIDO',
                            'JUNHO BRUTO',
                            'JUNHO LIQUIDO']
        df = df[selected_columns] if selected_columns is not None else df

        # Write DataFrame to an Excel file
        df.to_excel(output_excel_path, index=False)

        print(f"Data successfully written to {output_excel_path}")

    @staticmethod
    def number_days(date1, date2):
        data1 = date1
        data2 = date2
        # Calculate the difference between the dates
        difference = date2 - date1
        # Extract the number of days from the difference
        number_days = difference.days
        print("Number of days between the two dates:", number_days)
        return number_days

    # ----------------------------------------------------------------
    @staticmethod
    def user_float_input(texto):
        while True:
            try:
                variavel = float(input(texto))
                break  # Exit the loop if successful
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        return variavel

    # ----------------------------------------------------------------
    @staticmethod
    def yes_no(texto):
        yes_list = ["y", "yes", "s", "sim"]
        no_list = ["n", "no", "nao"]

        while True:
            answer = input(texto).strip().lower()  # Convert user input to lowercase
            if answer in yes_list:
                return "yes"  # Return 'yes' for a positive response
            elif answer in no_list:
                return "no"  # Return 'no' for a negative response
            else:
                print("Invalid input. Please enter y/n or sim/nao.")  # Prompt for valid input


# ====================================================================

class FormattingFunctions:
    @staticmethod
    # ----------------------------------------------------------------
    # Function to emulate grid lines
    def create_grid(window, rows, columns, button_width=10, button_height=2):

        # Change the background color to a warm sepia tone
        window.configure(bg="#FFFF66")

        # Create a rowsxcolumns grid
        for i in range(rows, columns):
            for j in range(3):
                cell_number = f"({i},{j})"
                grid_label = centralized_imports.tk.Label(window, text=cell_number, bg="#F3F5F0",
                                      width=button_width, height=button_height,
                                      borderwidth=1, relief="solid")
                grid_label.grid(row=i, column=j, pady=5, padx=5)

    @staticmethod
    # ----------------------------------------------------------------
    # Function to style an input box
    def styled_input(prompt):
        print("+" + "-" * 80 + "+")
        print("|" + " " * 12 + prompt + " " * 12 + "|")
        print("+" + "-" * 80 + "+")
        return input()

    # ----------------------------------------------------------------
    # Function to sort out a list
    def ordenar_lista(lista):
        lista_ordenada = sorted(lista, key=lambda x: (x.isdigit(), x))
        return lista_ordenada

    # ----------------------------------------------------------------
    # Function to sort the array based on a given header
    @staticmethod
    def ordenar_matriz_crescente(array, headers):
        print("array =", array)
        print("headers =", headers)

        for index, header_name in enumerate(headers, start=1):
            print(f"{index}. {header_name}")
        print()

        while True:
            try:
                header_index = int(input("DIGITE O NUMERO DA COLUNA PARA ORDENAMENTO DA TABELA: "))
                if 1 <= header_index <= len(headers):
                    selected_header = headers[header_index - 1]
                    break
                else:
                    print("Invalid selection. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Sort the array based on the specified header
        sorted_array = sorted(array, key=lambda x: x[header_index - 1])

        return sorted_array

    # ----------------------------------------------------------------
    # Function to sort the array based on a given header
    @staticmethod
    def ordenar_matriz_decrescente(array, headers):
        print("array =", array)
        print("headers =", headers)

        for index, header_name in enumerate(headers, start=1):
            print(f"{index}. {header_name}")
        print()

        while True:
            try:
                # header_index = int(input("DIGITE O NUMERO DA COLUNA PARA ORDENAMENTO DA TABELA: "))
                header_index = int(3)
                if 1 <= header_index <= len(headers):
                    selected_header = headers[header_index - 1]
                    break
                else:
                    print("Invalid selection. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Sort the array based on the specified header
        sorted_array = sorted(array, key=lambda x: x[header_index - 1], reverse=True)

        return sorted_array








