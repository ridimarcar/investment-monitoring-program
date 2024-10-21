import centralized_imports

def atualizar_rentabilidade_representatividade(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE atualizar_rentabilidade_representatividade FUNCTION.")


    # ===================================================================
    # SET UP PARAMETERS
    filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_entrada_key = parametros_funcoes.get("year_entrada_key")
    year_interest = parametros_funcoes.get("year_interest")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_saida_key = parametros_funcoes.get("year_saida_key")

    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Convert year_interest to string
    year_interest_str = str(year_interest)

    # ===================================================================
    # LOAD FILES
    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    dados_financeiros_historicos = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_dados_financeiros_historicos))

    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))

    try:
        rentabilidade_representatividade = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_rentabilidade_representatividade))

        if rentabilidade_representatividade is None:
            print("Warning: Loaded 'rentabilidade_representatividade' is None. Initializing an empty dictionary.")
            rentabilidade_representatividade = {}

    except FileNotFoundError:
        print("File not found. Initializing 'rentabilidade_representatividade' as an empty dictionary.")
        rentabilidade_representatividade = {}

    except Exception as e:
        print(f"An error occurred while loading 'rentabilidade_representatividade': {e}")
        rentabilidade_representatividade = {}

    # ===================================================================
    # COPYING AND PASTING THE INVESTMENT INITIAL DATA
    try:
        for investment in valores_mensais.keys():
            try:
                # Get investment initial data from valores_mensais
                mercado_valores_mensais = valores_mensais[investment].get('MERCADO', '')
                modalidade_valores_mensais = valores_mensais[investment].get('MODALIDADE', '')
                codigo_valores_mensais = valores_mensais[investment].get('CODIGO', '')
                data_compra_valores_mensais = valores_mensais[investment].get('DATA COMPRA', '')
                data_vencimento_valores_mensais = valores_mensais[investment].get('DATA VENCIMENTO', '')

                # Ensure that movimentacoes_mensais[investment] is initialized as a dictionary if it doesn't exist
                if investment not in rentabilidade_representatividade:
                    rentabilidade_representatividade[investment] = {}

                # Save investment initial data to rentabilidade_representatividade
                rentabilidade_representatividade[investment]["MERCADO"] = mercado_valores_mensais
                rentabilidade_representatividade[investment]["MODALIDADE"] = modalidade_valores_mensais
                rentabilidade_representatividade[investment]["CODIGO"] = codigo_valores_mensais
                rentabilidade_representatividade[investment]["DATA COMPRA"] = data_compra_valores_mensais
                rentabilidade_representatividade[investment]["DATA VENCIMENTO"] = data_vencimento_valores_mensais

            except KeyError as e:
                print(f"KeyError: Missing key {e} in valores_mensais for investment '{investment}'")
            except Exception as e:
                print(f"An unexpected error occurred while processing investment '{investment}': {e}")

    except Exception as e:
        print(f"An unexpected error occurred in the outer block: {e}")
    print("movimentacoes_mensais initial data updated")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_representatividade,
                                                                                   rentabilidade_representatividade)
    # CALCULO DA RENTABILIDADE PARA CADA INVESTIMENTO ATE A DATA DE INTERESSE
    # ===============================================================================================
    for investment in rentabilidade_representatividade:
        rentabilidade_representatividade[investment].setdefault("RENTABILIDADE TOTAL", 0)
        rentabilidade_representatividade[investment].setdefault("RENTABILIDADE ANUAL MEDIA", 0)
        rentabilidade_representatividade[investment].setdefault("RENTABILIDADE MENSAL MEDIA", 0)
        rentabilidade_representatividade[investment].setdefault("REPRESENTATIVIDADE", 0)
        rentabilidade_representatividade[investment].setdefault("SALDO ATUAL", 0)
        rentabilidade_representatividade[investment].setdefault("GANHOS EFETIVOS", 0)

    # Calcular rentabilidade e representatividade dos investimentos
    calcular_rentabilidade_representatividade_investimentos(parametros_funcoes)

    # Calcular rentabilidade e representatividade dos mercados e modalidades
    calcular_rentabilidade_representatividade_mercados_modalidades(parametros_funcoes)

    # CREATE TABLES FOR REPORT
    # ================================================================================================
    centralized_imports.gerar_tabelas.tabela_rentabilidade_representavidade(parametros_funcoes)

    # CREATE GROUPED BAR CHARTS FOR REPORT
    # ================================================================================================
    tipo_grafico = "BARRAS RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS"
    centralized_imports.gerar_graficos.criar_grafico_barras_horizontais(tipo_grafico,parametros_funcoes)

    tipo_grafico = "BARRAS RENTABILIDADE REPRESENTATIVIDADE MERCADOS"
    centralized_imports.gerar_graficos.criar_grafico_barras_horizontais(tipo_grafico, parametros_funcoes)

    tipo_grafico = "BARRAS RENTABILIDADE REPRESENTATIVIDADE MODALIDADES"
    centralized_imports.gerar_graficos.criar_grafico_barras_horizontais(tipo_grafico, parametros_funcoes)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def calcular_rentabilidade_representatividade_investimentos(parametros_funcoes):

    # SET UP PARAMETERS
    filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_entrada_key = parametros_funcoes.get("year_entrada_key")
    year_interest = parametros_funcoes.get("year_interest")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_saida_key = parametros_funcoes.get("year_saida_key")

    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Convert year_interest to string
    year_interest_str = str(year_interest)

    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))

    dados_financeiros_historicos = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_dados_financeiros_historicos))

    try:
        rentabilidade_representatividade = (
            centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_rentabilidade_representatividade))

        if rentabilidade_representatividade is None:
            print("Warning: Loaded 'rentabilidade_representatividade' is None. Initializing an empty dictionary.")
            rentabilidade_representatividade = {}

    except FileNotFoundError:
        print("File not found. Initializing 'rentabilidade_representatividade' as an empty dictionary.")
        rentabilidade_representatividade = {}

    except Exception as e:
        print(f"An error occurred while loading 'rentabilidade_representatividade': {e}")
        rentabilidade_representatividade = {}

    contador_investimentos = 0
    soma_representatividade = 0
    number_actual_investments = len(movimentacoes_mensais.items()) - len(skip_investment_list)

    for investment, details in movimentacoes_mensais.items():
        # Skip mercados and modalidades
        if investment in skip_investment_list:
            continue
        print("-" * 95)
        contador_investimentos += 1
        print("Investment = ", investment)
        print(f"This is investment #{contador_investimentos} out of {number_actual_investments} investments")
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
            # Set saldo atual to zero
            rentabilidade_representatividade[investment]['SALDO ATUAL'] = 0
            print("SALDO ATUAL = ", rentabilidade_representatividade[investment]['SALDO ATUAL'])

            print("movimentacoes_anuais saida = ", movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'])
            print("movimentacoes_anuais entrada = ", movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])

            rentabilidade_representatividade[investment]['GANHOS EFETIVOS'] = (
                movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'] - movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])


            ganhos_efetivos = movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'] - movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA']
            print("GANHOS EFETIVOS = ", rentabilidade_representatividade[investment]['GANHOS EFETIVOS'])

            numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_date)
            print("NUMERO DIAS = ", numero_dias)
            print("movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA']")
            print(movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])

            try:
                if numero_dias == 0:
                    rentabilidade_total = 0
                    rentabilidade_mensal_media = 0
                    rentabilidade_anual_media = 0
                else:
                    rentabilidade_total = \
                        (ganhos_efetivos / movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])
                    rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
                    rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
                representatividade = 0

                # Saving results to the rentabilidade_representatividade dictionary
                rentabilidade_representatividade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
                rentabilidade_representatividade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
                rentabilidade_representatividade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
                rentabilidade_representatividade[investment]['REPRESENTATIVIDADE'] = representatividade

                print("numero_dias = ", numero_dias)
                print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
                print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
                print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
                print(f"representatividade = {representatividade * 100:.2f}%")

            except ZeroDivisionError:
                rentabilidade_total = 0  # Handle division by zero
                representatividade = 0
                rentabilidade_anual_media = 0
                rentabilidade_mensal_media = 0

        # CASO APLICACAO AINDA EM VIGOR
        if year_month_interest_end <= data_vencimento_date:
            data_vencimento_ajustada = year_month_interest_end
            numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_ajustada)

            if investment in valores_mensais:
                if month_bruto_key in valores_mensais[investment] and month_liquido_key in valores_mensais[investment]:
                    # Read and assign values to valor_atual_bruto and valor_atual_liquido
                    valor_atual_bruto = valores_mensais[investment][month_bruto_key]
                    valor_atual_liquido = valores_mensais[investment][month_liquido_key]

                    try:
                        print("valor_atual_liquido = R${:,.2f}".format(valor_atual_liquido))
                        print("movimentacoes_anuais saida = ",
                              movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'])
                        print("movimentacoes_anuais entrada = ",
                              movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])

                        rentabilidade_total = (
                                (valor_atual_liquido + (movimentacoes_anuais[investment]["TOTAL INTERESSE SAIDA"] -
                                                        movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"]))
                                / movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"])
                        rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
                        rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1

                    except ZeroDivisionError:
                        rentabilidade_total = 0  # Handle division by zero

                    patrimonio_bruto = valores_mensais["TOTAL"][month_bruto_key]
                    patrimonio_liquido = valores_mensais["TOTAL"][month_liquido_key]
                    print()
                    print("patrimonio_bruto = R${:,.2f}".format(patrimonio_bruto))
                    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))

                    # Calculando a representatividade
                    representatividade = valor_atual_liquido / patrimonio_liquido
                    representatividade = representatividade
                    soma_representatividade += representatividade

                    print("valor_atual_liquido = R${:,.2f}".format(valor_atual_liquido))
                    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))
                    print("valor_atual_liquido = R${:,.2f}".format(valor_atual_liquido))
                    print(movimentacoes_anuais[investment]["TOTAL INTERESSE SAIDA"])
                    print(movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"])
                    # print(f"numero_dias = {numero_dias}")
                    print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
                    print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
                    print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
                    print(f"representatividade = {representatividade * 100:.2f}%")
                    print(f"soma_representatividade = {soma_representatividade * 100:.2f}%")

                    # Save the updated data back to the output pickle file
                    rentabilidade_representatividade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
                    rentabilidade_representatividade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
                    rentabilidade_representatividade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
                    rentabilidade_representatividade[investment]['REPRESENTATIVIDADE'] = representatividade



                else:
                    print(f"Headers {month_bruto_key} or {month_liquido_key} not found for investment {investment}")
            else:
                print(f"Investment {investment} not found in valores_mensais")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_representatividade, rentabilidade_representatividade)

# -------------------------------------------
def calcular_rentabilidade_representatividade_mercados_modalidades(parametros_funcoes):

    # SET UP PARAMETERS
    filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_entrada_key = parametros_funcoes.get("year_entrada_key")
    year_interest = parametros_funcoes.get("year_interest")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_saida_key = parametros_funcoes.get("year_saida_key")

    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Convert year_interest to string
    year_interest_str = str(year_interest)

    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))

    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # Initialize dictionaries to store profitability calculations for MERCADO and MODALIDADE
    mercado_rentabilidade = {}
    modalidade_rentabilidade = {}

    for investment, details in movimentacoes_mensais.items():
        if investment not in skip_investment_list:
            continue
        mercado = details.get('MERCADO', 'UNKNOWN')
        modalidade = details.get('MODALIDADE', 'UNKNOWN')

        print()
        print("Debugging carteira_rentabilidade:")
        print(f"{investment} -> {mercado}")
        print(f"{investment} -> {modalidade}")

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
        if mercado not in rentabilidade_representatividade:
            rentabilidade_representatividade[mercado] = {}

        rentabilidade_representatividade[mercado]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
        rentabilidade_representatividade[mercado]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
        rentabilidade_representatividade[mercado]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
        rentabilidade_representatividade[mercado]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']
        rentabilidade_representatividade[mercado]['GANHOS EFETIVOS'] = values['GANHOS EFETIVOS']

    # Save the profitability for each MODALIDADE
    for modalidade, values in modalidade_rentabilidade.items():
        if modalidade not in rentabilidade_representatividade:
            rentabilidade_representatividade[modalidade] = {}

        rentabilidade_representatividade[modalidade]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
        rentabilidade_representatividade[modalidade]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
        rentabilidade_representatividade[modalidade]['RENTABILIDADE MENSAL MEDIA'] = values[
            'RENTABILIDADE MENSAL MEDIA']
        rentabilidade_representatividade[modalidade]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']
        rentabilidade_representatividade[modalidade]['GANHOS EFETIVOS'] = values['GANHOS EFETIVOS']

    # Print out the updated rentabilidade_representatividade dictionary
    print("Updated rentabilidade_representatividade dictionary for MERCADO and MODALIDADE:")
    for key, value in rentabilidade_representatividade.items():
        print(f"{key}:")
        for sub_key, sub_value in value.items():
            print(f"  {sub_key}: {sub_value}")

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_rentabilidade_representatividade,
        rentabilidade_representatividade)