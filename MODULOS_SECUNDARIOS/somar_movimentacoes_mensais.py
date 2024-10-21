import centralized_imports

def somar_movimentacoes_mensais(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE somar_movimentacoes_mensais FUNCTION.")
    print()

    # --------------------------------------------------------
    # Set up parameters
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")
    month_saida_key = parametros_funcoes.get("month_saida_key")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    months_list = centralized_imports.investimentos_btg.months_list
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # year_interest = int(year_month_interest_end.split("-")[0])
    # month_interest = int(year_month_interest_end.split("-")[1])
    year_interest = year_month_interest_end.year
    month_interest = year_month_interest_end.month
    # Restrict valid months up to year_month_interest_end
    valid_months = months_list[:month_interest]
    # year_interest_str = str(year_interest)

    # Set locale for Brazilian currency format
    centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')

    # Check expected numerical entries are really floats
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_movimentacoes_mensais)

    # --------------------------------------------------------
    # Load files
    try:
        movimentacoes_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_movimentacoes_mensais)
        if movimentacoes_mensais is None or not isinstance(movimentacoes_mensais, dict) or not movimentacoes_mensais:
            print("Invalid or empty movimentacoes_mensais.")
    except Exception as e:
        print(f"An error occurred while loading movimentacoes_mensais: {e}")

    # --------------------------------------------------------
    # Initialize total variables for the month
    month_total_entrada = 0
    month_total_saida = 0

    # Initialize totals for the month by MERCADO and MODALIDADE
    mercado_totals = {}
    modalidade_totals = {}
    investimento_totals = {}

    # Ensure 'TOTAL' key exists
    movimentacoes_mensais.setdefault('TOTAL', {month_entrada_key: 0, month_saida_key: 0})
    # Reset them in case they already exist
    movimentacoes_mensais["TOTAL"][month_entrada_key] = 0
    movimentacoes_mensais["TOTAL"][month_saida_key] = 0

    # Iterate over the items in movimentacoes_mensais
    for investimento, movimentacoes in movimentacoes_mensais.items():
        # If the current investment is in the skip list, skip to the next iteration
        if investimento in skip_investment_list:
            continue

        print("-" * 80)
        print(f"Processing investment: {investimento}")

        soma_entrada = sum(value for key, value in movimentacoes.items()
                           if "ENTRADA" in key and any(month in key for month in valid_months))
        soma_saida = sum(value for key, value in movimentacoes.items()
                         if "SAIDA" in key and any(month in key for month in valid_months))

        investimento_totals[investimento] = {
            "ENTRADA": soma_entrada,
            "SAIDA": soma_saida
        }

        # print(f"Total ENTRADA for {investimento}: {soma_entrada}")
        # print(f"Total SAIDA for {investimento}: {soma_saida}")
        print(f"Total ENTRADA: {soma_entrada}")
        print(f"Total SAIDA: {soma_saida}")

        mercado = movimentacoes.get('MERCADO', 'UNKNOWN')
        modalidade = movimentacoes.get('MODALIDADE', 'UNKNOWN')

        # Initialize nested dictionaries for mercado and modalidade
        mercado_totals.setdefault(mercado, {month_entrada_key: 0, month_saida_key: 0})
        modalidade_totals.setdefault(modalidade, {month_entrada_key: 0, month_saida_key: 0})

        # Sum entrada and saida for valid months
        if month_entrada_key in movimentacoes:
            entrada = float(movimentacoes.get(month_entrada_key, 0))
            month_total_entrada += entrada
            mercado_totals[mercado][month_entrada_key] += entrada
            modalidade_totals[modalidade][month_entrada_key] += entrada

        if month_saida_key in movimentacoes:
            saida = float(movimentacoes.get(month_saida_key, 0))
            month_total_saida += saida
            mercado_totals[mercado][month_saida_key] += saida
            modalidade_totals[modalidade][month_saida_key] += saida

        # Save summations for each mercado and modalidade
        movimentacoes_mensais["TOTAL"][month_entrada_key] = month_total_entrada
        movimentacoes_mensais["TOTAL"][month_saida_key] = month_total_saida

        for mercado, totals in mercado_totals.items():
            movimentacoes_mensais.setdefault(mercado, {}).update(totals)

        for modalidade, totals in modalidade_totals.items():
            movimentacoes_mensais.setdefault(modalidade, {}).update(totals)

        # Remove unwanted main keys
        for key in ["MERCADO", "MODALIDADE", "UNKNOWN", ""]:
            movimentacoes_mensais.pop(key, None)

    # Save the updated movimentacoes_mensais
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_movimentacoes_mensais,
        movimentacoes_mensais)

    # Display the updated file
    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(
        filepath_movimentacoes_mensais)


