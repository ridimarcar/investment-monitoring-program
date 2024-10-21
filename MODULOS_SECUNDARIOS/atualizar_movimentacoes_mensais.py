import centralized_imports

def atualizar_movimentacoes_mensais(parametros_funcoes, config):
    print("&" * 90)
    print("THIS IS THE atualizar_movimentacoes_mensais FUNCTION.")

    # Extract relevant parameters from the function arguments
    year_interest = str(parametros_funcoes.get("year_interest"))
    month_interest = parametros_funcoes.get("month_interest")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_movimentacoes_mensais_padrao = parametros_funcoes.get("filepath_movimentacoes_mensais_padrao")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")
    month_saida_key = parametros_funcoes.get("month_saida_key")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")

    print("filepath_movimentacoes_mensais_padrao", filepath_movimentacoes_mensais_padrao)

    input_mode = config.get("input_mode", "manual")

    # Handle automatic mode configuration
    if input_mode == "automatic":
        year_interest = config.get("selected_year")
        month_interest = config.get("selected_month")
        month_entrada_key = f"{month_interest} ENTRADA"
        month_saida_key = f"{month_interest} SAIDA"
        year_month_interest_start = centralized_imports.datetime.datetime.strptime(
            config.get("year_month_interest_start"), '%Y-%m-%d').date()
        year_month_interest_end = centralized_imports.datetime.datetime.strptime(
            config.get("year_month_interest_end"), '%Y-%m-%d').date()
        filepath_movimentacoes_mensais = config.get("filepath_movimentacoes_mensais")
    
    # -----------------------------------------------------------------
    # Load files
    try:
        movimentacoes_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_movimentacoes_mensais)
        if movimentacoes_mensais is None or not isinstance(movimentacoes_mensais, dict) or not movimentacoes_mensais:
            print("Invalid or empty movimentacoes_mensais.")
            movimentacoes_mensais = {}
    except Exception as e:
        print(f"An error occurred while loading movimentacoes_mensais: {e}")
        movimentacoes_mensais = {}

    try:
        valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_valores_mensais)
        if valores_mensais is None or not isinstance(valores_mensais, dict) or not valores_mensais:
            print("Invalid or empty valores_mensais.")
            return
    except Exception as e:
        print(f"An error occurred while loading valores_mensais: {e}")
        return

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # print("-" * 90)
    # print("COPYING AND PASTING THE INVESTMENT INITIAL DATA")
    # try:
    #     for investment in valores_mensais.keys():
    #         try:
    #             # Get investment initial data from valores_mensais
    #             mercado_valores_mensais = valores_mensais[investment].get('MERCADO', '')
    #             modalidade_valores_mensais = valores_mensais[investment].get('MODALIDADE', '')
    #             codigo_valores_mensais = valores_mensais[investment].get('CODIGO', '')
    #             data_compra_valores_mensais = valores_mensais[investment].get('DATA COMPRA', '')
    #             data_vencimento_valores_mensais = valores_mensais[investment].get('DATA VENCIMENTO', '')
    #
    #             print("mercado_valores_mensais = ", mercado_valores_mensais)
    #             print("modalidade_valores_mensais = ", modalidade_valores_mensais)
    #             print("codigo_valores_mensais = ", codigo_valores_mensais)
    #             print("data_compra_valores_mensais = ", data_compra_valores_mensais)
    #             print("data_vencimento_valores_mensais = ", data_vencimento_valores_mensais)
    #
    #             # Ensure that movimentacoes_mensais[investment] is initialized as a dictionary if it doesn't exist
    #             if investment not in movimentacoes_mensais:
    #                 movimentacoes_mensais[investment] = {}
    #
    #             # Save investment initial data to movimentacoes_mensais
    #             movimentacoes_mensais[investment]["MERCADO"] = mercado_valores_mensais
    #             movimentacoes_mensais[investment]["MODALIDADE"] = modalidade_valores_mensais
    #             movimentacoes_mensais[investment]["CODIGO"] = codigo_valores_mensais
    #             movimentacoes_mensais[investment]["DATA COMPRA"] = data_compra_valores_mensais
    #             movimentacoes_mensais[investment]["DATA VENCIMENTO"] = data_vencimento_valores_mensais
    #
    #             print("mercado_movimentacoes_mensais = ", movimentacoes_mensais[investment]["MERCADO"])
    #             print("modalidade_movimentacoes_mensais = ", movimentacoes_mensais[investment]["MODALIDADE"])
    #             print("codigo_movimentacoes_mensais = ", movimentacoes_mensais[investment]["CODIGO"])
    #             print("data_compra_movimentacoes_mensais = ", movimentacoes_mensais[investment]["DATA COMPRA"])
    #             print("data_vencimento_movimentacoes_mensais = ", movimentacoes_mensais[investment]["DATA VENCIMENTO"])
    #             print("-" * 90)
    #
    #         except KeyError as e:
    #             print(f"KeyError: Missing key {e} in valores_mensais for investment '{investment}'")
    #         except Exception as e:
    #             print(f"An unexpected error occurred while processing investment '{investment}': {e}")
    #
    # except Exception as e:
    #     print(f"An unexpected error occurred in the outer block: {e}")
    # print("movimentacoes_mensais initial data updated")
    #
    # centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_movimentacoes_mensais)

    # centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_movimentacoes_mensais, movimentacoes_mensais)

    # Conferir com padrao
    movimentacoes_mensais_padrao = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
        filepath_movimentacoes_mensais_padrao)
    centralized_imports.criar_dicionarios_padronizados.atualizar_dicionario_alvo(
        movimentacoes_mensais_padrao, movimentacoes_mensais, filepath_movimentacoes_mensais)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # print("-" * 90)
    # print("COPYING AND PASTING THE INVESTMENT INITIAL DATA")
    #
    # try:
    #     for investment in variacoes_mensais.keys():
    #         try:
    #             # Get investment initial data from variacoes_mensais
    #             mercado_variacoes_mensais = variacoes_mensais[investment].get('MERCADO', '')
    #             modalidade_variacoes_mensais = variacoes_mensais[investment].get('MODALIDADE', '')
    #             codigo_variacoes_mensais = variacoes_mensais[investment].get('CODIGO', '')
    #             data_compra_variacoes_mensais = variacoes_mensais[investment].get('DATA COMPRA', '')
    #             data_vencimento_variacoes_mensais = variacoes_mensais[investment].get('DATA VENCIMENTO', '')
    #
    #             # Ensure that movimentacoes_mensais[investment] is initialized as a dictionary if it doesn't exist
    #             if investment not in movimentacoes_mensais:
    #                 movimentacoes_mensais[investment] = {}
    #
    #             # Check if the information is already present in movimentacoes_mensais
    #             needs_update = (
    #                     movimentacoes_mensais[investment].get("MERCADO") != mercado_variacoes_mensais or
    #                     movimentacoes_mensais[investment].get("MODALIDADE") != modalidade_variacoes_mensais or
    #                     movimentacoes_mensais[investment].get("CODIGO") != codigo_variacoes_mensais or
    #                     movimentacoes_mensais[investment].get("DATA COMPRA") != data_compra_variacoes_mensais or
    #                     movimentacoes_mensais[investment].get("DATA VENCIMENTO") != data_vencimento_variacoes_mensais
    #             )
    #
    #             # Only update movimentacoes_mensais if the information is missing or outdated
    #             if needs_update:
    #                 movimentacoes_mensais[investment]["MERCADO"] = mercado_variacoes_mensais
    #                 movimentacoes_mensais[investment]["MODALIDADE"] = modalidade_variacoes_mensais
    #                 movimentacoes_mensais[investment]["CODIGO"] = codigo_variacoes_mensais
    #                 movimentacoes_mensais[investment]["DATA COMPRA"] = data_compra_variacoes_mensais
    #                 movimentacoes_mensais[investment]["DATA VENCIMENTO"] = data_vencimento_variacoes_mensais
    #                 print(f"Updated data for investment '{investment}'")
    #
    #         except KeyError as e:
    #             print(f"KeyError: Missing key {e} in variacoes_mensais for investment '{investment}'")
    #         except Exception as e:
    #             print(f"An unexpected error occurred while processing investment '{investment}': {e}")
    #
    # except Exception as e:
    #     print(f"An unexpected error occurred in the outer block: {e}")

    # -----------------------------------------------------------------
    while True:
        try:
            mercado, modalidade = centralized_imports.investimentos_functions.InvestimentosFunctions.selecionar_mercado_modalidade(config)
            print()
            print(f"mercado = {mercado}")
            print(f"modalidade = {modalidade}")
            investment_list = centralized_imports.investimentos_btg.InvestimentosBTG.get_selected_list(mercado, modalidade)
            print(f"THIS IS THE CURRENT LIST OF INVESTMENTS IN '{mercado}' / '{modalidade}' :")
            for investment in investment_list:
                print(investment)

            if not investment_list:
                print("The investment_list is empty. Exiting the loop.")
                return movimentacoes_mensais

            print("Entering the for loop:")
            for index, investment in enumerate(investment_list, start=1):
                print("-" * 90)
                print(f'INVESTMENT = {investment}')
                print(f"THIS IS INVESTMENT #{index} OUT OF {len(investment_list)} INVESTMENTS IN {mercado} / {modalidade}.")

                if investment not in movimentacoes_mensais:
                    print(f"{investment} not found in the main dictionary. Skipping ...")
                    continue

                data_compra = movimentacoes_mensais[investment].get('DATA COMPRA', '')
                data_vencimento = movimentacoes_mensais[investment].get('DATA VENCIMENTO', '')
                print(f"data_compra = {data_compra}")
                print(f"data_vencimento = {data_vencimento}")

                if data_compra and data_vencimento:
                    try:
                        purchase_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()
                        maturity_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
                    except ValueError as e:
                        print(f"Invalid date format for investment {investment}. Error: {e}. Skipping...")
                        continue

                    if not (purchase_date <= year_month_interest_end and year_month_interest_start <= maturity_date):
                        movimentacoes_mensais[investment][month_entrada_key] = 0
                        movimentacoes_mensais[investment][month_saida_key] = 0
                        print(f"{investment} is not within the selected year/month of interest. Setting values to zero and skipping...")
                        continue

                # Inserir valor_entrada e valor_saida
                if input_mode == "automatic":
                    # Ensure config values are cast as floats
                    valor_entrada = float(config["valor_entrada"][index - 1])
                    print(f"Using config value for valor_entrada: {valor_entrada}")
                    valor_atual_liquido = float(config["valor_atual_liquido"][index - 1])
                    print(f"Using config value for valor_atual_liquido: {valor_atual_liquido}")
                else:
                    while True:
                        try:
                            texto = "Inserir valor entrada: "
                            valor_entrada = centralized_imports.general_functions.GeneralFunctions.user_float_input(texto)
                            print(f"You entered: {valor_entrada}")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number for valor entrada.")

                    while True:
                        try:
                            texto = "Inserir valor saida: "
                            valor_saida = centralized_imports.general_functions.GeneralFunctions.user_float_input(texto)
                            print(f"You entered: {valor_saida}")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number for valor saida.")

                try:
                    movimentacoes_mensais[investment][month_entrada_key] = valor_entrada
                    movimentacoes_mensais[investment][month_saida_key] = valor_saida
                except KeyError as e:
                    print(f"KeyError encountered: {e}")

            if input_mode == "automatic":
                pergunta1 = config.get("pergunta1", "n")
                print(f"Using config value for pergunta1: {pergunta1}")
            else:
                pergunta1 = input("Deseja adicionar outro investimento? (s/n): ")
                print(f"You entered: {pergunta1}")

            if pergunta1.lower() != 's':
                break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

    # Save modified dict
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(
        filepath_movimentacoes_mensais, movimentacoes_mensais)

    # Check for non-numeric entries
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_movimentacoes_mensais)

    # ---------------------------------------------------------
    print("-" * 90)
    print("SOMANDO AS MOVIMENTACOES MENSAIS:")

    # 1. PERFORM SUMMATIONS FOR THE MONTH AND YEAR IN year_month_interest_end
    centralized_imports.somar_movimentacoes_mensais.somar_movimentacoes_mensais(parametros_funcoes)

    # 2. PERFORM SUMMATIONS FOR THE YEAR IN year_month_interest_end
    #    AND UP TO month_interest INCLUSIVE.
    centralized_imports.atualizar_movimentacoes_anuais.atualizar_movimentacoes_anuais(parametros_funcoes, config)

    # 3. PERFORM SUMMATIONS FOR ALL THE RELEVANT YEARS FOR EACH INVESTMENT
    centralized_imports.atualizar_movimentacoes_anuais.somar_historico_movimentacoes_anuais(parametros_funcoes)

    # 4. PLOT TABLES
    centralized_imports.gerar_tabelas.tabela_movimentacoes_mensais(parametros_funcoes)





