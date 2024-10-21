import centralized_imports

def ano_mes_interesse(config=None):
    print("=" * 90)
    print("THIS IS THE ano_mes_interesse FUNCTION")

    if config and config.get("input_mode") == "automatic":
        year_index = config["selected_year"] - 1
        selected_year = centralized_imports.investimentos_btg.years_list[year_index]
        year_interest = int(selected_year)
        month_index = config["selected_month"] - 1
        selected_month = centralized_imports.investimentos_btg.months_list[month_index]
        month_number = centralized_imports.investimentos_btg.month_name_mapping.get(selected_month, None)
    else:
        # Year selection
        print("-" * 90)
        print("SECTION: YEAR SELECTION")
        print("Select year:", end='\n')
        for i, item in enumerate(centralized_imports.investimentos_btg.years_list):
            print(f"{i + 1}. {item}")
        try:
            year_index = int(input("Enter YEAR: ")) - 1
            selected_year = centralized_imports.investimentos_btg.years_list[year_index]
            year_interest = int(selected_year)
        except (ValueError, IndexError):
            print("Invalid year selection. Please try again.")
            return None

        # Month selection
        print("-" * 90)
        print("SECTION: MONTH SELECTION")
        print("Select Month:", end='\n')
        for i, item in enumerate(centralized_imports.investimentos_btg.months_list):
            print(f"{i + 1}. {item}")
        try:
            month_index = int(input("Enter MONTH: ")) - 1
            selected_month = centralized_imports.investimentos_btg.months_list[month_index]
            month_number = centralized_imports.investimentos_btg.month_name_mapping.get(selected_month, None)
            if month_number is None:
                raise ValueError("Invalid month")
        except (ValueError, IndexError):
            print("Invalid month selection. Please try again.")
            return None

    year_entrada_key = f"{selected_year} ENTRADA"
    year_saida_key = f"{selected_year} SAIDA"
    year_bruto_key = f"{selected_year} BRUTO"
    year_liquido_key = f"{selected_year} LIQUIDO"
    month_bruto_key = f"{selected_month} BRUTO"
    month_liquido_key = f"{selected_month} LIQUIDO"
    month_entrada_key = f"{selected_month} ENTRADA"
    month_saida_key = f"{selected_month} SAIDA"

    try:
        year_month_interest_start = centralized_imports.datetime.date(year_interest, month_number, 1)
        next_month = month_number % 12 + 1
        next_month_year = year_interest if month_number != 12 else year_interest + 1
        year_month_interest_end = (
            centralized_imports.datetime.date(next_month_year, next_month, 1) - centralized_imports.datetime.timedelta(days=1))
    except ValueError as e:
        print("Error combining year and month:", e)
        return None

    retrieved_filepaths = (
        centralized_imports.general_functions.GeneralFunctions.recuperar_caminhos_arquivos(year_interest))
    filepath_movimentacoes_mensais = retrieved_filepaths[0]
    filepath_valores_mensais = retrieved_filepaths[1]
    filepath_evolucao_patrimonial_mensal = retrieved_filepaths[2]

    print("filepath_evolucao_patrimonial_mensal = ", filepath_evolucao_patrimonial_mensal)

    keywords_dictionary = {
        "year_interest": year_interest,
        "year_entrada_key": year_entrada_key,
        "year_saida_key": year_saida_key,
        "year_bruto_key": year_bruto_key,
        "year_liquido_key": year_liquido_key,
        "selected_month": selected_month,
        "month_number": month_number,
        "month_bruto_key": month_bruto_key,
        "month_liquido_key": month_liquido_key,
        "month_entrada_key": month_entrada_key,
        "month_saida_key": month_saida_key,
        "year_month_interest_start": year_month_interest_start,
        "year_month_interest_end": year_month_interest_end,
        "filepath_evolucao_patrimonial_mensal": filepath_evolucao_patrimonial_mensal,
        "filepath_valores_mensais": filepath_valores_mensais,
        "filepath_movimentacoes_mensais": filepath_movimentacoes_mensais
    }

    return keywords_dictionary