import centralized_imports

def somar_valores_mensais(parametros_funcoes):
    print("&" * 90)
    print("THIS IS THE somar_valores_mensais FUNCTION.")

    year_interest = str(parametros_funcoes.get("year_interest"))
    year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
    month_interest = parametros_funcoes.get("month_interest")
    month_bruto_key = parametros_funcoes.get("month_bruto_key")
    month_liquido_key = parametros_funcoes.get("month_liquido_key")
    # filepath_dados_financeiros_historicos = parametros_funcoes.get("filepath_dados_financeiros_historicos")
    filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")

    # Set locale for Brazilian currency format
    centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')

    # Load files
    try:
        valores_mensais = centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
            filepath_valores_mensais)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath_valores_mensais}. Please check the file path.")
        return
    except Exception as e:
        print(f"Error: Failed to open the file. {str(e)}")
        return

    # Initialize dictionaries to store totals by MERCADO and MODALIDADE
    mercado_totals_bruto = {}
    mercado_totals_liquido = {}
    modalidade_totals_bruto = {}
    modalidade_totals_liquido = {}

    # Ensure 'TOTAL' key exists in valores_mensais and reset the totals
    valores_mensais['TOTAL'] = {}
    valores_mensais['TOTAL']["MERCADO"] = "TOTAL"
    valores_mensais['TOTAL']["MODALIDADE"] = "TOTAL"
    valores_mensais['TOTAL']["CODIGO"] = "TOTAL"
    valores_mensais['TOTAL']["DATA COMPRA"] = "2020-05-20"
    valores_mensais['TOTAL']["DATA VENCIMENTO"] = "2032-05-17"
    valores_mensais['TOTAL'][month_bruto_key] = 0
    valores_mensais['TOTAL'][month_liquido_key] = 0

    # Initialize the 'MERCADO' and 'MODALIDADE' keys and reset their totals
    for investment, data in valores_mensais.items():
        mercado = data.get('MERCADO', 'UNKNOWN')
        modalidade = data.get('MODALIDADE', 'UNKNOWN')

        # Reset totals for 'MERCADO'
        if mercado not in mercado_totals_bruto:
            mercado_totals_bruto[mercado] = 0
        if mercado not in mercado_totals_liquido:
            mercado_totals_liquido[mercado] = 0

        # Reset totals for 'MODALIDADE'
        if modalidade not in modalidade_totals_bruto:
            modalidade_totals_bruto[modalidade] = 0
        if modalidade not in modalidade_totals_liquido:
            modalidade_totals_liquido[modalidade] = 0

    # Fetch skip_investment_list
    skip_investment_list = centralized_imports.investimentos_btg.skip_investment_list

    # Iterate over the items in valores_mensais
    for investment, data in valores_mensais.items():
        if investment in skip_investment_list:
            continue

        # Remove 'CAPITAL INICIAL INVESTIDO' if exists
        data.pop('CAPITAL INICIAL INVESTIDO', None)

        bruto_exists = month_bruto_key in data
        liquido_exists = month_liquido_key in data

        if bruto_exists and isinstance(data[month_bruto_key], str):
            try:
                data[month_bruto_key] = float(data[month_bruto_key].replace(",", "."))
            except ValueError:
                continue

        if liquido_exists and isinstance(data[month_liquido_key], str):
            try:
                data[month_liquido_key] = float(data[month_liquido_key].replace(",", "."))
            except ValueError:
                continue

        mercado = data.get('MERCADO', 'UNKNOWN')
        modalidade = data.get('MODALIDADE', 'UNKNOWN')

        if bruto_exists:
            mercado_totals_bruto[mercado] += data[month_bruto_key]
            modalidade_totals_bruto[modalidade] += data[month_bruto_key]

        if liquido_exists:
            mercado_totals_liquido[mercado] += data[month_liquido_key]
            modalidade_totals_liquido[modalidade] += data[month_liquido_key]

    print()

    # Save summations for each mercado
    mercados_list = centralized_imports.investimentos_btg.mercados_list
    for mercado in mercados_list:
        try:
            valores_mensais[mercado][month_bruto_key] = mercado_totals_bruto[mercado]
            valores_mensais[mercado][month_liquido_key] = mercado_totals_liquido[mercado]
            print(f"mercado_totals_bruto[{mercado}] = {mercado_totals_bruto[mercado]}")
            print(f"mercado_totals_liquido[{mercado}] = {mercado_totals_liquido[mercado]}")
            print("valores_mensais[mercado][month_bruto_key]", valores_mensais[mercado][month_bruto_key])
            print("valores_mensais[mercado][month_liquido_key]", valores_mensais[mercado][month_liquido_key])
            valores_mensais[mercado]["MERCADO"] = mercado
            valores_mensais[mercado]["MODALIDADE"] = mercado
            valores_mensais[mercado]["CODIGO"] = mercado
            valores_mensais[mercado]["DATA COMPRA"] = "2020-05-20"
            valores_mensais[mercado]["DATA VENCIMENTO"] = "2032-05-17"
        except KeyError:
            print(f"Warning: Mercado '{mercado}' not found. Creating it ...")
            valores_mensais[mercado] = {}
            valores_mensais[mercado]["MERCADO"] = mercado
            valores_mensais[mercado]["MODALIDADE"] = mercado
            valores_mensais[mercado]["CODIGO"] = mercado
            valores_mensais[mercado]["DATA COMPRA"] = "2020-05-20"
            valores_mensais[mercado]["DATA VENCIMENTO"] = "2032-05-17"
            valores_mensais[mercado][month_bruto_key] = mercado_totals_bruto.get(mercado, 0)
            valores_mensais[mercado][month_liquido_key] = mercado_totals_liquido.get(mercado, 0)

    # Save summations for each modalidade
    modalidades_list = centralized_imports.investimentos_btg.modalidades_list
    for modalidade in modalidades_list:
        try:
            # print(f"modalidade_totals_bruto[{modalidade}] = {modalidade_totals_bruto[modalidade]}")
            # print(f"modalidade_totals_liquido[{modalidade}] = {modalidade_totals_liquido[modalidade]}")
            valores_mensais[modalidade][month_bruto_key] = modalidade_totals_bruto[modalidade]
            valores_mensais[modalidade][month_liquido_key] = modalidade_totals_liquido[modalidade]
            valores_mensais[modalidade]["MERCADO"] = modalidade
            valores_mensais[modalidade]["MODALIDADE"] = modalidade
            valores_mensais[modalidade]["CODIGO"] = modalidade
            valores_mensais[modalidade]["DATA COMPRA"] = "2020-05-20"
            valores_mensais[modalidade]["DATA VENCIMENTO"] = "2032-05-17"
        except KeyError:
            print(f"Warning: Modalidade '{modalidade}' not found. Creating it ...")
            valores_mensais[modalidade] = {}
            valores_mensais[modalidade]["MERCADO"] = modalidade
            valores_mensais[modalidade]["MODALIDADE"] = modalidade
            valores_mensais[modalidade]["CODIGO"] = modalidade
            valores_mensais[modalidade]["DATA COMPRA"] = "2020-05-20"
            valores_mensais[modalidade]["DATA VENCIMENTO"] = "2032-05-17"
            valores_mensais[modalidade][month_bruto_key] = modalidade_totals_bruto.get(modalidade, 0)
            valores_mensais[modalidade][month_liquido_key] = modalidade_totals_liquido.get(modalidade, 0)

    # Save the summation by MERCADO and MODALIDADE within the TOTAL key
    valores_mensais['TOTAL'][month_bruto_key] = sum(mercado_totals_bruto.values())
    valores_mensais['TOTAL'][month_liquido_key] = sum(mercado_totals_liquido.values())

    # Ensure 'MERCADO', 'MODALIDADE', 'UNKNOWN', AND '' are not being added as main keys
    if "MERCADO" in valores_mensais:
        del valores_mensais["MERCADO"]
    if "MODALIDADE" in valores_mensais:
        del valores_mensais["MODALIDADE"]
    if "UNKNOWN" in valores_mensais:
        del valores_mensais["UNKNOWN"]
    if "" in valores_mensais:
        del valores_mensais[""]

    try:
        centralized_imports.arquivos_functions.ArquivosFunctions.gravar_arquivo_pickle(filepath_valores_mensais,
                                                                                       valores_mensais)
        centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_valores_mensais)
        # centralized_imports.gui_functions.show_dictionary_window(filepath_valores_mensais)
    except Exception as e:
        print(f"Error saving file: {str(e)}")

