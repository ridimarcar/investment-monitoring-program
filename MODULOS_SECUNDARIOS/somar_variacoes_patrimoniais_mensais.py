import centralized_imports

def somar_variacoes_patrimoniais_mensais(parametros_funcoes):
    print("THIS IS THE somar_variacoes_patrimoniais_mensais FUNCTION.")

    # year_interest = parametros_funcoes.get("year_interest")
    month_interest = parametros_funcoes.get("month_interest")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    # month_entrada_key = parametros_funcoes.get("month_entrada_key")
    # month_saida_key = parametros_funcoes.get("month_saida_key")
    filepath_variacoes_patrimoniais_mensais = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")

    months_list = centralized_imports.investimentos_btg.months_list
    # year_interest = int(year_month_interest_end.split("-")[0])
    # month_interest = int(year_month_interest_end.split("-")[1])
    year_interest = year_month_interest_end.year
    month_interest_numeric = year_month_interest_end.month
    valid_months = months_list[:month_interest_numeric]  # Restrict valid months up to year_month_interest_end

    # year_interest_str = str(year_interest)

    # Set locale for Brazilian currency format
    centralized_imports.locale.setlocale(
        centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')

    # Check expected numerical entries are really floats
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(
        filepath_variacoes_patrimoniais_mensais)

    # Load file
    variacoes_patrimoniais_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_variacoes_patrimoniais_mensais))

    # Initialize total variables for the month
    # month_total_entrada = 0
    # month_total_saida = 0
    month_total = 0

    # Initialize totals for the month by MERCADO and MODALIDADE
    mercado_totals = {}
    modalidade_totals = {}
    investimento_totals = {}

    # Ensure 'TOTAL' key exists
    variacoes_patrimoniais_mensais.setdefault('TOTAL', {month_interest: 0, month_interest: 0})

    # Fetch skip_investment_list
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Iterate over the items in variacoes_patrimoniais_mensais
    for investimento, variacoes in variacoes_patrimoniais_mensais.items():
        # If the current investment is in the skip list, skip to the next iteration
        if investimento in skip_investment_list:
            continue

        print("-" * 80)
        print(f"Processing investment: {investimento}")

        soma_investimento = sum(value for key, value in variacoes.items()
                           if month_interest in key and any(month in key for month in valid_months))

        investimento_totals[investimento] = {soma_investimento}

        print(f"Variacao patrimonial for {investimento}: {soma_investimento}")

        mercado = variacoes.get('MERCADO', 'UNKNOWN')
        modalidade = variacoes.get('MODALIDADE', 'UNKNOWN')

        # Initialize nested dictionaries for mercado and modalidade
        mercado_totals.setdefault(mercado, {month_interest: 0})
        modalidade_totals.setdefault(modalidade, {month_interest: 0})

        # Sum entrada and saida for valid months
        if month_interest in variacoes:
            variacao_patrimonial = float(variacoes.get(month_interest, 0))
            month_total += variacao_patrimonial
            mercado_totals[mercado][month_interest] += variacao_patrimonial
            modalidade_totals[modalidade][month_interest] += variacao_patrimonial

        # Save summations for each mercado and modalidade
        variacoes_patrimoniais_mensais["TOTAL"][month_interest] = month_total

        for mercado, totals in mercado_totals.items():
            variacoes_patrimoniais_mensais.setdefault(mercado, {}).update(totals)

        for modalidade, totals in modalidade_totals.items():
            variacoes_patrimoniais_mensais.setdefault(modalidade, {}).update(totals)

        # Remove unwanted main keys
        for key in ["MERCADO", "MODALIDADE", "UNKNOWN", ""]:
            variacoes_patrimoniais_mensais.pop(key, None)

    # Save the updated variacoes_patrimoniais_mensais
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_variacoes_patrimoniais_mensais,
        variacoes_patrimoniais_mensais)

    # Display the updated file
    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(
        filepath_variacoes_patrimoniais_mensais)

