import centralized_imports

def evolucao_patrimonial_mensal(parametros_funcoes):

    # CHAPTER 1: Retrieve parameters from the dictionary
    # --------------------------------------------------
    year_interest = parametros_funcoes.get("year_interest")
    month_interest = parametros_funcoes.get("month_interest")
    year_entrada_key = parametros_funcoes.get("year_entrada_key")
    year_saida_key = parametros_funcoes.get("year_saida_key")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    month_entrada_key = parametros_funcoes.get("month_entrada_key")
    month_saida_key = parametros_funcoes.get("month_saida_key")
    year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    filepath_evolucao_patrimonial_mensal = parametros_funcoes.get("filepath_evolucao_patrimonial_mensal")
    filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
    filepath_saldos_anuais_rentabilidade = parametros_funcoes.get("filepath_saldos_anuais_rentabilidade")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")

    # Debug: Print all file paths
    print("filepath_evolucao_patrimonial_mensal =", filepath_evolucao_patrimonial_mensal)
    # print("filepath_movimentacoes_mensais =", filepath_movimentacoes_mensais)
    # print("filepath_saldos_anuais_rentabilidade =", filepath_saldos_anuais_rentabilidade)
    # print("filepath_valores_mensais =", filepath_valores_mensais)

    # CHAPTER 2: Create or load the output file (evolucao_patrimonial)
    # ----------------------------------------------------------------
    try:
        evolucao_patrimonial_mensal = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_evolucao_patrimonial_mensal)
        if evolucao_patrimonial_mensal is None:
            evolucao_patrimonial_mensal = {}
            print("evolucao_patrimonial_mensal did not exist and was successfully created.")
    except Exception as e:
        print(f"An error occurred while loading evolucao_patrimonial_mensal: {e}")
        return

    valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais)
    movimentacoes_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais)

    # Copy initial investment data
    for investment in valores_mensais.keys():
        try:
            mercado_valores_mensais = valores_mensais[investment].get('MERCADO', '')
            modalidade_valores_mensais = valores_mensais[investment].get('MODALIDADE', '')
            codigo_valores_mensais = valores_mensais[investment].get('CODIGO', '')
            data_compra_valores_mensais = valores_mensais[investment].get('DATA COMPRA', '')
            data_vencimento_valores_mensais = valores_mensais[investment].get('DATA VENCIMENTO', '')

            if investment not in evolucao_patrimonial_mensal:
                evolucao_patrimonial_mensal[investment] = {}

            evolucao_patrimonial_mensal[investment]["MERCADO"] = mercado_valores_mensais
            evolucao_patrimonial_mensal[investment]["MODALIDADE"] = modalidade_valores_mensais
            evolucao_patrimonial_mensal[investment]["CODIGO"] = codigo_valores_mensais
            evolucao_patrimonial_mensal[investment]["DATA COMPRA"] = data_compra_valores_mensais
            evolucao_patrimonial_mensal[investment]["DATA VENCIMENTO"] = data_vencimento_valores_mensais

        except KeyError as e:
            print(f"KeyError: Missing key {e} in valores_mensais for investment '{investment}'")
        except Exception as e:
            print(f"An unexpected error occurred while processing investment '{investment}': {e}")

    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_evolucao_patrimonial_mensal, evolucao_patrimonial_mensal)

    # --------------------------------------------------
    # Check for non-numeric entries
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_evolucao_patrimonial_mensal)
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_valores_mensais)
    centralized_imports.general_functions.GeneralFunctions.converter_para_numerico(filepath_movimentacoes_mensais)

    # --------------------------------------------------
    # Initialize variables
    patrimonio_bruto = patrimonio_liquido = saldo_mensal_entradas = saldo_mensal_saidas = 0.0
    try:
        patrimonio_bruto = valores_mensais["TOTAL"][month_bruto_key]
    except KeyError:
        patrimonio_bruto = 0.0
        print(f"KeyError: {month_bruto_key} not found in 'TOTAL'")

    # Calculate monthly evolution
    for investment, data in evolucao_patrimonial_mensal.items():
        try:
            valor_bruto_atual = valores_mensais[investment].get(month_bruto_key, 0.0)
            valor_liquido_atual = valores_mensais[investment].get(month_liquido_key, 0.0)

            # Calculate previous month key
            previous_month_end = year_month_interest_end.replace(day=1) - centralized_imports.datetime.timedelta(days=1)
            previous_month_bruto_key = previous_month_end.strftime("%B").upper() + " BRUTO"
            valor_liquido_anterior = valores_mensais[investment].get(previous_month_bruto_key, 0.0)

            saldo_mensal_entradas = movimentacoes_mensais[investment].get(month_entrada_key, 0.0)
            saldo_mensal_saidas = movimentacoes_mensais[investment].get(month_saida_key, 0.0)

            ganho_efetivo = (
                        (valor_liquido_atual - valor_liquido_anterior) - (saldo_mensal_entradas - saldo_mensal_saidas))

            evolucao_patrimonial_mensal[investment][month_interest] = ganho_efetivo

        except KeyError as e:
            print(f"KeyError: {e} for investment '{investment}'")
        except Exception as e:
            # Print the values of all variables involved to identify the problem
            print(f"An unexpected error occurred while processing investment '{investment}': {e}")
            print("Debugging Info:")
            print(f"valor_bruto_atual: {valor_bruto_atual}")
            print(f"valor_liquido_atual: {valor_liquido_atual}")
            print(f"previous_month_bruto_key: {previous_month_bruto_key}")
            print(f"valor_liquido_anterior: {valor_liquido_anterior}")
            print(f"saldo_mensal_entradas: {saldo_mensal_entradas}")
            print(f"saldo_mensal_saidas: {saldo_mensal_saidas}")

    # Save the updated evolucao_patrimonial_mensal
    centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_evolucao_patrimonial_mensal,
                                                                                   evolucao_patrimonial_mensal)
    centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_evolucao_patrimonial_mensal)

    centralized_imports.gerar_tabelas.tabelas_evolucao_patrimonial(parametros_funcoes)


