# MEUS MODULOS DE PROGRAMACAO REUTILIZAVEIS
# ===========================================================================
import centralized_imports

investments_actions_list = [
    "Apagar investimento",
    "Acrescentar investimento ou subchave",
    "Modificar investimento",
    "Sair"
]


# ---------------------------------------------------------------------------
class InvestimentosFunctions:

    @staticmethod
    def reduzir_dicionario_temporalmente(dicionario, parametros_funcoes):
        print("&" * 90)
        print("THIS IS THE reduzir_dicionario_temporalmente FUNCTION")
        year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

        time_reduced_dict = centralized_imports.copy.deepcopy(dicionario)

        for investment, value in dicionario.items():
            # print(f"{investment} -> {value}")
            try:
                data_compra = value["DATA COMPRA"]
                # print(f"data_compra for {investment} =", data_compra)
            except KeyError:
                print(f"KeyError: 'DATA COMPRA' not found for investment {investment}. Moving on...")
                continue

            # Check if data_compra is empty
            if not data_compra:
                print(f"Warning: 'DATA COMPRA' is empty for investment '{investment}'. Skipping this investment.")
                continue

            # Ensure that both data_compra and year_month_interest_end are datetime objects
            if isinstance(data_compra, str):
                try:
                    data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, "%Y-%m-%d").date()
                except ValueError:
                    print(f"Invalid date format for investment '{investment}': {data_compra}")
                    continue
            else:
                data_compra_date = data_compra  # Assuming it's already a datetime.date object

            if data_compra_date > year_month_interest_end:
                del time_reduced_dict[investment]  # Delete investments that are after the end date

        return time_reduced_dict

    @staticmethod
    def criar_dicionario_reduzido(dicionario, parametros_funcoes):
        pass
        # print("-" * 90)
        # print("THIS IS THE criar_dicionario_reduzido FUNCTION")
        # year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

        # time_reduced_dict = {}
        #
        # for investment, data in dicionario.items():
        #     data_compra = data.get("DATA COMPRA")
            # print("data_compra = ", data_compra)
            # data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()

            # Ensure that both data_compra and year_month_interest_end are datetime objects
            # if isinstance(data_compra, str):
            #     try:
            #         data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, "%Y-%m-%d").date()
            #     except ValueError:
            #         print(f"Invalid date format for investment '{investment}': {data_compra}")
            #         continue

            # if data_compra_date > year_month_interest_end:
            #     continue

            # # Initialize the sub-dictionary for the investment
            # time_reduced_dict[investment] = {}

            # Get original data for the investment
        #     rentabilidade_total = data.get("RENTABILIDADE TOTAL")
        #     rentabilidade_anual_media = data.get("RENTABILIDADE ANUAL MEDIA")
        #     rentabilidade_mensal_media = data.get("RENTABILIDADE MENSAL MEDIA")
        #     representatividade = data.get("REPRESENTATIVIDADE")
        #
        #     # Save data to time_reduced_dict
        #     time_reduced_dict[investment]["RENTABILIDADE TOTAL"] = rentabilidade_total
        #     time_reduced_dict[investment]["RENTABILIDADE ANUAL MEDIA"] = rentabilidade_anual_media
        #     time_reduced_dict[investment]["RENTABILIDADE MENSAL MEDIA"] = rentabilidade_mensal_media
        #     time_reduced_dict[investment]["REPRESENTATIVIDADE"] = representatividade
        #
        # return time_reduced_dict

    # ...........................................................................
    @staticmethod
    def acrescentar_investimento_subchave(filepath_pickle):
        # Carregar arquivo
        arquivo_pickle_restaurado = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle))

        # Import here to avoid circular import issues
        from centralized_imports.general_functions import yes_list

        while True:
            # Exibir dicionário
            centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_pickle)

            # Ask user if they want to add a main key or a subkey
            action = input("Do you want to add a main key or a subkey? (main/subkey): ").strip().lower()

            if action == 'main':
                # Inserir nova chave principal
                new_main_key = input("Enter new main key: ").upper()
                new_value = input("Enter new value for the new main key: ")
                arquivo_pickle_restaurado[new_main_key] = new_value

            elif action == 'subkey':
                # Ask user for the main key to which the subkey will be added
                main_key = input("Enter the main key to which you want to add a subkey: ").upper()
                if main_key in arquivo_pickle_restaurado and isinstance(arquivo_pickle_restaurado[main_key], dict):
                    # Insert new subkey
                    new_subkey = input("Enter new subkey: ").upper()
                    new_subvalue = input("Enter new value for the new subkey: ")
                    arquivo_pickle_restaurado[main_key][new_subkey] = new_subvalue
                else:
                    print(f"Main key '{main_key}' not found or is not a dictionary.")

            else:
                print("Invalid option. Please choose 'main' or 'subkey'.")

            centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_pickle, arquivo_pickle_restaurado)

            # Perguntar ao usuário se deseja adicionar outra chave ou subchave
            texto = "Do you want to add another key or subkey? (yes/no): "
            add_another = centralized_imports.general_functions.GeneralFunctions.yes_no(texto)
            # add_another = input("Do you want to add another key or subkey? (yes/no): ").strip().lower()
            if add_another not in centralized_imports.general_functions.yes_list:
                break

        # Gravar arquivo
        centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_pickle, arquivo_pickle_restaurado)
        # Exibir dicionário modificado
        centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_pickle)

    # ...........................................................................
    @staticmethod
    def apagar_investimento(filepath_pickle):
        # Carregar arquivo
        arquivo_pickle_restaurado = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle))

        while True:
            # Exibir dicionário
            centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_pickle)

            # Escolher chave a ser apagada
            key_to_delete = input("Enter key to delete: ").upper()
            del arquivo_pickle_restaurado[key_to_delete]

            # Gravar arquivo
            centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_pickle,
                                                                                           arquivo_pickle_restaurado)
            # Perguntar ao usuário se deseja adicionar outra chave
            texto = "Do you want to delete another main key? (yes/no): "
            add_another = centralized_imports.general_functions.GeneralFunctions.yes_no()
            if add_another not in centralized_imports.general_functions.yes_list:
                break


        # Exibir dicionário modificado
        centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_pickle)

    # ...........................................................................
    @staticmethod
    def modificar_investimento(filepath_pickle):
        # Carregar arquivo
        arquivo_pickle_restaurado = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle))

        while True:
            # Display investment options
            investment_keys = list(arquivo_pickle_restaurado.keys())
            selected_investment_key = centralized_imports.general_functions.GeneralFunctions.escolher_opcao_lista(
                investment_keys)

            if selected_investment_key not in arquivo_pickle_restaurado:
                print("Selected investment does not exist.")
                continue

            selected_investment = arquivo_pickle_restaurado[selected_investment_key]

            while True:
                # Display nested key-value pairs for the selected investment
                print(f"Editing investment: {selected_investment_key}")
                if isinstance(selected_investment, dict):
                    for key, value in selected_investment.items():
                        print(f"{key}: {value}")
                else:
                    print("Selected investment data is not a dictionary.")

                key_to_edit = input("Enter the key you want to edit (or 'exit' to stop): ")
                if key_to_edit.lower() == 'exit':
                    break

                if key_to_edit in selected_investment:
                    # Check if the key contains the words "ENTRADA", "SAIDA", "BRUTO", or "LIQUIDO"
                    if any(word in key_to_edit.upper() for word in ['ENTRADA', 'SAIDA', 'BRUTO', 'LIQUIDO']):
                        # Ask for the new value and cast it to float
                        while True:
                            try:
                                new_value = float(input(f"Enter the new numeric value (float) for {key_to_edit}: "))
                                break
                            except ValueError:
                                print("Invalid input. Please enter a valid float.")
                    else:
                        # If the key does not match, treat it as a regular string input
                        new_value = input(f"Enter the new value for {key_to_edit}: ")

                    # Update the selected investment's key with the new value
                    selected_investment[key_to_edit] = new_value

                    # Save changes to the file
                    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
                        filepath_pickle, arquivo_pickle_restaurado)

                else:
                    print("Key not found. Please try again.")

                # Ask the user whether they want to edit another key:value pair
                another_edit = input("Do you want to edit another key:value pair? (y/n): ")
                if another_edit.lower() != 'y':
                    break

            # Ask if the user wants to edit another investment
            another_investment = input("Do you want to edit another investment? (y/n): ")
            if another_investment.lower() != 'y':
                break

    # @staticmethod
    # def modificar_investimento(filepath_pickle):
    #     # Carregar arquivo
    #     arquivo_pickle_restaurado = (
    #         centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle))
    #
    #     while True:
    #         # Display investment options
    #         investment_keys = list(arquivo_pickle_restaurado.keys())
    #         selected_investment_key = centralized_imports.general_functions.GeneralFunctions.escolher_opcao_lista(
    #             investment_keys)
    #
    #         if selected_investment_key not in arquivo_pickle_restaurado:
    #             print("Selected investment does not exist.")
    #             continue
    #
    #         selected_investment = arquivo_pickle_restaurado[selected_investment_key]
    #
    #         while True:
    #             # Display nested key-value pairs for the selected investment
    #             print(f"Editing investment: {selected_investment_key}")
    #             if isinstance(selected_investment, dict):
    #                 for key, value in selected_investment.items():
    #                     print(f"{key}: {value}")
    #             else:
    #                 print("Selected investment data is not a dictionary.")
    #
    #             key_to_edit = input("Enter the key you want to edit (or 'exit' to stop): ")
    #             if key_to_edit.lower() == 'exit':
    #                 break
    #
    #             if key_to_edit in selected_investment:
    #                 new_value = input(f"Enter the new value for {key_to_edit}: ")
    #                 selected_investment[key_to_edit] = new_value
    #             else:
    #                 print("Key not found. Please try again.")
    #
    #             # Save changes to the file
    #             centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_pickle,
    #                                                                                            arquivo_pickle_restaurado)
    #
    #             # Ask the user whether they want to edit another key:value pair
    #             another_edit = input("Do you want to edit another key:value pair? (y/n): ")
    #             if another_edit.lower() != 'y':
    #                 break
    #
    #         # Ask if the user wants to edit another investment
    #         another_investment = input("Do you want to edit another investment? (y/n): ")
    #         if another_investment.lower() != 'y':
    #             break


    # ...........................................................................
    @staticmethod
    def preencher_entradas_vazias():
        print("THIS IS THE preencher_entradas_vazias FUNCTION.")

        # FIRST PART: SELECT A FILEPATH
        print("FIRST PART: SELECT A FILEPATH")
        print("&" * 90)

        filepaths_list = centralized_imports.investimentos_btg.filepaths_list
        caminho_arquivo = centralized_imports.general_functions.GeneralFunctions.escolher_opcao_lista(filepaths_list)

        # SECOND PART: LOAD THE FILE
        print("SECOND PART: LOAD THE FILE")
        print("&" * 90)

        arquivo_pickle_restaurado = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            caminho_arquivo)

        # THIRD PART: FILL EMPTY ENTRIES WITH ZERO
        print("THIRD PART: FILL EMPTY ENTRIES WITH ZERO")
        print("&" * 90)

        keywords = ["ENTRADA", "SAIDA", "BRUTO", "LIQUIDO", "TOTAL"]
        for investment, details in arquivo_pickle_restaurado.items():
            for key in details:
                if any(keyword in key for keyword in keywords) and (details[key] == "" or (
                        isinstance(details[key], float) and centralized_imports.np.isnan(details[key]))):
                    details[key] = 0.0
                    print(f"Updated {investment} - {key} to 0.0")

        # FOURTH PART: SAVE THE MODIFIED FILE
        print("FOURTH PART: SAVE THE MODIFIED FILE")
        print("&" * 90)

        centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(caminho_arquivo,
                                                                                       arquivo_pickle_restaurado)
        print(f"Arquivo atualizado e salvo em {caminho_arquivo}")

        # Display modified file
        centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(caminho_arquivo)

    # Function #1: Select Mercado and Modalidade
    # --------------------------------------------------------------------
    @staticmethod
    def selecionar_mercado_modalidade(config=None):
        # ------------------------------------------------------------
        print()
        print("&" * 90)
        print("THIS IS THE selecionar_mercado_modadalidade FUNCTION")
        print()

        input_mode = config.get("input_mode", "manual") if config else "manual"

        if input_mode == "automatic":
            mercado = config.get("mercado")
            modalidade = config.get("modalidade")
            return mercado, modalidade
        else:
            # Mercado selection
            print("Select MERCADO:", end='\n')
            for i, item in enumerate(centralized_imports.investimentos_btg.mercados_list):
                print(f"{i + 1}. {item}")
            # Convert input to integer and check if it's valid
            print()
            mercado_index = int(input("Enter MERCADO: ")) - 1
            # Access the corresponding word expression using the index
            mercado = centralized_imports.investimentos_btg.mercados_list[mercado_index]
            print("Mercado = ", mercado)

            # ------------------------------------------------------------
            # Modalidade selection with automatic assignment for COE and FUNDOS DE INVESTIMENTO
            if mercado == "COE":
                modalidade = "COE"
            elif mercado == "FUNDOS DE INVESTIMENTO":
                modalidade = "FUNDOS DE INVESTIMENTO"
            else:
                # Filter modalidades based on selected mercado
                if mercado == "RENDA FIXA":
                    modalidades_to_show = centralized_imports.investimentos_btg.modalidadesRF
                elif mercado == "RENDA VARIAVEL":
                    modalidades_to_show = centralized_imports.investimentos_btg.modalidadesRV
                else:
                    modalidades_to_show = centralized_imports.investimentos_btg.modalidades_list  # Show all modalities otherwise

                print()
                print("Select MODALIDADE:")
                for i, item in enumerate(modalidades_to_show):
                    print(f"{i + 1}. {item}")
                # Convert input to integer and check if it's valid
                print()
                modalidade_index = int(input("Enter MODALIDADE: ")) - 1
                # Access the corresponding word expression using the index
                modalidade = modalidades_to_show[modalidade_index]

            print("Modalidade = ", modalidade)

            return mercado, modalidade

    # Function #3: Editar investimentos
    # --------------------------------------------------------------------
    @staticmethod
    def editar_investimentos():

        # Import here to avoid circular import issues
        yes_list = centralized_imports.general_functions.yes_list

        while True:
            print()
            print("&" * 90)
            print("THIS IS THE editar_investimentos FUNCTION.")

            # FIRST PART: LOADING AND DISPLAYING SELECTED FILE
            # ===================================================================
            filepaths_list = centralized_imports.investimentos_btg.filepaths_list
            # Select file to be edited
            print()
            print("Lista dos arquivos disponíveis para edição:")
            caminho_arquivo = centralized_imports.general_functions.GeneralFunctions.escolher_opcao_lista(
                filepaths_list)
            # Load file
            arquivo_pickle_restaurado = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                caminho_arquivo)
            # Display the original file
            centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(caminho_arquivo)

            # SECOND PART: SELECTING EDITING ACTION
            # ===================================================================
            while True:
                selected_editing_action = (
                    centralized_imports.general_functions.GeneralFunctions.escolher_opcao_lista(investments_actions_list))
                print("selected_editing_action = ", selected_editing_action)

                if selected_editing_action == 'Apagar investimento':
                    InvestimentosFunctions.apagar_investimento(caminho_arquivo)
                elif selected_editing_action == 'Acrescentar investimento ou subchave':
                    InvestimentosFunctions.acrescentar_investimento_subchave(caminho_arquivo)
                elif selected_editing_action == 'Modificar investimento':
                    InvestimentosFunctions.modificar_investimento(caminho_arquivo)
                elif selected_editing_action == 'Sair':
                    print("Exiting.")
                    break
                else:
                    print("Invalid selected_editing_action, please try again.")

            another_file = input("Do you want to upload another file for editing? (y/n): ")
            if another_file.lower() != 'y':
                break

    # Function #5: Calcular somas parciais CHATGPT
    # --------------------------------------------------------------------
    # Function to sum all entries under a particular sub-key
    def sum_entries(data, category, sub_key):
        total = 0
        if category in data and sub_key in data[category]:
            total += sum(data[category][sub_key].values())
        return total

    # ----------------------------------------------------------------------------
    # Function #6 Apagar chaves do dicionario
    # --------------------------------------------------------------------
    @staticmethod
    def apagar_chaves_dicionario(pickle_filepath):
        try:
            # Step 1: Open and read the pickle file
            with open(pickle_filepath, 'rb') as file:
                investments = centralized_imports.pickle.load(file)

            while True:
                # List all main keys (investment names)
                print("\nInvestments available for editing:")
                investment_names = list(investments.keys())
                for index, name in enumerate(investment_names):
                    print(f"{index + 1}. {name}")

                # List all nested keys to help the user select one to delete
                all_keys = set()
                for investment in investments.values():
                    all_keys.update(investment.keys())

                print("\nKeys available for deletion:")
                all_keys = list(all_keys)
                for index, key in enumerate(all_keys):
                    print(f"{index + 1}. {key}")

                try:
                    key_choice = int(input("Enter the number of the key you want to delete: ")) - 1
                    if key_choice < 0 or key_choice >= len(all_keys):
                        print("Invalid choice. Please try again.")
                        continue

                    key_to_delete = all_keys[key_choice]
                    print(f"Selected key to delete: {key_to_delete}")

                    # Step 3: Delete the key:value pairs throughout the dictionary
                    for investment in investments.values():
                        if key_to_delete in investment:
                            del investment[key_to_delete]
                    print(f"Deleted key '{key_to_delete}' from all investments.")

                    another_key = input("Do you want to delete another key? (y/n): ")
                    if another_key.lower() != 'y':
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            # Step 5: Save the updated investments dictionary back to the pickle file
            with open(pickle_filepath, 'wb') as file:
                centralized_imports.pickle.dump(investments, file)
            print(f"Updated investments saved to {pickle_filepath}")

        except Exception as e:
            print(f"An error occurred: {e}")
