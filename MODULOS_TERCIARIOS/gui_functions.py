import centralized_imports
import numpy as np
import locale

# Set the locale for Brazilian currency
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def show_dictionary_window(caminho_arquivo):
    print()
    print("&" * 90)
    print("THIS IS THE show_dictionary_window FUNCTION:")

    filepath_dictionary = caminho_arquivo
    # print()
    # print("filepath_dictionary = ", filepath_dictionary)

    arquivo_pickle_restaurado = (
        centralized_imports.arquivos_functions.ArquivosFunctions.abrir_arquivo_pickle(filepath_dictionary))

    window = centralized_imports.tk.Toplevel()
    window.title("Dictionary Display")
    window.geometry("1000x600")
    window.configure(bg="#F5ECD2")  # Set background to sepia

    style = centralized_imports.ttk.Style()
    style.configure("Treeview", background="#F5ECD2", foreground="black", rowheight=25, fieldbackground="#F5ECD2", font=("Arial", 14))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#D2B48C")
    style.map('Treeview', background=[('selected', '#D3D3D3')])

    tree = centralized_imports.ttk.Treeview(window, style="Treeview")

    # Select the correct headers based on the file path
    if filepath_dictionary == centralized_imports.investimentos_btg.filepaths_dictionary.get("filepath_valores_mensais_2020"):
        headers_order = centralized_imports.investimentos_btg.mapa_cabecalhos.get("valores_mensais")
        print("headers_order for valores mensais = ", headers_order)
    elif filepath_dictionary == centralized_imports.investimentos_btg.filepaths_dictionary.get("filepath_movimentacoes_mensais_2020"):
        headers_order = centralized_imports.investimentos_btg.mapa_cabecalhos.get("movimentacoes_mensais")
        print("headers_order for movimentacoes mensais = ", headers_order)
    elif filepath_dictionary == centralized_imports.investimentos_btg.filepaths_dictionary.get("filepath_saldos_anuais_rentabilidade"):
        headers_order = centralized_imports.investimentos_btg.mapa_cabecalhos.get("saldos_anuais_rentabilidade")
        print("headers_order for saldos anuais rentabilidade = ", headers_order)
    else:
        headers_order = list(arquivo_pickle_restaurado[next(iter(arquivo_pickle_restaurado))].keys())

    # Extract all unique headers (nested keys) and ensure order
    headers = {header: '' for header in headers_order}
    # print("headers dict = ", headers)
    for main_key, nested_dict in arquivo_pickle_restaurado.items():
        for key in nested_dict.keys():
            if key not in headers:
                headers[key] = ''  # Add any extra headers not in predefined order

    headers = list(headers.keys())  # Convert to list to maintain order
    # print("headers list = ", headers)

    # Define columns for Treeview
    tree["columns"] = headers

    # Set up column headings
    for col in headers:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='w')

    # Insert data into Treeview with alternating row colors
    for index, (main_key, nested_dict) in enumerate(arquivo_pickle_restaurado.items()):
        row_data = [locale.currency(nested_dict.get(header, 0), grouping=True) if isinstance(nested_dict.get(header), (int, float)) else nested_dict.get(header, '') for header in headers]
        tag = 'oddrow' if index % 2 == 0 else 'evenrow'
        tree.insert("", "end", text=main_key, values=row_data, tags=(tag,))

    tree.tag_configure('oddrow', background='#F5ECD2')
    tree.tag_configure('evenrow', background='#E0D5C4')

    tree.pack(pady=10, expand=True, fill='both')

    # Add vertical scrollbar
    y_scrollbar = centralized_imports.ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=y_scrollbar.set)

    # Add horizontal scrollbar
    x_scrollbar = centralized_imports.ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=x_scrollbar.set)

    window.mainloop()

