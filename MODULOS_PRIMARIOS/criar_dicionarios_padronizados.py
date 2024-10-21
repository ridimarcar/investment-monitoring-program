import centralized_imports
from datetime import datetime

# CHAPTER 1: PRELIMINARIES
# ===============================================================================
filepath_base_dados_investimentos = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\base_dados_investimentos.pickle"))
filepath_valores_mensais_padrao = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_padrao.pickle"))
filepath_movimentacoes_mensais_padrao = (
    centralized_imports.Path(r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\movimentacoes_mensais_padrao.pickle"))

# CHAPTER 2: MONTHS AND YEARS LISTS
# ===============================================================================
months_list = [
    "JANEIRO", "FEVEREIRO", "MARCO", "ABRIL",
    "MAIO", "JUNHO", "JULHO", "AGOSTO",
    "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]

# Dictionary to map month names to month numbers
month_name_mapping = {
    "JANEIRO": 1, "FEVEREIRO": 2, "MARCO": 3, "ABRIL": 4,
    "MAIO": 5, "JUNHO": 6, "JULHO": 7, "AGOSTO": 8,
    "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12
}

# Dictionary to map month numbers to month names
month_number_mapping = {1: "JANEIRO", 2: "FEVEREIRO", 3: "MARCO", 4: "ABRIL",
                        5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
                        9: "SETEMBRO",10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"}

years_list = [
    "2020", "2021", "2022", "2023",
    "2024", "2025"
]

# CHAPTER 3: STANDARD DICTIONARIES FIXED PARAMETERS
# ===============================================================================
initial_subkeys = {
    "MERCADO": str,
    "MODALIDADE": str,
    "CODIGO": str,
    "DATA COMPRA": datetime,  # Dates
    "DATA VENCIMENTO": datetime  # Dates
}

# Monthly subkeys, which will be float values
valores_mensais_month_keywords = ["BRUTO", "LIQUIDO"]

# Monthly subkeys, which will be float values
movimentacoes_mensais_month_keywords = ["ENTRADA", "SAIDA"]

# CHAPTER 4: THE criar_dicionarios_padrao FUNCTION
# ===============================================================================

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def criar_dicionarios_padrao(parametros_funcoes):
    print()
    print("-" * 90)
    print("THIS IS THE criar_dicionarios_padrao FUNCTION")

    base_dados_investimentos = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_base_dados_investimentos))

    # Prompt user to select a year
    year = input(f"Select a year from {years_list}: ")

    # Ensure the selected year is valid
    while year not in years_list:
        print("Invalid year selected. Please choose a valid year.")
        year = input(f"Select a year from {years_list}: ")

    selected_year_end = f"{year}-12-31"
    reference_date = centralized_imports.datetime.datetime.strptime(selected_year_end, "%Y-%m-%d").date()

    # Filter investments based on the new criteria
    filtered_investments = [
        inv for inv in base_dados_investimentos
        if inv["DATA COMPRA"] <= reference_date and inv["DATA VENCIMENTO"] > reference_date
    ]

    # Inform the user of the selected investments
    print(f"Selected {len(filtered_investments)} investments with DATA VENCIMENTO <= {selected_year_end}")

    # Define the structure of subkeys and their types (initial subkeys are strings or dates)
    subkeys = {
        "MERCADO": str,
        "MODALIDADE": str,
        "CODIGO": str,
        "DATA COMPRA": centralized_imports.datetime.date,
        "DATA VENCIMENTO": centralized_imports.datetime.date
    }

    # CHAPTER 4: DICTIONARIES STRUCTURES
    # ===============================================================================

    # SECT. 4.1: VALORES MENSAIS
    # -------------------------------------------------------------------------------
    # Define month subkeys explicitly as floats (e.g., BRUTO, LIQUIDO)
    valores_mensais_month_subkeys = {f"{month} {keyword}": 0.0 for month in months_list for keyword in valores_mensais_month_keywords}

    # Create the valores_mensais dictionary structure
    valores_mensais_padrao = {}

    for investment in filtered_investments:
        investment_name = investment["NAME"]
        # Copy the initial subkeys (and their types) and add monthly subkeys (all float type)
        valores_mensais_padrao[investment_name] = {
            subkey: investment[subkey] if subkey in investment else None  # Copy the existing value from investment
            for subkey, subkey_type in subkeys.items()
        }

        # Add the monthly subkeys initialized to 0.0 (treated as floats)
        valores_mensais_padrao[investment_name].update(valores_mensais_month_subkeys)

    # Save the valores_mensais_padrao dictionary
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_valores_mensais_padrao, valores_mensais_padrao)
    print(f"valores_mensais_padrao saved to {filepath_valores_mensais_padrao}")

    # SECT. 4.2: MOVIMENTACOES MENSAIS
    # -------------------------------------------------------------------------------
    # Define month subkeys explicitly as floats (e.g., ENTRADA, SAIDA)
    movimentacoes_mensais_month_subkeys = {f"{month} {keyword}": 0.0 for month in months_list for keyword in movimentacoes_mensais_month_keywords}

    # Create the movimentacoes_mensais dictionary structure
    movimentacoes_mensais_padrao = {}

    for investment in filtered_investments:
        investment_name = investment["NAME"]
        # Copy the initial subkeys (and their types) and add monthly subkeys (all float type)
        movimentacoes_mensais_padrao[investment_name] = {
            subkey: investment[subkey] if subkey in investment else None  # Copy the existing value from investment
            for subkey, subkey_type in subkeys.items()
        }

        # Add the monthly subkeys initialized to 0.0 (treated as floats)
        movimentacoes_mensais_padrao[investment_name].update(movimentacoes_mensais_month_subkeys)

    # Save the movimentacoes_mensais_padrao dictionary
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_movimentacoes_mensais_padrao, movimentacoes_mensais_padrao)
    print(f"movimentacoes_mensais_padrao saved to {filepath_movimentacoes_mensais_padrao}")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def atualizar_dicionario_alvo(dicionario_padrao, dicionario_alvo, caminho_salvar_dicionario):
    """
    Update the target dictionary (dicionario_alvo) based on the standard dictionary (dicionario_padrao).
    If a key or subkey is missing in the target dictionary, it will be added.
    If certain fields ('MERCADO', 'MODALIDADE', 'CODIGO', 'DATA COMPRA', 'DATA VENCIMENTO') do not match,
    they will be updated, and a message will be printed stating the changes.
    """

    # Fields to check for updates
    fields_to_check = ["MERCADO", "MODALIDADE", "CODIGO", "DATA COMPRA", "DATA VENCIMENTO"]

    # Iterate through each main key in the standard dictionary
    for main_key, subkeys_standard in dicionario_padrao.items():

        # If the main key doesn't exist in the target dictionary, add it with all subkeys
        if main_key not in dicionario_alvo:
            # Add the main key and copy all subkeys from the standard dictionary
            dicionario_alvo[main_key] = subkeys_standard.copy()
            print(f"{main_key} added to {dicionario_alvo}")
            # print(f"Added new investment: {main_key}")

        # If the main key already exists in the target dictionary, check its subkeys
        else:
            print(f"Checking existing investment: {main_key}")

            # Check and update specific fields if needed
            for field in fields_to_check:
                if field in subkeys_standard:  # Ensure the field exists in the standard dict
                    # If the field is missing or the values don't match, update the target dict
                    if field not in dicionario_alvo[main_key] or dicionario_alvo[main_key][field] != \
                            subkeys_standard[field]:
                        dicionario_alvo[main_key][field] = subkeys_standard[field]
                        print(f"Updated {field} for {main_key}: {subkeys_standard[field]}")

            # Check if there are any subkeys in the standard dict that are missing in the target dict
            for subkey in subkeys_standard:
                if subkey not in dicionario_alvo[main_key]:
                    dicionario_alvo[main_key][subkey] = subkeys_standard[subkey]
                    print(f"Added missing subkey '{subkey}' to {main_key}")

    print("Target dictionary has been updated.")
    # Optionally save the updated dictionary to disk if needed
    # centralized_imports.arquivos_functions.gravar_arquivo_pickle(caminho_salvar_dicionario, dicionario_alvo)

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(caminho_salvar_dicionario, dicionario_alvo)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_valid_date(prompt):
    """Prompt user for a valid date in YYYY-MM-DD format."""
    while True:
        date_str = input(prompt)
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

# --------------------------------------------------------------------------------
def get_investment_data(investment_name):
    """Prompt the user to input investment details for a specific investment."""
    print(f"\nEntering details for {investment_name}:")

    # Prompt for each value
    mercado = input("Enter MERCADO: ")
    modalidade = input("Enter MODALIDADE: ")
    codigo = input("Enter CODIGO: ")
    data_compra = get_valid_date("Enter DATA COMPRA (YYYY-MM-DD): ")
    data_vencimento = get_valid_date("Enter DATA VENCIMENTO (YYYY-MM-DD): ")

    # Return a dictionary with the investment details
    return {
        "NAME": investment_name,
        "MERCADO": mercado,
        "MODALIDADE": modalidade,
        "CODIGO": codigo,
        "DATA COMPRA": data_compra,
        "DATA VENCIMENTO": data_vencimento
    }

# ---------------------------------------------------------------------
def get_valid_date(prompt):
    """Prompt user for a valid date in YYYY-MM-DD format."""
    while True:
        date_str = input(prompt)
        try:
            return centralized_imports.datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

# ----------------------------------------------------------------------
def investment_exists(investment_name, investment_database):
    """Check if an investment with the given name already exists in the database."""
    for investment in investment_database:
        if investment.get("NAME") == investment_name:
            return True
    return False

# ---------------------------------------------------------------------
def criar_base_dados_investimentos(parametros_funcoes):
    """
    Create or update an investment database by adding missing investments.
    If an investment already exists, it is skipped. You can stop and save the list at any time.
    """

    filepath_base_dados_investimentos = parametros_funcoes.get("filepath_base_dados_investimentos")

    try:
        # Try to load the existing database
        investment_database = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_base_dados_investimentos)

        # If the database is loaded as None, initialize it as an empty list
        if investment_database is None:
            investment_database = []

    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        investment_database = []

    lista_completa_investimentos = centralized_imports.investimentos_btg.InvestimentosBTG.all_investments_list()

    # Helper function to check if an investment already exists
    def investment_exists(investment_name, investment_database):
        for investment in investment_database:
            if investment.get("NAME") == investment_name:
                return True
        return False

    # Loop over each investment name and add only if it's missing
    numero_total_investimentos = len(lista_completa_investimentos)
    for index, investment_name in enumerate(lista_completa_investimentos, start=1):
        print("-" * 90)
        print(investment_name)
        print(f"This is investment #{index} out of {numero_total_investimentos} investments")
        if not investment_exists(investment_name, investment_database):
            print(f"Investment {investment_name} not found in the database. Adding it...")

            # Add the missing investment by prompting the user
            investment_data = get_investment_data(investment_name)
            investment_database.append(investment_data)

            # After adding the missing investment, prompt for continuation
            # should_continue = input("Would you like to continue? (yes to continue, no to save and exit): ").strip().lower()
            should_continue = centralized_imports.general_functions.GeneralFunctions.yes_no("Would you like to continue? (yes to continue, no to save and exit): ")

            if should_continue == 'no':
                print("Saving progress to disk...")
                centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_base_dados_investimentos, investment_database)
                print(f"Progress saved to {filepath_base_dados_investimentos}. You can resume later.")
                break
    else:
        # Save the updated investment database if the loop completes without stopping
        print("Saving all updates to disk...")
        centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_base_dados_investimentos, investment_database)
        print(f"All investments have been saved to {filepath_base_dados_investimentos}.")







