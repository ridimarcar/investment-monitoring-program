import centralized_imports

def calcular_rentabilidade_mercados_modalidades(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE calcular_rentabilidade_mercados_modalidades FUNCTION.")

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
    # print("year_interest = ", year_interest)
    # print("year_entrada_key = ", year_entrada_key)
    # print("year_saida_key = ", year_saida_key)
    # print("month_bruto_key = ", month_bruto_key)
    # print("month_liquido_key = ", month_liquido_key)
    # print("year_month_interest_start = ", year_month_interest_start)
    # print("year_month_interest_end = ", year_month_interest_end)
    # print("filepath_movimentacoes_mensais = ", filepath_movimentacoes_mensais)
    # print("filepath_movimentacoes_anuais = ", filepath_movimentacoes_anuais)
    # print("filepath_rentabilidade_representatividade = ", filepath_rentabilidade_representatividade)
    # print()

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
    # print()
    # for key, value in movimentacoes_anuais.items():
    #     print(f"{key} -> {value}")

    try:
        rentabilidade_mercados_modalidades = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_rentabilidade_mercados_modalidades))

        if rentabilidade_mercados_modalidades is None:
            print("Warning: Loaded 'rentabilidade_representatividade' is None. Initializing an empty dictionary.")
            rentabilidade_mercados_modalidades = {}

    except FileNotFoundError:
        print("File not found. Initializing 'rentabilidade_representatividade' as an empty dictionary.")
        rentabilidade_mercados_modalidades = {}

    except Exception as e:
        print(f"An error occurred while loading 'rentabilidade_representatividade': {e}")
        rentabilidade_mercados_modalidades = {}

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
    print("-" * 90)
    print("COPYING AND PASTING THE INVESTMENT INITIAL DATA")
    try:
        for investment in valores_mensais.keys():
            if investment not in skip_investment_list:
                continue
            try:
                # Get investment initial data from valores_mensais
                mercado_valores_mensais = valores_mensais[investment].get('MERCADO', '')
                modalidade_valores_mensais = valores_mensais[investment].get('MODALIDADE', '')
                codigo_valores_mensais = valores_mensais[investment].get('CODIGO', '')
                data_compra_valores_mensais = valores_mensais[investment].get('DATA COMPRA', '')
                data_vencimento_valores_mensais = valores_mensais[investment].get('DATA VENCIMENTO', '')

                # print("mercado_valores_mensais = ", mercado_valores_mensais)
                # print("modalidade_valores_mensais = ", modalidade_valores_mensais)
                # print("codigo_valores_mensais = ", codigo_valores_mensais)
                # print("data_compra_valores_mensais = ", data_compra_valores_mensais)
                # print("data_vencimento_valores_mensais = ", data_vencimento_valores_mensais)

                # Ensure that movimentacoes_mensais[investment] is initialized as a dictionary if it doesn't exist
                if investment not in rentabilidade_mercados_modalidades:
                    rentabilidade_mercados_modalidades[investment] = {}

                # Save investment initial data to rentabilidade_mercados_modalidades
                rentabilidade_mercados_modalidades[investment]["MERCADO"] = mercado_valores_mensais
                rentabilidade_mercados_modalidades[investment]["MODALIDADE"] = modalidade_valores_mensais
                rentabilidade_mercados_modalidades[investment]["CODIGO"] = codigo_valores_mensais
                rentabilidade_mercados_modalidades[investment]["DATA COMPRA"] = data_compra_valores_mensais
                rentabilidade_mercados_modalidades[investment]["DATA VENCIMENTO"] = data_vencimento_valores_mensais

                # print("mercado_rentabilidade_mercados_modalidades = ", rentabilidade_mercados_modalidades[investment]["MERCADO"])
                # print("modalidade_rentabilidade_mercados_modalidades = ", rentabilidade_mercados_modalidades[investment]["MODALIDADE"])
                # print("codigo_rentabilidade_mercados_modalidades = ", rentabilidade_mercados_modalidades[investment]["CODIGO"])
                # print("data_compra_rentabilidade_mercados_modalidades = ", rentabilidade_mercados_modalidades[investment]["DATA COMPRA"])
                # print("data_vencimento_rentabilidade_mercados_modalidades = ",
                #       rentabilidade_mercados_modalidades[investment]["DATA VENCIMENTO"])
                # print("-" * 90)

            except KeyError as e:
                print(f"KeyError: Missing key {e} in valores_mensais for investment '{investment}'")
            except Exception as e:
                print(f"An unexpected error occurred while processing investment '{investment}': {e}")

    except Exception as e:
        print(f"An unexpected error occurred in the outer block: {e}")
    print("rentabilidade_mercados_modalidades initial data updated")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_representatividade,
                                                                                   rentabilidade_mercados_modalidades)
    # centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_rentabilidade_mercados_modalidades)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

    # THIRD PART: PROFITABILITY CALCULATIONS FOR INDIVIDUAL INVESTMENTS
    # ===============================================================================================
    # print()
    # print("THIRD PART: CALCULO DA RENTABILIDADE PARA CADA INVESTIMENTO ATE A DATA DE INTERESSE")
    # print("=" * 95)
    # 
    # for investment in rentabilidade_mercados_modalidades:
    #     rentabilidade_mercados_modalidades[investment].setdefault("RENTABILIDADE TOTAL", 0)
    #     rentabilidade_mercados_modalidades[investment].setdefault("RENTABILIDADE ANUAL MEDIA", 0)
    #     rentabilidade_mercados_modalidades[investment].setdefault("RENTABILIDADE MENSAL MEDIA", 0)
    #     rentabilidade_mercados_modalidades[investment].setdefault("REPRESENTATIVIDADE", 0)
    #     rentabilidade_mercados_modalidades[investment].setdefault("SALDO ATUAL", 0)
    #     rentabilidade_mercados_modalidades[investment].setdefault("GANHOS EFETIVOS", 0)
    # 
    # contador_investimentos = 0
    # soma_representatividade = 0
    # skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
    # number_actual_investments = len(movimentacoes_mensais.items()) - len(skip_investment_list)
    # for investment, details in movimentacoes_mensais.items():
    #     if investment in skip_investment_list:
    #         continue
    #     print("-" * 95)
    #     contador_investimentos += 1
    #     print("Investment = ", investment)
    #     print(f"This is investment #{contador_investimentos} out of {number_actual_investments} investments")
    #     data_compra = details.get('DATA COMPRA')
    #     data_vencimento = details.get('DATA VENCIMENTO')
    #     print("data_compra = ", data_compra)
    #     print("data_vencimento = ", data_vencimento, end='\n')
    # 
    #     if not data_compra or not data_vencimento:
    #         print(f"Warning: 'DATA COMPRA' or 'DATA VENCIMENTO' is blank for investment {investment}. Skipping...")
    #         continue
    # 
    #     # Convert dates to datetime.date objects
    #     data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
    #     data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()
    # 
    #     # CASO CEDO DEMAIS PARA INVESTIMENTO ESTAR AQUI
    #     if data_compra_date > year_month_interest_end:
    #         print(f"Warning: It is too early for {investment} to be here. Skipping...")
    #         continue
    # 
    #     # CASO APLICACAO VENCIDA
    #     if year_month_interest_end > data_vencimento_date:
    #         print("APLICACAO JA VENCIDA")
    #         # if investment not in rentabilidade_representatividade.keys():
    #         #     rentabilidade_representatividade[investment] = {}
    #         rentabilidade_representatividade[investment]['SALDO ATUAL'] = 0
    #         print("movimentacoes_anuais saida = ", movimentacoes_anuais[investment][year_interest_str]['SAIDA'])
    #         print("movimentacoes_anuais entrada = ", movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
    #         rentabilidade_representatividade[investment]['GANHOS EFETIVOS'] = (
    #             movimentacoes_anuais[investment][year_interest_str]['SAIDA'] - movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
    #         print("SALDO ATUAL = ", rentabilidade_representatividade[investment]['SALDO ATUAL'])
    #         print("GANHOS EFETIVOS = ", rentabilidade_representatividade[investment]['GANHOS EFETIVOS'])
    #         try:
    #             rentabilidade_total = (
    #                     (movimentacoes_anuais[investment][year_interest_str]['SAIDA'] - movimentacoes_anuais[investment][year_interest_str]['ENTRADA'] /
    #                     movimentacoes_anuais[investment][year_interest_str]['ENTRADA']))
    #             numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_date)
    #             rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
    #             rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
    #             representatividade = 0
    #             # Saving results to the rentabilidade_representatividade dictionary
    #             rentabilidade_representatividade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
    #             rentabilidade_representatividade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
    #             rentabilidade_representatividade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
    #             rentabilidade_representatividade[investment]['REPRESENTATIVIDADE'] = representatividade
    #             print("numero_dias = ", numero_dias)
    #             print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
    #             print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
    #             print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
    #             print(f"representatividade = {representatividade * 100:.2f}%")
    #         except ZeroDivisionError:
    #             rentabilidade_total = 0  # Handle division by zero
    #             representatividade = 0
    #             rentabilidade_anual_media = 0
    #             rentabilidade_mensal_media = 0
    # 
    #     else:
    #         data_vencimento_ajustada = year_month_interest_end
    #         numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_ajustada)
    #         if investment in valores_mensais:
    #             if month_bruto_key in valores_mensais[investment] and month_liquido_key in valores_mensais[investment]:
    #                 # Read and assign values to valor_atual_bruto and valor_atual_liquido
    #                 valor_atual_bruto = valores_mensais[investment][month_bruto_key]
    #                 valor_atual_liquido = valores_mensais[investment][month_liquido_key]
    #                 valor_mensal_medio_bruto, valor_mensal_medio_liquido = (
    #                     centralized_imports.valores_mensais_medios.calcular_valores_mensais_medios(data_compra_date,
    #                                                                                                data_vencimento_ajustada,
    #                                                                                                year_month_interest_end,
    #                                                                                                investment))
    # 
    #                 try:
    #                     print(movimentacoes_anuais[investment][year_interest_str]['SAIDA'])
    #                     print(movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
    #                     rentabilidade_total = (
    #                             (valor_atual_liquido + (movimentacoes_anuais[investment][year_interest_str]['SAIDA'] - movimentacoes_anuais[investment][year_interest_str]['ENTRADA']))
    #                             / movimentacoes_anuais[investment][year_interest_str]['ENTRADA'])
    #                     # rentabilidade_total = rentabilidade_total
    #                 except ZeroDivisionError:
    #                     rentabilidade_total = 0  # Handle division by zero
    # 
    #                 # Annual average profit
    #                 rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
    #                 rentabilidade_anual_media = rentabilidade_anual_media
    #                 # Monthly average profit
    #                 rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
    #                 rentabilidade_mensal_media = rentabilidade_mensal_media
    #                 # Calculando a representatividade
    #                 representatividade = valor_atual_liquido / patrimonio_liquido
    #                 representatividade = representatividade
    #                 soma_representatividade += representatividade
    # 
    #                 print("valor_atual_liquido = R${:,.2f}".format(valor_atual_liquido))
    #                 print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))
    #                 # print(f"numero_dias = {numero_dias}")
    #                 print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
    #                 print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
    #                 print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
    #                 print(f"representatividade = {representatividade * 100:.2f}%")
    #                 # Save the updated data back to the output pickle file
    #                 rentabilidade_representatividade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
    #                 rentabilidade_representatividade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
    #                 rentabilidade_representatividade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
    #                 rentabilidade_representatividade[investment]['REPRESENTATIVIDADE'] = representatividade
    # 
    #             else:
    #                 print(f"Headers {month_bruto_key} or {month_liquido_key} not found for investment {investment}")
    #         else:
    #             print(f"Investment {investment} not found in valores_mensais")
    # 
    #     print(f"soma_representatividade = {soma_representatividade:.2f}%")
    # 
    # print("Updated rentabilidade_representatividade dictionary:")
    # # for key, value in rentabilidade_representatividade.items():
    # #     print(f"Investment: {key}")
    # #     for sub_key, sub_value in value.items():
    # #         print(f"  {sub_key}: {sub_value}")
    # 
    # centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_representatividade,
    #                                                                                rentabilidade_representatividade)

    # centralized_imports.gui_functions.show_dictionary_window(filepath_rentabilidade_representatividade)

    # FOURTH PART: PROFITABILITY CALCULATIONS FOR EACH MERCADO AND EACH MODALIDADE SEPARATELY
    # ================================================================================================
    print()
    print("FOURTH PART: CALCULO DA RENTABILIDADE PARA CADA MERCADO E CADA MODALIDADE")
    print("=" * 95)

    # Initialize dictionaries to store profitability calculations for MERCADO and MODALIDADE
    mercado_rentabilidade = {}
    modalidade_rentabilidade = {}

    for investment, details in movimentacoes_mensais.items():
        if investment not in skip_investment_list:
            continue
        mercado = details.get('MERCADO', 'UNKNOWN')
        modalidade = details.get('MODALIDADE', 'UNKNOWN')

        # Initialize the structures if they don't exist yet
        if mercado not in mercado_rentabilidade:
            mercado_rentabilidade[mercado] = {
                "RENTABILIDADE TOTAL": 0,
                "RENTABILIDADE ANUAL MEDIA": 0,
                "RENTABILIDADE MENSAL MEDIA": 0,
                "REPRESENTATIVIDADE": 0,
                "GANHOS EFETIVOS": 0
            }
        if modalidade not in modalidade_rentabilidade:
            modalidade_rentabilidade[modalidade] = {
                "RENTABILIDADE TOTAL": 0,
                "RENTABILIDADE ANUAL MEDIA": 0,
                "RENTABILIDADE MENSAL MEDIA": 0,
                "REPRESENTATIVIDADE": 0,
                "GANHOS EFETIVOS": 0
            }

        try:
            valor_atual_liquido = valores_mensais[investment][month_liquido_key]
            print("valor_atual_liquido = ", valor_atual_liquido)
            rentabilidade_total = (
                    (valor_atual_liquido + (movimentacoes_anuais[investment][year_interest_str]['SAIDA'] -
                                            movimentacoes_anuais[investment][year_interest_str]['ENTRADA']))
                    / movimentacoes_anuais[investment][year_interest_str]['ENTRADA']
            )
        except KeyError as e:
            print(
                f"KeyError: Missing key {e} in movimentacoes_anuais for investment '{investment}'. Setting rentabilidade_total to 0.")
            rentabilidade_total = 0
        except ZeroDivisionError:
            print(
                f"ZeroDivisionError: Division by zero encountered for investment '{investment}'. Setting rentabilidade_total to 0.")
            rentabilidade_total = 0
        except Exception as e:
            print(
                f"An unexpected error occurred while calculating rentabilidade_total for investment '{investment}': {e}")
            rentabilidade_total = 0

    # Save the profitability for each MERCADO
    for mercado, values in mercado_rentabilidade.items():
        if mercado not in rentabilidade_mercados_modalidades:
            rentabilidade_mercados_modalidades[mercado] = {}

        rentabilidade_mercados_modalidades[mercado]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
        rentabilidade_mercados_modalidades[mercado]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
        rentabilidade_mercados_modalidades[mercado]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
        rentabilidade_mercados_modalidades[mercado]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']
        rentabilidade_mercados_modalidades[mercado]['GANHOS EFETIVOS'] = values['GANHOS EFETIVOS']

    # Save the profitability for each MODALIDADE
    for modalidade, values in modalidade_rentabilidade.items():
        if modalidade not in rentabilidade_mercados_modalidades:
            rentabilidade_mercados_modalidades[modalidade] = {}

        rentabilidade_mercados_modalidades[modalidade]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
        rentabilidade_mercados_modalidades[modalidade]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
        rentabilidade_mercados_modalidades[modalidade]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
        rentabilidade_mercados_modalidades[modalidade]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']
        rentabilidade_mercados_modalidades[modalidade]['GANHOS EFETIVOS'] = values['GANHOS EFETIVOS']

    # Print out the updated rentabilidade_mercados_modalidades dictionary
    print("Updated rentabilidade_mercados_modalidades dictionary for MERCADO and MODALIDADE:")
    for key, value in rentabilidade_mercados_modalidades.items():
        print(f"{key}:")
        for sub_key, sub_value in value.items():
            print(f"  {sub_key}: {sub_value}")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_rentabilidade_mercados_modalidades,
        rentabilidade_mercados_modalidades)

    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_rentabilidade_mercados_modalidades)

    # FIFTH PART: CREATE TABLE AND PLOT DATA
    # ================================================================================================
    # Criar dicionario reduzido
    rent_rep_reduzido = (
        centralized_imports.investimentos_functions.InvestimentosFunctions.criar_dicionario_reduzido(rentabilidade_mercados_modalidades,
                                                                                                     parametros_funcoes))

    print()
    print("CALLING THE gerar_matriz_numpy FUNCTION")
    tipo_dicionario = "rentabilidade_mercados_modalidades"
    centralized_imports.gerar_graficos.gerar_matriz_numpy(rent_rep_reduzido,
                                                          tipo_dicionario,
                                                          parametros_funcoes)