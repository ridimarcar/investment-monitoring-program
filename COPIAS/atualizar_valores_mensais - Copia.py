import centralized_imports

def atualizar_valores_mensais(config):
    print("&" * 90)
    print("1. THIS IS THE atualizar_valores_mensais FUNCTION.")

    input_mode = config.get("input_mode", "manual")

    if input_mode == "automatic":
        # Get values from config
        year_interest = config.get("selected_year")
        month_interest = config.get("selected_month")
        year_entrada_key = f"{year_interest} ENTRADA"
        year_saida_key = f"{year_interest} SAIDA"
        month_bruto_key = f"{month_interest} BRUTO"
        month_liquido_key = f"{month_interest} LIQUIDO"
        month_entrada_key = f"{month_interest} ENTRADA"
        month_saida_key = f"{month_interest} SAIDA"
        year_month_interest_start = centralized_imports.datetime.datetime.strptime(config.get("year_month_interest_start"), '%Y-%m-%d').date()
        year_month_interest_end = centralized_imports.datetime.datetime.strptime(config.get("year_month_interest_end"), '%Y-%m-%d').date()
        filepath_valores_mensais = config.get("filepath_valores_mensais")
        filepath_movimentacoes_mensais = config.get("filepath_movimentacoes_mensais")
        filepath_variacoes_patrimoniais_mensais = config.get("filepath_variacoes_patrimoniais_mensais")
        filepath_variacoes_patrimoniais_anuais = config.get("filepath_variacoes_patrimoniais_anuais")
    else:
        dicionario_palavras_chave = centralized_imports.year_month_interest.ano_mes_interesse()

        if dicionario_palavras_chave is None:
            print("Failed to retrieve year and month interests.")
            return

        year_interest = dicionario_palavras_chave.get("year_interest")
        year_entrada_key = dicionario_palavras_chave.get("year_entrada_key")
        year_saida_key = dicionario_palavras_chave.get("year_saida_key")
        month_interest = dicionario_palavras_chave.get("selected_month")
        month_bruto_key = dicionario_palavras_chave.get("month_bruto_key")
        month_liquido_key = dicionario_palavras_chave.get("month_liquido_key")
        month_entrada_key = dicionario_palavras_chave.get("month_entrada_key")
        month_saida_key = dicionario_palavras_chave.get("month_saida_key")
        year_month_interest_start = dicionario_palavras_chave.get("year_month_interest_start")
        year_month_interest_end = dicionario_palavras_chave.get("year_month_interest_end")
        filepath_variacoes_patrimoniais_mensais = dicionario_palavras_chave.get("filepath_variacoes_patrimoniais_mensais")
        filepath_valores_mensais = dicionario_palavras_chave.get("filepath_valores_mensais")
        filepath_movimentacoes_mensais = dicionario_palavras_chave.get("filepath_movimentacoes_mensais")
        filepath_movimentacoes_anuais = dicionario_palavras_chave.get("filepath_movimentacoes_anuais")

    print("-" * 90)
    print("FIRST CHECK: THIS IS RIGHT AFTER THE FIRST IF ELSE BLOCK")
    print(f"Selected Year: {year_interest}")
    print(f"Selected Month: {month_interest}")
    print("month_bruto_key =", month_bruto_key)
    print("month_liquido_key =", month_liquido_key)
    print("month_entrada_key =", month_entrada_key)
    print("month_saida_key =", month_saida_key)
    print("year_month_interest_start =", year_month_interest_start)
    print("year_month_interest_end =", year_month_interest_end)

    filepaths_dictionary = centralized_imports.investimentos_btg.filepaths_dictionary
    filepath_movimentacoes_anuais = filepaths_dictionary.get("filepath_movimentacoes_anuais")
    filepath_variacoes_patrimoniais_anuais = filepaths_dictionary.get("filepath_variacoes_patrimoniais_anuais")
    filepath_movimentacoes_mensais_somadas = filepaths_dictionary.get("filepath_movimentacoes_mensais_somadas")
    filepath_rentabilidade_mercados_modalidades = filepaths_dictionary.get("filepath_rentabilidade_mercados_modalidades")
    filepath_rentabilidade_representatividade = filepaths_dictionary.get("filepath_rentabilidade_representatividade")
    filepath_valores_mensais_somados = filepaths_dictionary.get("filepath_valores_mensais_somados")

    # print("")
    # print("SECOND CHECK: THIS IS RIGHT BEFORE SETTING UP PARAMETROS FUNCOES")
    # print("filepath_variacoes_patrimoniais_mensais = ", filepath_variacoes_patrimoniais_mensais)
    # print("filepath_variacoes_patrimoniais_anuais = ", filepath_variacoes_patrimoniais_anuais)

    parametros_funcoes = {
        "year_interest": year_interest,
        "year_entrada_key": year_entrada_key,
        "year_saida_key": year_saida_key,
        "month_interest": month_interest,
        "month_entrada_key": month_entrada_key,
        "month_saida_key": month_saida_key,
        "month_bruto_key": month_bruto_key,
        "month_liquido_key": month_liquido_key,
        "year_month_interest_start": year_month_interest_start,
        "year_month_interest_end": year_month_interest_end,
        "filepath_valores_mensais": filepath_valores_mensais,
        "filepath_movimentacoes_mensais": filepath_movimentacoes_mensais,
        "filepath_movimentacoes_anuais": filepath_movimentacoes_anuais,
        "filepath_variacoes_patrimoniais_mensais": filepath_variacoes_patrimoniais_mensais,
        "filepath_variacoes_patrimoniais_anuais": filepath_variacoes_patrimoniais_anuais,
        "filepath_movimentacoes_mensais_somadas": filepath_movimentacoes_mensais_somadas,
        "filepath_rentabilidade_mercados_modalidades": filepath_rentabilidade_mercados_modalidades,
        "filepath_rentabilidade_representatividade": filepath_rentabilidade_representatividade,
        "filepath_valores_mensais_somados": filepath_valores_mensais_somados
    }

    # print("")
    # print("THIRD CHECK: THIS IS RIGHT AFTER SETTING UP PARAMETROS FUNCOES")
    # check = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")
    # print("check = ", check)

    print("=" * 90)
    # Ask the user if they want to run additional functions
    while True:
        print("Which function would you like to execute next?")
        print("1. Atualizar Movimentações Mensais")
        print("2. Atualizar Rentabilidade e Representatividade")
        print("3. Calcular Evolução Patrimonial")
        print("4. Calcular Rentabilidade Mercados Modalidades")
        print("5. Skip and Continue")

        print()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            centralized_imports.atualizar_movimentacoes_mensais.atualizar_movimentacoes_mensais(parametros_funcoes,
                                                                                                config)
            centralized_imports.gui_functions.show_dictionary_window(filepath_movimentacoes_mensais)
        elif choice == '2':
            centralized_imports.saldos_anuais_rentabilidade.atualizar_rentabilidade_representatividade(parametros_funcoes)
            centralized_imports.gui_functions.show_dictionary_window(filepath_rentabilidade_representatividade)
        elif choice == '3':
            centralized_imports.evolucao_patrimonial.calcular_evolucao_patrimonial(parametros_funcoes)
        elif choice == '4':
            centralized_imports.rentabilidade_mercados_modalidades.calcular_rentabilidade_mercados_modalidades(
                parametros_funcoes)
        elif choice == '5':
            print("Skipping additional functions and continuing with the script.")
            break  # Break out of the while loop to continue with the rest of the script
        else:
            print("Invalid choice. Please try again.")

    print("-" * 90)
    print("LOADING FILES:")
    valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais)

    if valores_mensais is None:
        print("valores_mensais is None")
        return
    if not isinstance(valores_mensais, dict):
        print("valores_mensais is not a dictionary")
        return
    if not valores_mensais:
        print("valores_mensais is empty")
        return

    print("-" * 90)
    # print("ENTERING THE LEFTMOST WHILE TRUE BLOCK")
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list
    while True:
        try:
            mercado, modalidade = centralized_imports.investimentos_functions.InvestimentosFunctions.selecionar_mercado_modalidade(config)
            is_tax_exempt = modalidade in centralized_imports.investimentos_btg.tax_exempt_modalidades
            print()
            print("mercado = ", mercado)
            print("modalidade = ", modalidade)
            print(f"The modalidade '{modalidade}' is {'tax-exempt' if is_tax_exempt else 'not tax-exempt'}", end='\n\n')
            investment_list = centralized_imports.investimentos_btg.InvestimentosBTG.get_selected_list(mercado, modalidade)
            print(f"THIS IS THE CURRENT LIST OF INVESTMENTS IN '{mercado}' / '{modalidade}' :", end='\n\n')
            for investment in investment_list:
                print(investment)
            print(end='\n')

            if not investment_list:
                print("The investment_list is empty. Exiting the loop.")
                return valores_mensais

            print("ENTERING THE FOR LOOP:")
            for index, investment in enumerate(investment_list, start=1):
                if investment in skip_investment_list:
                    continue
                print("-" * 90)
                print('INVESTMENT = ', investment)
                print(f"THIS IS INVESTMENT #{index} OUT OF {len(investment_list)} INVESTMENTS IN {mercado} / {modalidade}.", end='\n')
                if investment not in valores_mensais:
                    print(f"Skipping {investment} as it is not found in the main dictionary.")
                    print()
                    continue

                data_compra = valores_mensais[investment].get('DATA COMPRA', '')
                data_vencimento = valores_mensais[investment].get('DATA VENCIMENTO', '')
                print("data_compra =", data_compra)
                print("data_vencimento =", data_vencimento, end='\n\n')

                if data_compra and data_vencimento:
                    try:
                        purchase_date = centralized_imports.datetime.datetime.strptime(data_compra, '%Y-%m-%d').date()
                        maturity_date = centralized_imports.datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
                    except ValueError as e:
                        print(f"Invalid date format for investment {investment}. Error: {e}. Skipping...")
                        continue

                    if not (purchase_date <= year_month_interest_end and year_month_interest_start <= maturity_date):
                        valores_mensais[investment][month_bruto_key] = 0
                        valores_mensais[investment][month_liquido_key] = 0
                        print(f"{investment} is not within the selected year/month of interest. Setting values to zero and skipping...")
                        continue

                # Inserir valor_atual_bruto
                if input_mode == "automatic":
                    valor_atual_bruto = config["valor_atual_bruto"][index - 1]
                    print("Using config value for valor_atual_bruto:", valor_atual_bruto)

                    if is_tax_exempt:
                        valor_atual_liquido = valor_atual_bruto
                    else:
                        valor_atual_liquido = config["valor_atual_liquido"][index - 1]
                        print("Using config value for valor_atual_liquido:", valor_atual_liquido)
                else:
                    while True:
                        try:
                            texto = "Inserir valor atual bruto: "
                            valor_atual_bruto = centralized_imports.general_functions.GeneralFunctions.user_float_input(texto)
                            print("You entered:", valor_atual_bruto, end='\n\n')
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number for valor atual bruto.")

                    if is_tax_exempt:
                        valor_atual_liquido = valor_atual_bruto
                    else:
                        while True:
                            try:
                                texto = "Inserir valor atual liquido: "
                                valor_atual_liquido = centralized_imports.general_functions.GeneralFunctions.user_float_input(texto)
                                print("You entered:", valor_atual_liquido, end='\n\n')
                                break
                            except ValueError:
                                print("Invalid input. Please enter a valid number for valor atual liquido.")

                try:
                    valores_mensais[investment][month_bruto_key] = valor_atual_bruto
                    valores_mensais[investment][month_liquido_key] = valor_atual_liquido
                except KeyError as e:
                    print("KeyError encountered:", e)

            if input_mode == "automatic":
                pergunta1 = config.get("pergunta1", "n")
                print("Using config value for pergunta1:", pergunta1)
            else:
                pergunta1 = input("Deseja adicionar outro investimento? (s/n): ")
                print("You entered:", pergunta1)

            if pergunta1.lower() != 's':
                break

            print()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

    # Save all the new entries before moving on
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_valores_mensais,
                                                                                   valores_mensais)
    print()
    print("CALLING somar_valores_mensais FUNCTION")
    centralized_imports.somar_valores_mensais.somar_valores_mensais(parametros_funcoes)

    # Criar tabelas dos valores mensais para o relatorio
    # --------------------------------------------------------------------------------
    centralized_imports.gerar_tabelas.tabela_valores_mensais(parametros_funcoes)

    # Criar graficos pizza dos valores mensais para o relatorio
    # --------------------------------------------------------------------------------
    centralized_imports.gerar_graficos.criar_graficos_pizza(parametros_funcoes)

    # Atualizar movimentacoes mensais
    # --------------------------------------------------------------------------------
    print("-" * 90)
    if input_mode == "automatic":
        pergunta2 = config.get("pergunta2", "n")
        print("Using config value for atualizar movimentacoes MENSAIS:", pergunta2)
    else:
        # pergunta2 = input("Deseja atualizar as movimentacoes mensais agora? (s/n): ")
        pergunta2 = "s"
        print("You entered:", pergunta2)
    if pergunta2.lower() == 's':
        print("CALLING THE atualizar_movimentacoes_MENSAIS FUNCTION. ")
        centralized_imports.atualizar_movimentacoes_mensais.atualizar_movimentacoes_mensais(parametros_funcoes, config)

    # centralized_imports.gui_functions.show_dictionary_window(filepath_movimentacoes_mensais)
    # --------------------------------------------------------------------------------
    print("-" * 90)
    if input_mode == "automatic":
        pergunta3 = config.get("pergunta3", "n")
        print("Using config value for atualizar movimentacoes_ANUAIS:", pergunta3)
    else:
        # pergunta3 = input("Deseja atualizar movimentacoes_ANUAIS agora? (s/n): ")
        pergunta3 = "s"
        print("You entered:", pergunta3)
    if pergunta3.lower() == 's':
        print()
        print("CALLING THE atualizar_movimentacoes_ANUAIS FUNCTION.")
        centralized_imports.atualizar_movimentacoes_anuais.atualizar_movimentacoes_anuais(parametros_funcoes, config)

    # centralized_imports.gui_functions.show_dictionary_window(filepath_saldos_anuais_rentabilidade)
    # --------------------------------------------------------------------------------
    print("-" * 90)
    if input_mode == "automatic":
        pergunta4 = config.get("pergunta4", "n")
        print("Using config value for atualizar rentabilidade_representatividade:", pergunta4)
    else:
        # pergunta4 = input("Deseja atualizar saldos_anuais_rentabilidade agora? (s/n): ")
        pergunta4 = "s"
        print("You entered:", pergunta4)
    if pergunta4.lower() == 's':
        print("CALLING THE atualizar_rentabilidade_representatividade FUNCTION.")
        centralized_imports.rentabilidade_representatividade.atualizar_rentabilidade_representatividade(parametros_funcoes)

    # centralized_imports.gui_functions.show_dictionary_window(filepath_saldos_anuais_rentabilidade)
    # --------------------------------------------------------------------------------
    print("-" * 90)
    if input_mode == "automatic":
        pergunta5 = config.get("pergunta5", "n")
        print("Using config value for calcular_rentabilidade_mercados_modalidades:", pergunta5)
    else:
        # pergunta5 = input("Deseja calcular_rentabilidade_mercados_modalidades agora? (s/n): ")
        pergunta5 = "s"
        print("You entered:", pergunta5)
    if pergunta5.lower() == 's':
        print("CALLING THE calcular_rentabilidade_mercados_modalidades FUNCTION.")
        centralized_imports.rentabilidade_mercados_modalidades.calcular_rentabilidade_mercados_modalidades(
            parametros_funcoes)

    # --------------------------------------------------------------------------------
    print("-" * 90)
    if input_mode == "automatic":
        pergunta6 = config.get("pergunta6", "n")
        print("Using config value for atualizar variacoes_patrimonais_mensais:", pergunta6)
    else:
        # pergunta6 = input("Deseja atualizar evolucao_patrimonial agora? (s/n): ")
        pergunta6 = "s"
        print("You entered:", pergunta6)
    if pergunta6.lower() == 's':
        print("CALLING THE variacoes_patrimoniais_mensais FUNCTION.")
        centralized_imports.atualizar_variacoes_patrimoniais_mensais.atualizar_variacoes_patrimoniais_mensais(parametros_funcoes)

    # # --------------------------------------------------------------------------------
    # print("-" * 90)
    # if input_mode == "automatic":
    #     pergunta6 = config.get("pergunta6", "n")
    #     print("Using config value for calcular_rentabilidade_mercados_modalidades:", pergunta6)
    # else:
    #     # pergunta6 = input("Deseja calcular_rentabilidade_mercados_modalidades agora? (s/n): ")
    #     pergunta6 = "n"
    #     print("You entered:", pergunta6)
    # if pergunta6.lower() == 's':
    #     print("CALLING THE calcular_rentabilidade_mercados_modalidades FUNCTION.")
    #     centralized_imports.rentabilidade_mercados_modalidades.calcular_rentabilidade_mercados_modalidades(parametros_funcoes)

    # --------------------------------------------------------------------------------
    print("-" * 90)
    if input_mode == "automatic":
        pergunta7 = config.get("pergunta7", "n")
        print("Deseja gerar_relatorio_pdf agora? (s/n):", pergunta7)
    else:
        # pergunta7 = input("Deseja gerar_relatorio_pdf agora? (s/n): ")
        pergunta7 = "s"
        print("You entered:", pergunta7)
    if pergunta7.lower() == 's':
        print("CALLING THE gerar_relatorio FUNCTION")
        centralized_imports.gerar_relatorios.gerar_relatorio_mensal(parametros_funcoes)

