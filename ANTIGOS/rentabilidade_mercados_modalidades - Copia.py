import centralized_imports

def atualizar_rentabilidade_mercados_modalidades(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE atualizar_rentabilidade_mercados_modalidades FUNCTION.")

    # FIRST PART: LOADING RELEVANT PARAMETERS AND FILES
    # ===================================================================
    print()
    print("FIRST PART: LOADING RELEVANT FILES")
    print("=" * 90)

    year_interest = parametros_funcoes.get("year_interest")
    year_entrada_key = parametros_funcoes.get("year_entrada_key")
    year_saida_key = parametros_funcoes.get("year_saida_key")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_rentabilidade_mercados_modalidades = parametros_funcoes.get("filepath_rentabilidade_mercados_modalidades")

    # print()
    print("year_interest = ", year_interest)
    print("year_entrada_key = ", year_entrada_key)
    print("year_saida_key = ", year_saida_key)
    print("month_bruto_key = ", month_bruto_key)
    print("month_liquido_key = ", month_liquido_key)
    print("year_month_interest_start = ", year_month_interest_start)
    print("year_month_interest_end = ", year_month_interest_end)
    print("filepath_movimentacoes_mensais = ", filepath_movimentacoes_mensais)
    print("filepath_movimentacoes_anuais = ", filepath_movimentacoes_anuais)
    print("filepath_rentabilidade_representatividade = ", filepath_rentabilidade_representatividade)
    print("filepath_rentabilidade_mercados_modalidades = ", filepath_rentabilidade_mercados_modalidades)
    print()

    # Convert year_interest to string
    year_interest_str = str(year_interest)
    # Load the first input pickle file (valores_mensais_ano)
    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    # Load the third input pickle file (movimentacoes_mensais_ano)
    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    # Load the third input pickle file (movimentacoes_anuais)
    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))
    print()
    for key, value in movimentacoes_anuais.items():
        print(f"{key} -> {value}")

    try:
        rentabilidade_mercados_modalidades = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_rentabilidade_mercados_modalidades))
    except FileNotFoundError:
        rentabilidade_mercados_modalidades = {}

    # SECOND PART: YEAR AND MONTH OF INTEREST / KEYWORDS SETUP
    # ===================================================================
    print()
    print("SECOND PART: YEAR AND MONTH OF INTEREST / KEYWORDS SETUP")
    print("=" * 90)

    # Assuming the keys exist, proceed to retrieve the values
    patrimonio_bruto = valores_mensais["TOTAL"][month_bruto_key]
    patrimonio_liquido = valores_mensais["TOTAL"][month_liquido_key]
    # print()
    print("patrimonio_bruto = R${:,.2f}".format(patrimonio_bruto))
    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))

    # THIRD PART: PROFITABILITY CALCULATIONS FOR INDIVIDUAL MERCADOS
    # ===============================================================================================
    print()
    print("THIRD PART: CALCULO DA RENTABILIDADE PARA CADA MERCADO ATE A DATA DE INTERESSE")
    print("=" * 95)
    contador_investimentos = 0
    soma_representatividade = 0
    for investment, details in movimentacoes_mensais.items():
        for investment, details in movimentacoes_mensais.items():
            if (investment not in centralized_imports.investimentos_btg.mercados_list or
                    investment not in centralized_imports.investimentos_btg.modalidades_list):
                continue
            # Proceed with the normal processing for investments that are in both lists

        print("-" * 95)
        contador_investimentos += 1
        print("Investment = ", investment)
        print(f"This is investment #{contador_investimentos} out of {len(movimentacoes_mensais.items())} investments")
        data_compra = details.get('DATA COMPRA')
        data_vencimento = details.get('DATA VENCIMENTO')
        print("data_compra = ", data_compra)
        print("data_vencimento = ", data_vencimento, end='\n')

        if not data_compra or not data_vencimento:
            print(f"Warning: 'DATA COMPRA' or 'DATA VENCIMENTO' is blank for investment {investment}. Skipping...")
            continue

        # Convert dates to datetime.date objects
        data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
        data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()

        # CASO CEDO DEMAIS PARA INVESTIMENTO ESTAR AQUI
        if data_compra_date > year_month_interest_end:
            print(f"Warning: It is too early for {investment} to be here. Skipping...")
            continue

        # CASO APLICACAO VENCIDA
        if year_month_interest_end > data_vencimento_date:
            print("APLICACAO JA VENCIDA")
            if investment not in rentabilidade_mercados_modalidades.keys():
                rentabilidade_mercados_modalidades[investment] = {}
            rentabilidade_mercados_modalidades[investment]['SALDO ATUAL'] = 0
            print("movimentacoes_anuais saida = ", movimentacoes_anuais[investment][year_interest_str]['SAIDA'])
            print("movimentacoes_anuais entrada = ", movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
            rentabilidade_mercados_modalidades[investment]['GANHOS EFETIVOS'] = (
                movimentacoes_anuais[investment][year_interest_str]['SAIDA'] - movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
            print("SALDO ATUAL = ", rentabilidade_mercados_modalidades[investment]['SALDO ATUAL'])
            print("GANHOS EFETIVOS = ", rentabilidade_mercados_modalidades[investment]['GANHOS EFETIVOS'])
            try:
                rentabilidade_total = (
                        (movimentacoes_anuais[investment][year_interest_str]['SAIDA'] - movimentacoes_anuais[investment][year_interest_str]['ENTRADA'] /
                        movimentacoes_anuais[investment][year_interest_str]['ENTRADA']))
                numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_date)
                rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
                rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
                representatividade = 0
                # Saving results to the rentabilidade_representatividade dictionary
                rentabilidade_mercados_modalidades[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total * 100
                rentabilidade_mercados_modalidades[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media * 100
                rentabilidade_mercados_modalidades[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media * 100
                rentabilidade_mercados_modalidades[investment]['REPRESENTATIVIDADE'] = representatividade * 100
                print("numero_dias = ", numero_dias)
                print("rentabilidade_total = ", rentabilidade_total)
                print("rentabilidade_mensal_media = ", rentabilidade_mensal_media)
                print("rentabilidade_anual_media = ", rentabilidade_anual_media)
                print("representatividade = ", representatividade)
            except ZeroDivisionError:
                rentabilidade_total = 0  # Handle division by zero
                representatividade = 0
                rentabilidade_anual_media = 0
                rentabilidade_mensal_media = 0

        else:
            data_vencimento_ajustada = year_month_interest_end
            numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_ajustada)
            if investment in valores_mensais:
                if month_bruto_key in valores_mensais[investment] and month_liquido_key in valores_mensais[investment]:
                    # Read and assign values to valor_atual_bruto and valor_atual_liquido
                    valor_atual_bruto = valores_mensais[investment][month_bruto_key]
                    valor_atual_liquido = valores_mensais[investment][month_liquido_key]
                    valor_mensal_medio_bruto, valor_mensal_medio_liquido = (
                        centralized_imports.valores_mensais_medios.calcular_valores_mensais_medios(data_compra_date,
                                                                                                   data_vencimento_ajustada,
                                                                                                   year_month_interest_end,
                                                                                                   investment))

                    try:
                        print(movimentacoes_anuais[investment][year_interest_str]['SAIDA'])
                        print(movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
                        rentabilidade_total = (
                                (valor_atual_liquido + (movimentacoes_anuais[investment][year_interest_str]['SAIDA'] - movimentacoes_anuais[investment][year_interest_str]['ENTRADA']))
                                / movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
                        rentabilidade_total = rentabilidade_total * 100
                    except ZeroDivisionError:
                        rentabilidade_total = 0  # Handle division by zero

                    # Annual average profit
                    rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
                    rentabilidade_anual_media = rentabilidade_anual_media * 100
                    # Monthly average profit
                    rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
                    rentabilidade_mensal_media = rentabilidade_mensal_media * 100
                    # Calculando a representatividade
                    representatividade = valor_atual_liquido / patrimonio_liquido
                    representatividade = representatividade * 100
                    soma_representatividade += representatividade

                    print("valor_atual_liquido = R${:,.2f}".format(valor_atual_liquido))
                    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))
                    # print(f"numero_dias = {numero_dias}")
                    print(f"rentabilidade_total = {rentabilidade_total:.2f}%")
                    print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media:.2f}%")
                    print(f"rentabilidade_anual_media = {rentabilidade_anual_media:.2f}%")
                    print(f"representatividade = {representatividade:.2f}%")
                    # Save the updated data back to the output pickle file
                    rentabilidade_mercados_modalidades[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
                    rentabilidade_mercados_modalidades[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
                    rentabilidade_mercados_modalidades[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
                    rentabilidade_mercados_modalidades[investment]['REPRESENTATIVIDADE'] = representatividade

                else:
                    print(f"Headers {month_bruto_key} or {month_liquido_key} not found for investment {investment}")
            else:
                print(f"Investment {investment} not found in valores_mensais")

        print(f"soma_representatividade = {soma_representatividade:.2f}%")

    print("Updated rentabilidade_representatividade dictionary:")
    for key, value in rentabilidade_mercados_modalidades.items():
        print(f"Investment: {key}")
        for sub_key, sub_value in value.items():
            print(f"  {sub_key}: {sub_value}")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_mercados_modalidades,
                                                                                   rentabilidade_mercados_modalidades)

    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_rentabilidade_mercados_modalidades)

    # centralized_imports.gui_functions.show_dictionary_window(filepath_rentabilidade_representatividade)

    # FOURTH PART: PROFITABILITY CALCULATIONS FOR EACH MERCADO AND EACH MODALIDADE SEPARATELY
    # ================================================================================================
    # print()
    # print("FOURTH PART: CALCULO DA RENTABILIDADE PARA CADA MERCADO E CADA MODALIDADE")
    # print("=" * 95)
    #
    # # Initialize dictionaries to store profitability calculations for MERCADO and MODALIDADE
    # mercado_rentabilidade = {}
    # modalidade_rentabilidade = {}
    #
    # for investment, details in movimentacoes_mensais.items():
    #     mercado = details.get('MERCADO', 'UNKNOWN')
    #     modalidade = details.get('MODALIDADE', 'UNKNOWN')
    #
    #     # Initialize the structures if they don't exist yet
    #     if mercado not in mercado_rentabilidade:
    #         mercado_rentabilidade[mercado] = {
    #             "RENTABILIDADE TOTAL": 0,
    #             "RENTABILIDADE ANUAL MEDIA": 0,
    #             "RENTABILIDADE MENSAL MEDIA": 0,
    #             "REPRESENTATIVIDADE": 0,
    #             "GANHOS EFETIVOS": 0
    #         }
    #     if modalidade not in modalidade_rentabilidade:
    #         modalidade_rentabilidade[modalidade] = {
    #             "RENTABILIDADE TOTAL": 0,
    #             "RENTABILIDADE ANUAL MEDIA": 0,
    #             "RENTABILIDADE MENSAL MEDIA": 0,
    #             "REPRESENTATIVIDADE": 0,
    #             "GANHOS EFETIVOS": 0
    #         }
    #
    #     # Calculate values for the investment
    #     if investment in rentabilidade_representatividade:
    #         rent_total = rentabilidade_representatividade[investment].get('RENTABILIDADE TOTAL', 0)
    #         rent_anual_media = rentabilidade_representatividade[investment].get('RENTABILIDADE ANUAL MEDIA', 0)
    #         rent_mensal_media = rentabilidade_representatividade[investment].get('RENTABILIDADE MENSAL MEDIA', 0)
    #         representatividade = rentabilidade_representatividade[investment].get('REPRESENTATIVIDADE', 0)
    #         ganhos_efetivos = rentabilidade_representatividade[investment].get('GANHOS EFETIVOS', 0)
    #
    #         # Sum these values into the respective MERCADO and MODALIDADE
    #         mercado_rentabilidade[mercado]['RENTABILIDADE TOTAL'] += rent_total
    #         mercado_rentabilidade[mercado]['RENTABILIDADE ANUAL MEDIA'] += rent_anual_media
    #         mercado_rentabilidade[mercado]['RENTABILIDADE MENSAL MEDIA'] += rent_mensal_media
    #         mercado_rentabilidade[mercado]['REPRESENTATIVIDADE'] += representatividade
    #         mercado_rentabilidade[mercado]['GANHOS EFETIVOS'] += ganhos_efetivos
    #
    #         modalidade_rentabilidade[modalidade]['RENTABILIDADE TOTAL'] += rent_total
    #         modalidade_rentabilidade[modalidade]['RENTABILIDADE ANUAL MEDIA'] += rent_anual_media
    #         modalidade_rentabilidade[modalidade]['RENTABILIDADE MENSAL MEDIA'] += rent_mensal_media
    #         modalidade_rentabilidade[modalidade]['REPRESENTATIVIDADE'] += representatividade
    #         modalidade_rentabilidade[modalidade]['GANHOS EFETIVOS'] += ganhos_efetivos

    # # Save the profitability for each MERCADO
    # for mercado, values in mercado_rentabilidade.items():
    #     if mercado not in rentabilidade_representatividade:
    #         rentabilidade_representatividade[mercado] = {}
    #
    #     rentabilidade_representatividade[mercado]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
    #     rentabilidade_representatividade[mercado]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
    #     rentabilidade_representatividade[mercado]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
    #     rentabilidade_representatividade[mercado]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']
    #     rentabilidade_representatividade[mercado]['GANHOS EFETIVOS'] = values['GANHOS EFETIVOS']
    #
    # # Save the profitability for each MODALIDADE
    # for modalidade, values in modalidade_rentabilidade.items():
    #     if modalidade not in rentabilidade_representatividade:
    #         rentabilidade_representatividade[modalidade] = {}
    #
    #     rentabilidade_representatividade[modalidade]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
    #     rentabilidade_representatividade[modalidade]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
    #     rentabilidade_representatividade[modalidade]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
    #     rentabilidade_representatividade[modalidade]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']
    #     rentabilidade_representatividade[modalidade]['GANHOS EFETIVOS'] = values['GANHOS EFETIVOS']

    # centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_mercados_modalidades)
    #
    # # Print out the updated rentabilidade_representatividade dictionary
    # print("Updated rentabilidade_representatividade dictionary for MERCADO and MODALIDADE:")
    # for key, value in rentabilidade_mercados_modalidades.items():
    #     print(f"{key}:")
    #     for sub_key, sub_value in value.items():
    #         print(f"  {sub_key}: {sub_value}")
