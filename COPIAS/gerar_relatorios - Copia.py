import os
import centralized_imports
from weasyprint import HTML

# Set environment variables for font configuration (if needed)
os.environ['FONTCONFIG_PATH'] = r'C:\Users\ridim\anaconda3\Library\etc\fonts'

# Define the base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths relative to the base directory
TEMPLATE_DIR = os.path.join(BASE_DIR, 'MODULOS_TERCIARIOS')
OUTPUT_DIR = os.path.join(BASE_DIR, 'RELATORIOS')
template_path = os.path.join(TEMPLATE_DIR, 'report_template.html')

# Image filepaths
image_valores_mensais_reduzido = os.path.join(OUTPUT_DIR, 'valores_mensais_reduzido.png')
image_mercados_pie_chart = os.path.join(OUTPUT_DIR, 'mercados_pie_chart.png')
image_modalidades_pie_chart = os.path.join(OUTPUT_DIR, 'modalidades_pie_chart.png')
image_movimentacoes_mensais_investimentos = os.path.join(OUTPUT_DIR, 'movimentacoes_mensais_investimentos.png')
image_movimentacoes_mensais_mercados = os.path.join(OUTPUT_DIR, 'movimentacoes_mensais_mercados.png')
image_movimentacoes_mensais_modalidades = os.path.join(OUTPUT_DIR, 'movimentacoes_mensais_modalidades.png')
image_rent_rep_investimentos = os.path.join(OUTPUT_DIR, 'rent_rep_investimentos.png')
image_graf_rent_rep_investimentos = os.path.join(OUTPUT_DIR, 'graf_rent_rep_investimentos.png')
image_evol_patr_investimentos = os.path.join(OUTPUT_DIR, 'evol_patr_invest_table.png')

def gerar_relatorio_mensal(parametros_funcoes):
    try:
        print("&" * 90)
        print("THIS IS THE gerar_relatorio_mensal FUNCTION.")

        # Set the locale for Brazilian currency
        centralized_imports.locale.setlocale(centralized_imports.locale.LC_ALL, 'pt_BR.UTF-8')

        # Extract relevant parameters from the function arguments
        year_interest = str(parametros_funcoes.get("year_interest"))
        month_interest = parametros_funcoes.get("month_interest")
        filepath_variacoes_patrimoniais_mensais = parametros_funcoes.get("filepath_variacoes_patrimoniais_mensais")
        filepath_variacoes_patrimoniais_anuais = parametros_funcoes.get("filepath_variacoes_patrimoniais_anuais")
        filepath_movimentacoes_mensais = parametros_funcoes.get("filepath_movimentacoes_mensais")
        filepath_rentabilidade_representatividade = parametros_funcoes.get("filepath_rentabilidade_representatividade")
        filepath_valores_mensais = parametros_funcoes.get("filepath_valores_mensais")
        month_bruto_key = parametros_funcoes.get("month_bruto_key")
        month_liquido_key = parametros_funcoes.get("month_liquido_key")
        month_entrada_key = parametros_funcoes.get("month_entrada_key")
        month_saida_key = parametros_funcoes.get("month_saida_key")
        year_month_interest_start = parametros_funcoes.get("year_month_interest_start")
        year_month_interest_end = parametros_funcoes.get("year_month_interest_end")
        year_month_interest = parametros_funcoes.get("year_month_interest")

        # Load files with error handling
        try:
            variacoes_patrimoniais_mensais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_variacoes_patrimoniais_mensais))
            variacoes_patrimoniais_anuais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                    filepath_variacoes_patrimoniais_anuais))
            valores_mensais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_valores_mensais))
            movimentacoes_mensais = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_movimentacoes_mensais))
            rentabilidade_representatividade = (
                centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(
                filepath_rentabilidade_representatividade))
        except FileNotFoundError as e:
            print(f"Error loading files: {e}")
            return

        # Extract data with error handling and currency formatting
        def safe_extract(key, dictionary, sub_key):
            try:
                return centralized_imports.locale.currency(dictionary[key][sub_key], grouping=True)
            except KeyError:
                print(f"KeyError: {key} or {sub_key} not found.")
                return centralized_imports.locale.currency(0, grouping=True)

        # VALORES POR MERCADO
        investimentos_renda_fixa = safe_extract("RENDA FIXA", valores_mensais, month_bruto_key)
        investimentos_renda_variavel = safe_extract("RENDA VARIAVEL", valores_mensais, month_bruto_key)
        investimentos_COE = safe_extract("COE", valores_mensais, month_bruto_key)
        investimentos_FI = safe_extract("FUNDOS DE INVESTIMENTO", valores_mensais, month_bruto_key)

        # VALORES POR MODALIDADE
        investimentos_cdb = safe_extract("CDB", valores_mensais, month_bruto_key)
        investimentos_cra = safe_extract("CRA", valores_mensais, month_bruto_key)
        investimentos_deb = safe_extract("DEBENTURES", valores_mensais, month_bruto_key)
        investimentos_lca = safe_extract("LCA", valores_mensais, month_bruto_key)
        investimentos_lci = safe_extract("LCI", valores_mensais, month_bruto_key)
        investimentos_acoes = safe_extract("ACOES", valores_mensais, month_bruto_key)
        investimentos_fundos_imobiliarios = safe_extract("FUNDOS IMOBILIARIOS", valores_mensais, month_bruto_key)
        investimentos_carteiras_recomendadas = safe_extract("CARTEIRAS RECOMENDADAS", valores_mensais, month_bruto_key)

        # VALORES PATRIMONIO
        patrimonio_total_bruto = safe_extract("TOTAL", valores_mensais, month_bruto_key)
        patrimonio_total_liquido = safe_extract("TOTAL", valores_mensais, month_liquido_key)

        # MOVIMENTACOES POR MERCADO
        # --------------------------------
        # Entrada
        movimentacoes_entrada_renda_fixa = (
            safe_extract("RENDA FIXA", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_renda_variavel = (
            safe_extract("RENDA VARIAVEL", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_COE = (
            safe_extract("COE", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_FI = (
            safe_extract("FUNDOS DE INVESTIMENTO", movimentacoes_mensais, month_entrada_key))
        # --------------------------------
        # Saida
        movimentacoes_saida_renda_fixa = (
            safe_extract("RENDA FIXA", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_renda_variavel = (
            safe_extract("RENDA VARIAVEL", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_COE = (
            safe_extract("COE", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_FI = (
            safe_extract("FUNDOS DE INVESTIMENTO", movimentacoes_mensais, month_saida_key))

        # MOVIMENTACOES POR MODALIDADE
        # --------------------------------
        # Entrada
        movimentacoes_entrada_cdb = (
            safe_extract("CDB", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_cra = (
            safe_extract("CRA", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_deb = (
            safe_extract("DEBENTURES", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_lca = (
            safe_extract("LCA", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_lci = (
            safe_extract("LCI", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_acoes = (
            safe_extract("ACOES", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_fundos_imobiliarios = (
            safe_extract("FUNDOS IMOBILIARIOS", movimentacoes_mensais, month_entrada_key))
        movimentacoes_entrada_carteiras_recomendadas = (
            safe_extract("CARTEIRAS RECOMENDADAS", movimentacoes_mensais, month_entrada_key))
        # --------------------------------
        # Saida
        movimentacoes_saida_cdb = (
            safe_extract("CDB", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_cra = (
            safe_extract("CRA", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_deb = (
            safe_extract("DEBENTURES", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_lca = (
            safe_extract("LCA", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_lci = (
            safe_extract("LCI", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_acoes = (
            safe_extract("ACOES", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_fundos_imobiliarios = (
            safe_extract("FUNDOS IMOBILIARIOS", movimentacoes_mensais, month_saida_key))
        movimentacoes_saida_carteiras_recomendadas = (
            safe_extract("CARTEIRAS RECOMENDADAS", movimentacoes_mensais, month_saida_key))
        # --------------------------------
        # Saida
        movimentacao_total_entrada = (
            safe_extract("TOTAL", movimentacoes_mensais,month_entrada_key))
        movimentacao_total_saida = (
            safe_extract("TOTAL", movimentacoes_mensais, month_saida_key))

        # RENTABILIDADE POR MERCADO
        # Extract and format data with error handling (Rentabilidade formatted as percentage)
        def safe_extract_percent(key, dictionary, sub_key):
            try:
                value = dictionary[key][sub_key] * 100  # Multiply by 100 to convert to percentage
                return f"{value:.2f}%"
            except KeyError:
                return "0.00%"

        # Rentabilidade
        rentabilidade_renda_fixa = safe_extract_percent("RENDA FIXA", rentabilidade_representatividade,
                                                        "RENTABILIDADE ANUAL MEDIA")

        rentabilidade_renda_variavel = safe_extract_percent("RENDA VARIAVEL", rentabilidade_representatividade,
                                                        "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_fundos_investimento = safe_extract_percent("FUNDOS DE INVESTIMENTO", rentabilidade_representatividade,
                                                            "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_fundos_investimento = safe_extract_percent("FUNDOS DE INVESTIMENTO",
                                                                 rentabilidade_representatividade,
                                                                 "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_coe = safe_extract_percent("COE", rentabilidade_representatividade,
                                                                 "RENTABILIDADE ANUAL MEDIA")
        rentabilidade_cra = safe_extract_percent("CRA", rentabilidade_representatividade,
                                                 "RENTABILIDADE ANUAL MEDIA")



        representatividade_renda_fixa = safe_extract_percent("RENDA FIXA", rentabilidade_representatividade,
                                                        "REPRESENTATIVIDADE")

        representatividade_renda_variavel = safe_extract_percent("RENDA VARIAVEL", rentabilidade_representatividade,
                                                            "REPRESENTATIVIDADE")
        representatividade_fundos_investimento = safe_extract_percent("FUNDOS DE INVESTIMENTO",
                                                                 rentabilidade_representatividade,
                                                                 "REPRESENTATIVIDADE")
        representatividade_fundos_investimento = safe_extract_percent("FUNDOS DE INVESTIMENTO",
                                                                 rentabilidade_representatividade,
                                                                 "REPRESENTATIVIDADE")
        representatividade_coe = safe_extract_percent("COE", rentabilidade_representatividade,
                                                 "REPRESENTATIVIDADE")
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # EVOLUCAO PATRIMONIAL POR MERCADO
        evolucao_renda_fixa = safe_extract("RENDA FIXA", variacoes_patrimoniais_mensais, month_interest)
        evolucao_renda_variavel = safe_extract("RENDA VARIAVEL", variacoes_patrimoniais_mensais, month_interest)
        evolucao_COE = safe_extract("COE", variacoes_patrimoniais_mensais, month_interest)
        evolucao_FI = safe_extract("FUNDOS DE INVESTIMENTO", variacoes_patrimoniais_mensais, month_interest)

        # EVOLUCAO PATRIMONIAL POR MODALIDADE
        evolucao_cdb = safe_extract("CDB", variacoes_patrimoniais_mensais, month_interest)
        evolucao_cra = safe_extract("CRA", variacoes_patrimoniais_mensais, month_interest)
        evolucao_deb = safe_extract("DEBENTURES", variacoes_patrimoniais_mensais, month_interest)
        evolucao_lca = safe_extract("LCA", variacoes_patrimoniais_mensais, month_interest)
        evolucao_lci = safe_extract("LCI", variacoes_patrimoniais_mensais, month_interest)
        evolucao_acoes = safe_extract("ACOES", variacoes_patrimoniais_mensais, month_interest)
        evolucao_fundos_imobiliarios = safe_extract("FUNDOS IMOBILIARIOS", variacoes_patrimoniais_mensais, month_interest)
        evolucao_carteiras_recomendadas = safe_extract("CARTEIRAS RECOMENDADAS", variacoes_patrimoniais_mensais, month_interest)

        # TOTAL EVOLUCAO PATRIMONIAL
        evolucao_total = safe_extract("TOTAL", variacoes_patrimoniais_mensais, month_interest)
        evolucao_total_acumulada = (
            safe_extract("TOTAL", variacoes_patrimoniais_anuais, "TOTAL INTERESSE"))
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        # Open the template file with error handling
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                template = file.read()
                print(f"Loaded HTML template from: {template_path}")
        except FileNotFoundError:
            print(f"Template file not found: {template_path}")
            return

        # Replace backslashes with forward slashes in the image path
        image_valores_mensais_reduzido_corrected = image_valores_mensais_reduzido.replace("\\", "/")
        image_mercados_pie_chart_corrected = image_mercados_pie_chart.replace("\\", "/")
        image_modalidades_pie_chart_corrected = image_modalidades_pie_chart.replace("\\", "/")
        image_movimentacoes_mensais_investimentos_corrected = image_movimentacoes_mensais_investimentos.replace("\\", "/")
        image_movimentacoes_mensais_mercados_corrected = image_movimentacoes_mensais_mercados.replace("\\","/")
        image_movimentacoes_mensais_modalidades_corrected = image_movimentacoes_mensais_modalidades.replace("\\", "/")
        image_rent_rep_investimentos_corrected = image_rent_rep_investimentos.replace("\\", "/")
        image_graf_rent_rep_investimentos_corrected = image_graf_rent_rep_investimentos.replace("\\", "/")
        image_evol_patr_investimentos_corrected = image_evol_patr_investimentos.replace("\\", "/")

        # Replace placeholders with the correct image paths
        report_content = template.replace('{{ image_valores_mensais_reduzido }}',
                                          f'file:///{image_valores_mensais_reduzido_corrected}')
        report_content = report_content.replace('{{ image_mercados_pie_chart }}',
                                                f'file:///{image_mercados_pie_chart_corrected}')
        report_content = report_content.replace('{{ image_modalidades_pie_chart }}',
                                                f'file:///{image_modalidades_pie_chart_corrected}')
        report_content = report_content.replace('{{ image_movimentacoes_mensais_investimentos }}',
                                                f'file:///{image_movimentacoes_mensais_investimentos_corrected}')
        report_content = report_content.replace('{{ image_movimentacoes_mensais_mercados }}',
                                                f'file:///{image_movimentacoes_mensais_mercados_corrected}')
        report_content = report_content.replace('{{ image_movimentacoes_mensais_modalidades }}',
                                                f'file:///{image_movimentacoes_mensais_modalidades_corrected}')
        report_content = report_content.replace('{{ image_rent_rep_investimentos }}',
                                                f'file:///{image_rent_rep_investimentos_corrected}')
        report_content = report_content.replace('{{ image_graf_rent_rep_investimentos }}',
                                                f'file:///{image_graf_rent_rep_investimentos_corrected}')
        report_content = report_content.replace('{{ image_evol_patr_invest_table }}',
                                                f'file:///{image_evol_patr_investimentos_corrected}')

        # Prepare data for template rendering
        data = {
            "year_month_interest_end": year_month_interest_end,
            "investimentos_renda_fixa": investimentos_renda_fixa,
            "investimentos_renda_variavel": investimentos_renda_variavel,
            "investimentos_FI": investimentos_FI,
            "investimentos_COE": investimentos_COE,
            "investimentos_cdb": investimentos_cdb,
            "investimentos_cra": investimentos_cra,
            "investimentos_deb": investimentos_deb,
            "investimentos_lca": investimentos_lca,
            "investimentos_lci": investimentos_lci,
            "investimentos_fundos_imobiliarios": investimentos_fundos_imobiliarios,
            "investimentos_acoes": investimentos_acoes,
            "investimentos_carteiras_recomendadas": investimentos_carteiras_recomendadas,
            "movimentacoes_entrada_renda_fixa": movimentacoes_entrada_renda_fixa,
            "movimentacoes_entrada_renda_variavel": movimentacoes_entrada_renda_variavel,
            "movimentacoes_entrada_FI": movimentacoes_entrada_FI,
            "movimentacoes_entrada_COE": movimentacoes_entrada_COE,
            "movimentacoes_saida_renda_fixa": movimentacoes_saida_renda_fixa,
            "movimentacoes_saida_renda_variavel": movimentacoes_saida_renda_variavel,
            "movimentacoes_saida_FI": movimentacoes_saida_FI,
            "movimentacoes_saida_COE": movimentacoes_saida_COE,
            "investimentos_cdb": investimentos_cdb,
            "movimentacoes_entrada_cra": movimentacoes_entrada_cra,
            "movimentacoes_entrada_deb": movimentacoes_entrada_deb,
            "movimentacoes_entrada_lca": movimentacoes_entrada_lca,
            "movimentacoes_entrada_lci": movimentacoes_entrada_lci,
            "movimentacoes_entrada_fundos_imobiliarios": movimentacoes_entrada_fundos_imobiliarios,
            "movimentacoes_entrada_acoes": movimentacoes_entrada_acoes,
            "movimentacoes_entrada_carteiras_recomendadas": movimentacoes_entrada_carteiras_recomendadas,
            "movimentacoes_saida_cra": movimentacoes_saida_cra,
            "movimentacoes_saida_deb": movimentacoes_saida_deb,
            "movimentacoes_saida_lca": movimentacoes_saida_lca,
            "movimentacoes_saida_lci": movimentacoes_saida_lci,
            "movimentacoes_saida_fundos_imobiliarios": movimentacoes_saida_fundos_imobiliarios,
            "movimentacoes_saida_acoes": movimentacoes_saida_acoes,
            "movimentacoes_saida_carteiras_recomendadas": movimentacoes_saida_carteiras_recomendadas,
            "movimentacao_total_entrada": movimentacao_total_entrada,
            "movimentacao_total_saida": movimentacao_total_saida,
            "patrimonio_total_bruto": patrimonio_total_bruto,
            "patrimonio_total_liquido": patrimonio_total_liquido,
            "rentabilidade_renda_fixa": rentabilidade_renda_fixa,
            "rentabilidade_renda_variavel": rentabilidade_renda_variavel,
            "rentabilidade_fundos_investimentos": rentabilidade_fundos_investimento,
            "rentabilidade_coe": rentabilidade_coe,
            "rentabilidade_cra": rentabilidade_cra,
            "rentabilidade_renda_variavel": rentabilidade_renda_variavel,
            "evolucao_renda_fixa": evolucao_renda_fixa,
            "evolucao_renda_variavel": evolucao_renda_variavel,
            "evolucao_FI": evolucao_FI,
            "evolucao_COE": evolucao_COE,
            "evolucao_cdb": evolucao_cdb,
            "evolucao_cra": evolucao_cra,
            "evolucao_deb": evolucao_deb,
            "evolucao_lca": evolucao_lca,
            "evolucao_lci": evolucao_lci,
            "evolucao_fundos_imobiliarios": evolucao_fundos_imobiliarios,
            "evolucao_acoes": evolucao_acoes,
            "evolucao_carteiras_recomendadas": evolucao_carteiras_recomendadas,
            "evolucao_total": evolucao_total,
            "evolucao_total_acumulada": evolucao_total_acumulada

        }

        # Render the template with data
        rendered_text = centralized_imports.Template(report_content).render(data)

        # Output the rendered text (for debugging purposes)
        print("-" * 90)
        print("Rendered HTML content:\n")
        print(rendered_text)
        print("-" * 90)

        # Generate PDF if requested
        generate_pdf = True
        if generate_pdf:
            try:
                # Save the final report
                pdf_filename = f"{year_month_interest_end}_relatorio_mensal.pdf"
                output_path = os.path.join(OUTPUT_DIR, pdf_filename)

                # Generate the PDF
                HTML(string=rendered_text).write_pdf(output_path)

                print(f"PDF report generated: {output_path}")
            except Exception as e:
                print(f"Error generating PDF: {e}")

    except Exception as e:
        print(f"An error occurred in gerar_relatorio_mensal: {e}")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




