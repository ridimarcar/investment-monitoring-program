# Function
# ------------------------------------------------------------------------
import centralized_imports

# ------------------------------------------------------------------------
def calcular_valores_mensais_medios(data_compra,
                                    data_vencimento,
                                    year_month_interest_end,
                                    investment_name):
    # print()
    # print("&" * 90)
    # print("THIS IS THE calcular_valores_mensais_medios FUNCTION.")
    # print("DATA COMPRA = ", data_compra)
    # print("DATA VENCIMENTO = ", data_vencimento)
    # print("investment_name = ", investment_name)
    # print("year_month_interest_end = ", year_month_interest_end)

    # ========================================================================
    # LOAD RELEVANT FILES

    # Fetch filepaths list
    filepaths_list = centralized_imports.investimentos_btg.filepaths_list
    # Determine the range of years to load
    start_year = data_compra.year
    end_year = min(centralized_imports.datetime.datetime.now().year, data_vencimento.year)

    # print("Loading data for years:", list(range(start_year, end_year + 1)))

    # Filter the filepaths based on the years
    relevant_filepaths = {
        year: filepath for year in range(start_year, end_year + 1)
        for filepath in filepaths_list if f"valores_mensais_{year}" in filepath
    }

    # print("Relevant filepaths to load:", relevant_filepaths)

    # Load the relevant pickle files
    valores_mensais_data = {}
    for year, filepath in relevant_filepaths.items():
        with open(filepath, 'rb') as file:
            valores_mensais_data[year] = centralized_imports.pickle.load(file)
            # print(f"Loaded data from {filepath}: {valores_mensais_data[year].keys()}")
            # print(f"Data loaded successfully from {filepath}")

    # ===============================================================================
    # CALCULATE THE AVERAGE BRUTO AND LIQUIDO VALUES

    # Extract the relevant data for the investment
    bruto_values = []
    liquido_values = []
    total_months_considered = 0

    # Loop over the range of years and months
    current_date = data_compra
    while current_date <= year_month_interest_end:
        year = current_date.year
        month = current_date.month

        if year not in valores_mensais_data:
            print(f"No data for year {year}")
            current_date = (current_date.replace(day=28) + centralized_imports.datetime.timedelta(days=4)).replace(day=1)
            continue

        month_name = centralized_imports.investimentos_btg.month_number_mapping[month]
        month_key_bruto = f"{month_name} BRUTO"
        month_key_liquido = f"{month_name} LIQUIDO"
        investment_data = valores_mensais_data[year].get(investment_name, {})

        if month_key_bruto in investment_data:
            try:
                bruto_value = float(investment_data[month_key_bruto])
                bruto_values.append(bruto_value)
                # print(f"Found {month_key_bruto}: {bruto_value}")
            except ValueError:
                print(f"Non-numeric value for {month_key_bruto}: {investment_data[month_key_bruto]}")
        else:
            print(f"Missing {month_key_bruto}")

        if month_key_liquido in investment_data:
            try:
                liquido_value = float(investment_data[month_key_liquido])
                liquido_values.append(liquido_value)
                # print(f"Found {month_key_liquido}: {liquido_value}")
            except ValueError:
                print(f"Non-numeric value for {month_key_liquido}: {investment_data[month_key_liquido]}")
        else:
            print(f"Missing {month_key_liquido}")

        total_months_considered += 1
        current_date = (current_date.replace(day=28) + centralized_imports.datetime.timedelta(days=4)).replace(day=1)

    # Calculate the averages
    avg_bruto = sum(bruto_values) / total_months_considered if bruto_values else 0
    avg_liquido = sum(liquido_values) / total_months_considered if liquido_values else 0

    # print("BRUTO values:", bruto_values)
    # print("LIQUIDO values:", liquido_values)
    # print("Total months considered for calculation:", total_months_considered)
    # print("Average BRUTO:", avg_bruto)
    # print("Average LIQUIDO:", avg_liquido)

    return avg_bruto, avg_liquido