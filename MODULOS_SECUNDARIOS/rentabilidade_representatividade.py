import centralized_imports

# ======================================================================
def atualizar_rentabilidade_representatividade(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE atualizar_rentabilidade_representatividade FUNCTION.")

    # SET UP PARAMETERS
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")

    # LOAD FILES
    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

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

    # COPY AND PASTE THE INVESTMENT INITIAL DATA
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
    print("rentabilidade_representatividade initial data updated")

    # RESET rentabilidade_representatividade DATA
    for investment in rentabilidade_representatividade:
        rentabilidade_representatividade[investment].setdefault("RENTABILIDADE TOTAL", 0)
        rentabilidade_representatividade[investment].setdefault("RENTABILIDADE ANUAL MEDIA", 0)
        rentabilidade_representatividade[investment].setdefault("RENTABILIDADE MENSAL MEDIA", 0)
        rentabilidade_representatividade[investment].setdefault("REPRESENTATIVIDADE", 0)
        rentabilidade_representatividade[investment].setdefault("SALDO ATUAL", 0)
        rentabilidade_representatividade[investment].setdefault("GANHOS EFETIVOS", 0)

    # SAVE UPDATED FILE
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_rentabilidade_representatividade,
                                                                                   rentabilidade_representatividade)
    # CALCULAR RENTABILIDADE E REPRESENTATIVIDADE
    # Investimentos
    calcular_rentabilidade_representatividade_investimentos(parametros_funcoes)
    # Mercados
    calcular_rentabilidade_representatividade_mercados(parametros_funcoes)
    # Modalidades
    calcular_rentabilidade_representatividade_modalidades(parametros_funcoes)
    # Carteira
    calcular_rentabilidade_representatividade_carteira(parametros_funcoes)

    # CREATE TABLES FOR REPORT
    centralized_imports.gerar_tabelas.tabela_rentabilidade_representavidade(parametros_funcoes)

    # CREATE GROUPED HORIZONTAL BAR CHARTS
    tipo_grafico = "BARRAS RENTABILIDADE REPRESENTATIVIDADE INVESTIMENTOS"
    centralized_imports.gerar_graficos.criar_grafico_barras_horizontais(tipo_grafico,parametros_funcoes)

    tipo_grafico = "BARRAS RENTABILIDADE REPRESENTATIVIDADE MERCADOS"
    centralized_imports.gerar_graficos.criar_grafico_barras_horizontais(tipo_grafico, parametros_funcoes)

    tipo_grafico = "BARRAS RENTABILIDADE REPRESENTATIVIDADE MODALIDADES"
    centralized_imports.gerar_graficos.criar_grafico_barras_horizontais(tipo_grafico, parametros_funcoes)

    tipo_grafico = "BARRAS GANHOS APLICACOES VENCIDAS"
    centralized_imports.gerar_graficos.criar_grafico_barras_ganhos_saldos_pandas(tipo_grafico, parametros_funcoes)

    tipo_grafico = "BARRAS GANHOS SALDOS APLICACOES EM VIGOR"
    centralized_imports.gerar_graficos.criar_grafico_barras_ganhos_saldos_pandas(tipo_grafico, parametros_funcoes)
# -------------------------------------------
def calcular_rentabilidade_representatividade_investimentos(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE calcular_rentabilidade_representatividade_investimentos FUNCTION.")

    # SET UP PARAMETERS
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # LOAD FILES
    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))

    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # TO THE REAL CALCULATIONS
    contador_investimentos = 0
    soma_representatividade = 0
    number_actual_investments = len(movimentacoes_mensais.items()) - len(skip_investment_list)
    # patrimonio_bruto = valores_mensais["TOTAL"][month_bruto_key]
    patrimonio_liquido = valores_mensais["TOTAL"][month_liquido_key]
    print()
    # print("patrimonio_bruto = R${:,.2f}".format(patrimonio_bruto))
    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))

    for investment, details in movimentacoes_mensais.items():
        print("-" * 95)
        contador_investimentos += 1
        print("Investment = ", investment)
        print(f"This is investment #{contador_investimentos} out of {number_actual_investments} investments")

        # Skip mercados and modalidades, but keep TOTAL
        if investment in skip_investment_list:
            print(f"{investment} was skipped")
            continue

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
            saldo_atual = 0
            # Calculate ganhos efetivos
            print("movimentacoes_anuais saida = ", movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'])
            print("movimentacoes_anuais entrada = ", movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])
            ganhos_efetivos = movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'] - \
                              movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA']
            print("GANHOS EFETIVOS = ", ganhos_efetivos)
            # Calculate numero_dias
            numero_dias = (
                centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_date))
            print("NUMERO DIAS = ", numero_dias)
           # Calculate rentabilidade
            rentabilidade_total = \
                (ganhos_efetivos / movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])
            rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
            rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
            representatividade = 0

            # Saving results to the rentabilidade_representatividade dictionary as decimal numbers
            rentabilidade_representatividade[investment]['SALDO ATUAL'] = 0
            rentabilidade_representatividade[investment]['GANHOS EFETIVOS'] = ganhos_efetivos
            rentabilidade_representatividade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
            rentabilidade_representatividade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
            rentabilidade_representatividade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
            rentabilidade_representatividade[investment]['REPRESENTATIVIDADE'] = representatividade

            print("numero_dias = ", numero_dias)
            print("SALDO ATUAL = ", saldo_atual)
            print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
            print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
            print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
            print(f"representatividade = {representatividade * 100:.2f}%")

        # CASO APLICACAO AINDA EM VIGOR
        if year_month_interest_end <= data_vencimento_date:
            data_vencimento_ajustada = year_month_interest_end
            numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(data_compra_date, data_vencimento_ajustada)

            if investment in valores_mensais:
                if month_liquido_key in valores_mensais[investment]:
                    valor_atual_liquido = valores_mensais[investment][month_liquido_key]
                    try:
                        print("valor_atual_liquido = R${:,.2f}".format(valor_atual_liquido))
                        print("movimentacoes_anuais saida = ",
                              movimentacoes_anuais[investment]['TOTAL INTERESSE SAIDA'])
                        print("movimentacoes_anuais entrada = ",
                              movimentacoes_anuais[investment]['TOTAL INTERESSE ENTRADA'])
                        # Set saldo atual
                        saldo_atual = valor_atual_liquido
                        # Calculate ganhos efetivos
                        ganhos_efetivos = (
                                movimentacoes_anuais[investment]["TOTAL INTERESSE SAIDA"] - movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"])
                        # Calculate profitability
                        rentabilidade_total = (
                                (valor_atual_liquido + (movimentacoes_anuais[investment]["TOTAL INTERESSE SAIDA"] -
                                                        movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"]))
                                / movimentacoes_anuais[investment]["TOTAL INTERESSE ENTRADA"])
                        rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
                        rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1
                    except ZeroDivisionError:
                        rentabilidade_total = 0  # Handle division by zero
                        rentabilidade_anual_media = 0
                        rentabilidade_mensal_media = 0


                    # Calculando a representatividade
                    representatividade = valor_atual_liquido / patrimonio_liquido
                    # representatividade = representatividade
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
            # Saving results to the rentabilidade_representatividade dictionary as decimal numbers
            rentabilidade_representatividade[investment]['SALDO ATUAL'] = saldo_atual
            rentabilidade_representatividade[investment]['GANHOS EFETIVOS'] = ganhos_efetivos
            rentabilidade_representatividade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
            rentabilidade_representatividade[investment][
                'RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
            rentabilidade_representatividade[investment][
                'RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
            rentabilidade_representatividade[investment]['REPRESENTATIVIDADE'] = representatividade

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_rentabilidade_representatividade, rentabilidade_representatividade)

def calcular_rentabilidade_representatividade_mercados(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE calcular_rentabilidade_representatividade_mercados FUNCTION.")

    # SET UP PARAMETERS
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_interest = parametros_funcoes.get("year_interest")
    year_interest_str = str(year_interest)
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    mercados_list = centralized_imports.investimentos_btg.mercados_list

    # LOAD FILES
    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))

    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # TO THE REAL CALCULATIONS
    mercados_rentabilidade = {}
    soma_representatividade = 0
    patrimonio_liquido = valores_mensais["TOTAL"][month_liquido_key]
    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))

    for investment, data in movimentacoes_anuais.items():
        # Check if the 'investment' is a 'MERCADO'
        if investment in mercados_list:
            mercados_rentabilidade[investment] = {
                "RENTABILIDADE TOTAL": 0,
                "RENTABILIDADE ANUAL MEDIA": 0,
                "RENTABILIDADE MENSAL MEDIA": 0,
                "REPRESENTATIVIDADE": 0
            }

            data_compra = data.get('DATA COMPRA')
            data_vencimento = data.get('DATA VENCIMENTO')

            if not data_compra or not data_vencimento:
                print(f"Warning: 'DATA COMPRA' or 'DATA VENCIMENTO' is blank for investment {investment}. Skipping...")
                continue

            # Convert dates to datetime.date objects
            data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
            data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()
            data_vencimento_ajustada = year_month_interest_end

            numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(
                data_compra_date, data_vencimento_ajustada)

            # CASO CEDO DEMAIS PARA INVESTIMENTO ESTAR AQUI
            if data_compra_date > year_month_interest_end:
                print(f"Warning: It is too early for {investment} to be here. Skipping...")
                continue

            try:
                valor_atual_liquido = valores_mensais[investment][month_liquido_key]
                year_interest_entrada = f"{year_interest_str} ENTRADA"
                year_interest_saida = f"{year_interest_str} SAIDA"

                rentabilidade_total = (
                        (valor_atual_liquido + (movimentacoes_anuais[investment][year_interest_saida] -
                                                movimentacoes_anuais[investment][year_interest_entrada]))
                        / movimentacoes_anuais[investment][year_interest_entrada]
                )
                rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
                rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1

                # Calculando a representatividade
                representatividade = valor_atual_liquido / patrimonio_liquido
                soma_representatividade += representatividade

                # Store the results back in the mercados_rentabilidade dictionary
                mercados_rentabilidade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
                mercados_rentabilidade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
                mercados_rentabilidade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
                mercados_rentabilidade[investment]['REPRESENTATIVIDADE'] = representatividade
            except KeyError as e:
                print(
                    f"KeyError: Missing key {e} in movimentacoes_anuais for investment '{investment}'. Setting rentabilidade_total to 0.")
                rentabilidade_total = 0
                rentabilidade_anual_media = 0
                rentabilidade_mensal_media = 0
                representatividade = 0
            except ZeroDivisionError:
                print(
                    f"ZeroDivisionError: Division by zero encountered for investment '{investment}'. Setting rentabilidade_total to 0.")
                rentabilidade_total = 0
                rentabilidade_anual_media = 0
                rentabilidade_mensal_media = 0
                representatividade = 0
            except Exception as e:
                print(
                    f"An unexpected error occurred while calculating rentabilidade_total for investment '{investment}': {e}")
                rentabilidade_total = 0
                rentabilidade_anual_media = 0
                rentabilidade_mensal_media = 0
                representatividade = 0

            print("-" * 90)
            print(f"{investment}")
            print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
            print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
            print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
            print(f"representatividade = {representatividade * 100:.2f}%")
            print(f"soma_representatividade = {soma_representatividade * 100:.2f}%")

    # Save the profitability for each MERCADO
    for mercado, values in mercados_rentabilidade.items():
        if mercado not in rentabilidade_representatividade:
            rentabilidade_representatividade[mercado] = {}

        # Ensure you are updating the dictionary correctly inside the loop
        rentabilidade_representatividade[mercado]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
        rentabilidade_representatividade[mercado]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
        rentabilidade_representatividade[mercado]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
        rentabilidade_representatividade[mercado]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']

    # Save the results to the pickle file
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_rentabilidade_representatividade,
        rentabilidade_representatividade)

def calcular_rentabilidade_representatividade_modalidades(parametros_funcoes):
    print()
    print("&" * 90)
    print("THIS IS THE calcular_rentabilidade_representatividade_modalidades FUNCTION.")

    # SET UP PARAMETERS
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_interest = parametros_funcoes.get("year_interest")
    year_interest_str = str(year_interest)
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    modalidades_list = centralized_imports.investimentos_btg.modalidades_list

    # LOAD FILES
    movimentacoes_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))

    valores_mensais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))

    movimentacoes_anuais = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_anuais))

    rentabilidade_representatividade = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_rentabilidade_representatividade))

    # REAL CALCULATIONS
    modalidades_rentabilidade = {}
    soma_representatividade = 0
    patrimonio_liquido = valores_mensais["TOTAL"][month_liquido_key]
    print("patrimonio_liquido = R${:,.2f}".format(patrimonio_liquido))

    print()
    for investment, data in movimentacoes_anuais.items():
        if investment not in modalidades_list:
            continue

        modalidades_rentabilidade[investment] = {
            "RENTABILIDADE TOTAL": 0,
            "RENTABILIDADE ANUAL MEDIA": 0,
            "RENTABILIDADE MENSAL MEDIA": 0,
            "REPRESENTATIVIDADE": 0
        }

        data_compra = data.get('DATA COMPRA')
        data_vencimento = data.get('DATA VENCIMENTO')

        if not data_compra or not data_vencimento:
            print(f"Warning: 'DATA COMPRA' or 'DATA VENCIMENTO' is blank for investment {investment}. Skipping...")
            continue

        # Convert dates to datetime.date objects
        data_vencimento_ajustada = year_month_interest_end
        data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()

        # Skip if the investment was purchased after the interest period
        if data_compra_date > year_month_interest_end:
            print(f"Warning: It is too early for {investment} to be here. Skipping...")
            continue

        numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(
            data_compra_date, data_vencimento_ajustada)

        try:
            valor_atual_liquido = valores_mensais[investment][month_liquido_key]
            year_interest_entrada = f"{year_interest_str} ENTRADA"
            year_interest_saida = f"{year_interest_str} SAIDA"

            # Calculate profitability
            rentabilidade_total = (
                (valor_atual_liquido + (movimentacoes_anuais[investment][year_interest_saida] -
                                        movimentacoes_anuais[investment][year_interest_entrada]))
                / movimentacoes_anuais[investment][year_interest_entrada]
            )
            rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
            rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1

            # Calculate representativity
            representatividade = valor_atual_liquido / patrimonio_liquido
            soma_representatividade += representatividade

            # Store the calculated values in modalidades_rentabilidade
            modalidades_rentabilidade[investment]['RENTABILIDADE TOTAL'] = rentabilidade_total
            modalidades_rentabilidade[investment]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
            modalidades_rentabilidade[investment]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media
            modalidades_rentabilidade[investment]['REPRESENTATIVIDADE'] = representatividade

        except KeyError as e:
            print(f"KeyError: Missing key {e} in movimentacoes_anuais for investment '{investment}'. Setting rentabilidade_total to 0.")
            rentabilidade_total = 0
            rentabilidade_anual_media = 0
            rentabilidade_mensal_media = 0
            representatividade = 0
        except ZeroDivisionError:
            print(f"ZeroDivisionError: Division by zero encountered for investment '{investment}'. Setting rentabilidade_total to 0.")
            rentabilidade_total = 0
            rentabilidade_anual_media = 0
            rentabilidade_mensal_media = 0
            representatividade = 0
        except Exception as e:
            print(f"An unexpected error occurred while calculating rentabilidade_total for investment '{investment}': {e}")
            rentabilidade_total = 0
            rentabilidade_anual_media = 0
            rentabilidade_mensal_media = 0
            representatividade = 0

        # Print for debugging
        print("-" * 90)
        print(f"{investment}")
        print(f"rentabilidade_total = {rentabilidade_total * 100:.2f}%")
        print(f"rentabilidade_mensal_media = {rentabilidade_mensal_media * 100:.2f}%")
        print(f"rentabilidade_anual_media = {rentabilidade_anual_media * 100:.2f}%")
        print(f"representatividade = {representatividade * 100:.2f}%")
        print(f"soma_representatividade = {soma_representatividade * 100:.2f}%")

    # Save the profitability for each MODALIDADE
    for modalidade, values in modalidades_rentabilidade.items():
        if modalidade not in rentabilidade_representatividade:
            rentabilidade_representatividade[modalidade] = {}

        # Store the calculated values for each modalidade
        rentabilidade_representatividade[modalidade]['RENTABILIDADE TOTAL'] = values['RENTABILIDADE TOTAL']
        rentabilidade_representatividade[modalidade]['RENTABILIDADE ANUAL MEDIA'] = values['RENTABILIDADE ANUAL MEDIA']
        rentabilidade_representatividade[modalidade]['RENTABILIDADE MENSAL MEDIA'] = values['RENTABILIDADE MENSAL MEDIA']
        rentabilidade_representatividade[modalidade]['REPRESENTATIVIDADE'] = values['REPRESENTATIVIDADE']

    # Save the results to the pickle file
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_rentabilidade_representatividade,
        rentabilidade_representatividade)

def calcular_rentabilidade_representatividade_carteira(parametros_funcoes):
    print("&" * 90)
    print("THIS IS THE calcular_rentabilidade_representatividade_carteira FUNCTION.")

    # SET UP PARAMETERS
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_movimentacoes_anuais = parametros_funcoes.get("filepath_movimentacoes_anuais")
    filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    year_interest = parametros_funcoes.get("year_interest")
    year_interest_str = str(year_interest)
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    # LOAD FILES
    valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_valores_mensais)
    movimentacoes_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_movimentacoes_mensais)
    movimentacoes_anuais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_movimentacoes_anuais)
    rentabilidade_representatividade = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_rentabilidade_representatividade)

    # Ensure 'TOTAL' key exists in both dictionaries to avoid KeyError
    if "TOTAL" not in valores_mensais or "TOTAL" not in movimentacoes_anuais:
        print("Error: 'TOTAL' key is missing from either valores_mensais or movimentacoes_anuais. Skipping...")
        return

    # TO THE CALCULATIONS
    data_compra = "2020-05-20"
    data_vencimento = "2032-05-17"

    if not data_compra or not data_vencimento:
        print(f"Warning: 'DATA COMPRA' or 'DATA VENCIMENTO' is blank for TOTAL. Skipping...")
        return

    # Convert dates to datetime.date objects
    data_vencimento_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
    data_compra_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()
    data_vencimento_ajustada = year_month_interest_end

    print("data_compra = ", data_compra)
    print("data_vencimento_ajustada = ", data_vencimento_ajustada)

    numero_dias = centralized_imports.general_functions.GeneralFunctions.number_days(
        data_compra_date, data_vencimento_ajustada)
    print("numero_dias = ", numero_dias)

    # Check if required subkeys exist before proceeding
    if not all(key in movimentacoes_anuais["TOTAL"] for key in ["TOTAL INTERESSE ENTRADA", "TOTAL INTERESSE SAIDA"]):
        print("Error: 'TOTAL INTERESSE ENTRADA' or 'TOTAL INTERESSE SAIDA' is missing. Skipping calculations...")
        return

    valor_atual_liquido = valores_mensais["TOTAL"].get(month_liquido_key, 0)

    if movimentacoes_anuais["TOTAL"]["TOTAL INTERESSE ENTRADA"] == 0:
        print("Warning: Division by zero risk with 'TOTAL INTERESSE ENTRADA'. Setting rentabilidade_total to 0.")
        rentabilidade_total = 0
    else:
        rentabilidade_total = (
            (valor_atual_liquido + (movimentacoes_anuais["TOTAL"]["TOTAL INTERESSE SAIDA"] -
                                    movimentacoes_anuais["TOTAL"]["TOTAL INTERESSE ENTRADA"]))
            / movimentacoes_anuais["TOTAL"]["TOTAL INTERESSE ENTRADA"]
        )

    # Ensure that numero_dias is not zero to prevent division by zero
    if numero_dias == 0:
        print("Warning: numero_dias is zero. Setting rentabilidade_mensal_media and rentabilidade_anual_media to 0.")
        rentabilidade_mensal_media = 0
        rentabilidade_anual_media = 0
    else:
        rentabilidade_mensal_media = (1 + rentabilidade_total) ** (30.42 / numero_dias) - 1
        rentabilidade_anual_media = (1 + rentabilidade_total) ** (365 / numero_dias) - 1

    # Store results in rentabilidade_representatividade
    if "TOTAL" not in rentabilidade_representatividade:
        rentabilidade_representatividade["TOTAL"] = {}

    rentabilidade_representatividade["TOTAL"]['RENTABILIDADE TOTAL'] = rentabilidade_total
    rentabilidade_representatividade["TOTAL"]['RENTABILIDADE ANUAL MEDIA'] = rentabilidade_anual_media
    rentabilidade_representatividade["TOTAL"]['RENTABILIDADE MENSAL MEDIA'] = rentabilidade_mensal_media

    print("rentabilidade_total = {:.2%}".format(rentabilidade_total))
    print("rentabilidade_mensal_media = {:.2%}".format(rentabilidade_mensal_media))
    print("rentabilidade_anual_media = {:.2%}".format(rentabilidade_anual_media))

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
       filepath_rentabilidade_representatividade, rentabilidade_representatividade)


