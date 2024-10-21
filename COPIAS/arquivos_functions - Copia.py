# MEUS MODULOS DE PROGRAMACAO REUTILIZAVEIS
# ===========================================================================
import centralized_imports

# ----------------------------------------------------------------
yes = ("y", "yes", "s", "sim")

def display_keys(dictionary, indent=0):
    for key, value in dictionary.items():
        print(" " * indent + str(key))
        if isinstance(value, dict):
            display_keys(value, indent + 4)
        elif isinstance(value, centralized_imports.np.ndarray):
            print(" " * (indent + 4) + "Array shape:", value.shape)
            # Add any additional handling for NumPy arrays here

# ----------------------------------------------------------------
class ArquivosFunctions:

    # ............................................................
    @staticmethod
    def editar_dicionario(filepath_pickle):
        # Load pickle file
        arquivo_pickle_restaurado = ArquivosFunctions.abrir_arquivo_pickle(filepath_pickle)
        # Create a deep copy for editing
        copia_profunda = centralized_imports.copy.deepcopy(arquivo_pickle_restaurado)
        # Choose editing action
        while True:
            print("\nChoose an action:")
            print("1. Delete a key")
            print("2. Add a new key-value pair")
            print("3. Update an existing key's value")
            print("4. Exit")

            choice = input("Enter the number of your choice: ")

            if choice == '1':
                ArquivosFunctions.apagar_chave_dicionario(filepath_pickle)
            elif choice == '2':
                ArquivosFunctions.acrescentar_chave_dicionario(filepath_pickle)
            elif choice == '3':
                pass
            elif choice == '4':
                print("Exiting.")
                break
            else:
                print("Invalid choice, please try again.")

    # ............................................................
    @staticmethod
    def load_config(filepath_config_json):
        with open(filepath_config_json, 'r') as file:
            return centralized_imports.json.load(file)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    def abrir_arquivo_pickle(filepath_arquivo_pickle):
        try:
            with open(filepath_arquivo_pickle, "rb") as file:
                data = centralized_imports.pickle.load(file)
            print(f"Data loaded successfully from {filepath_arquivo_pickle}")
            return data
        except Exception as e:
            print(f"Error loading data from {filepath_arquivo_pickle}: {e}")
            return None


    # Function #2: Exibir arquivo pickle
    # --------------------------------------------------------------------
    @staticmethod
    def exibir_arquivo_pickle(filepath_pickle):
        print()
        print("This is the exibir_arquivo_pickle function.")

        centralized_imports.general_functions.GeneralFunctions.mostrar_tabela_pickle(filepath_pickle)


    # Function #3: Gravar arquivo pickle
    # --------------------------------------------------------------------
    @staticmethod
    def gravar_arquivo_pickle(caminho_arquivo, arquivo_pickle_restaurado):
        print()
        print("THIS IS THE gravar_arquivo_pickle FUNCTION.")
        with open(caminho_arquivo, "wb") as file:
            centralized_imports.pickle.dump(arquivo_pickle_restaurado, file)
        print("Modification(s) added to file.File saved to disk at the address:")
        print(f"{caminho_arquivo}")

    # Function #4: Gravar arquivo seguranca
    # --------------------------------------------------------------------
    def gravar_arquivo_seguranca(caminho_arquivo):
        print()
        print("THIS IS THE gravar_arquivo_seguranca FUNCTION.")
        # No need to load the data, we only need the file path
        # Open the original file in binary read mode
        with open(caminho_arquivo, 'rb') as original_file:
            pass  # Empty pass as we don't need to read the data
        # Create a backup filename with ".backup" extension
        backup_filename = caminho_arquivo + ".backup"
        # Use shutil.copy2 to preserve creation and modification times
        shutil.copy2(caminho_arquivo, backup_filename)
        print("Backup copy created:", backup_filename)

    # Function #5: Exibir arquivo de seguranca
    # --------------------------------------------------------------------
    def exibir_arquivo_seguranca(caminho_arquivo_seguranca):

        # Define the available options as a list
        options = ['Criar arquivo valores mensais',
                   'Criar arquivo movimentacoes mensais',
                   'Criar arquivo saldos anuais',
                   'Criar arquivo rentabilidade']

        # Generate the input prompt dynamically based on the available options
        prompt = f"Please select one of the following options:\n"
        for index, option in enumerate(options, start=1):
            prompt += f"{index}. {option}\n"
        prompt += "Enter the number corresponding to your choice: "

        # Prompt the user to select a choice
        user_choice_index = input(prompt)

        # Perform actions based on the user's choice
        if user_choice_index.isdigit():
            user_choice_index = int(user_choice_index)
            if 1 <= user_choice_index <= len(options):
                selected_option = options[user_choice_index - 1]
                print(f"You selected {selected_option}.")

                if selected_option == 'Criar arquivo valores mensais':
                    arquivo = investimentos_btg.valores_mensais_2025
                    with open(caminho_valores, 'wb') as file:
                        pickle.dump(arquivo, file)
                elif selected_option == 'Criar arquivo movimentacoes mensais':
                    arquivo = investimentos_functions.InvestimentosFunctions.gerar_dicionario_movimentacoes()
                    with open(caminho_movimentacoes, 'wb') as file:
                        pickle.dump(arquivo, file)
                elif selected_option == 'Criar arquivo saldos anuais':
                    arquivo = investimentos_functions.InvestimentosFunctions.gerar_dicionario_saldos()
                    with open(caminho_saldos, 'wb') as file:
                        pickle.dump(arquivo, file)
                elif selected_option == 'Criar arquivo rentabilidade':
                    arquivo = investimentos_functions.InvestimentosFunctions.gerar_dicionario_rentabilidade()
                    with open(caminho_saldos, 'wb') as file:
                        pickle.dump(arquivo, file)
            else:
                print("Invalid choice. Please enter a number within the range of available options.")
        else:
            print("Invalid input. Please enter a number.")

        print("New pickle file has been created and saved to disk.")

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("'Exibir arquivo de seguranca' was selected")

        with open(caminho_arquivo_seguranca, 'rb') as file:
            data = pickle.load(file)

        data_flat = []
        for key, value in data.items():
            row = {'Investment': key}
            row.update(value)
            data_flat.append(row)

        # Create DataFrame
        df = pd.DataFrame(data_flat)

        # My DataFrame
        data = df[['Investment', 'MERCADO', 'MODALIDADE', 'CODIGO', 'DATA COMPRA', 'DATA VENCIMENTO',
                   'JANEIRO BRUTO', 'JANEIRO LIQUIDO']]

        # Convert DataFrame to a tabular format with borders
        table = tabulate(data, headers='keys', tablefmt='fancy_grid')

        # Print the tabulated data
        print(table)






