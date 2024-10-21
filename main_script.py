# PROGRAMA DE ATUALIZACAO MODULOS_SECUNDARIOS
# ===========================================================================

# CHAPTER 1: IMPORT RELEVANT LIBRARIES
# ===========================================================================
import centralized_imports
import tkinter as tk
from tkinter import ttk

# CHAPTER 2: LOAD CONFIGURATION FILE
# ===========================================================================
filepath_config_json = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\config\config.json"
config = centralized_imports.arquivos_functions.ArquivosFunctions.load_config(filepath_config_json)

# CHAPTER 3: DEFINE GLOBAL VARIABLES AND CONSTANTS
# ===========================================================================
arquivos_actions_list = [
    "Exibir arquivo pickle",
    "Exibir arquivo de seguranca"
]

investimentos_actions_list = [
    "Atualizar valores mensais",
    "Somar valores mensais",
    "Calcular valores mensais medios",
    "Atualizar movimentacoes mensais",
    "Atualizar saldos anuais e rentabilidade",
    "Calcular evolucao patrimonial",
    "Calcular rentabilidade mercados modalidades",
    "Editar investimentos",
    "Preencher entradas vazias",
    "Apagar investimento",
    "Editar chaves dicionario",
    "Acrescentar chave dicionario",
    "Apagar chaves dicionario"
]

# CHAPTER 4: CREATE THE ATUALIZACAO MODULOS_SECUNDARIOS PANEL CLASS
# ===========================================================================================
class AtualizacaoInvestimentosPanel:
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.arquivos_actions_list = arquivos_actions_list
        self.investimentos_actions_list = investimentos_actions_list
        self.setup_gui_first_part()
        self.binding_gui_functions()
        # Automatically select the default action if provided in config
        default_action = self.config.get("default_investimentos_action")
        if default_action and default_action in self.investimentos_actions_list:
            self.execute_action(default_action, "investimentos")

    def setup_gui_first_part(self):
        """Set up the initial GUI components."""
        self.parent.title("PAINEL DE ATUALIZACAO DE MODULOS_SECUNDARIOS")
        self.label = tk.Label(self.parent,
                              text="====== PAINEL DE ATUALIZACAO DE MODULOS_SECUNDARIOS ======",
                              font=("Tahoma", 16, "bold"),
                              bg="#6600ff",
                              fg="white")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)
        self.create_listboxes()

    def create_listboxes(self):
        """Create listboxes for the GUI."""
        self.arquivos_actions_listbox = self.create_listbox("O QUE VOCE DESEJA FAZER?", self.arquivos_actions_list, row=1, column=0)
        self.investimentos_actions_listbox = self.create_listbox("O QUE VOCE DESEJA FAZER?", self.investimentos_actions_list, row=1, column=1)

    def create_listbox(self, label_text, items_list, row, column):
        """Helper function to create a listbox with a label."""
        label = tk.Label(self.parent, text=label_text, font=("Tahoma", 14, "bold"), bg="#FFCCFF")
        label.grid(row=row, column=column, pady=10)
        listbox = tk.Listbox(self.parent,
                             selectmode=tk.SINGLE,
                             height=len(items_list),
                             exportselection=0,
                             font=("Tahoma", 12, "bold"), bg="#FFCCFF")
        max_width = max(len(item) for item in items_list)
        listbox.config(width=max_width + 2)
        for item in items_list:
            listbox.insert(tk.END, item)
        listbox.grid(row=row+1, column=column, pady=10)
        return listbox

    def binding_gui_functions(self):
        """Bind GUI listbox selections to their respective functions."""
        self.arquivos_actions_listbox.bind('<<ListboxSelect>>', self.on_arquivos_action_select)
        self.investimentos_actions_listbox.bind('<<ListboxSelect>>', self.on_investimentos_action_select)

    def on_arquivos_action_select(self, event):
        """Handle selection of actions from the 'arquivos' listbox."""
        selected_index = self.arquivos_actions_listbox.curselection()[0]
        selected_action = self.arquivos_actions_list[selected_index]
        # Perform the chosen action
        if selected_action == "Exibir arquivo pickle":
            filepath_pickle = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2020.pickle"
            centralized_imports.arquivos_functions.ArquivosFunctions.exibir_arquivo_pickle(filepath_pickle)

        elif selected_action == "Chamar ano mes interesse":
            pass

    def on_investimentos_action_select(self, event):
        """Handle selection of actions from the 'investimentos' listbox."""
        selected_index = self.investimentos_actions_listbox.curselection()[0]
        selected_action = self.investimentos_actions_list[selected_index]
        self.execute_action(selected_action, "investimentos")

    def execute_action(self, selected_action, action_type):
        """Execute the given action."""
        print(f"Executing action: {selected_action} of type: {action_type}")
        # Perform the chosen action
        if action_type == "investimentos":
            if selected_action == "Atualizar valores mensais":
                dictionary = centralized_imports.atualizar_valores_mensais.atualizar_valores_mensais(self.config)
                # centralized_imports.gui_functions.show_dictionary_window(dictionary)

            elif selected_action == "Editar investimentos":
                centralized_imports.investimentos_functions.InvestimentosFunctions.editar_investimentos()

            elif selected_action == "Preencher entradas vazias":
                print("Calling preencher_entradas_vazias")
                centralized_imports.investimentos_functions.InvestimentosFunctions.preencher_entradas_vazias()

            elif selected_action == "Apagar chaves dicionario":
                filepath_pickle = r"C:\Users\ridim\OneDrive\FINANCE\FINANCAS_INVESTIMENTOS\ARQUIVOS PICKLE\valores_mensais_2020.pickle"
                centralized_imports.investimentos_functions.InvestimentosFunctions.apagar_chaves_dicionario(filepath_pickle)

# # Define show_dictionary_window outside the class
# centralized_imports.gui_functions.show_dictionary_window()


# CHAPTER 5: INITIALIZE AND RUN THE APPLICATION
# ===========================================================================================
if __name__ == "__main__":
    # Create the main Tkinter window
    parent = tk.Tk()
    # Create an instance of the InvestimentosPanel class
    invest_panel = AtualizacaoInvestimentosPanel(parent, config)
    # Start the main event loop
    parent.mainloop()
