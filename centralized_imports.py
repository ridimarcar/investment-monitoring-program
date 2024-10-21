
# --------------------------------------------------------------
# STANDARD LIBRARIES
import calendar
import collections
import copy
import datetime
import io
import json
import locale
import math
import os
import pickle
import pprint
import shutil
import sys
from collections import ChainMap
from locale import setlocale
from pathlib import Path


# --------------------------------------------------------------
# THIRD-PARTY LIBRARIES
import jinja2
from jinja2 import Template
import numpy as np
import pandas as pd
import pandas_ods_reader as odr
import weasyprint
from weasyprint import HTML
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import matplotlib.ticker as ticker


# --------------------------------------------------------------
# CUSTOM MODULES

from MODULOS_PRIMARIOS import (
    arquivos_functions,
    atualizar_valores_mensais,
    criar_dicionarios_padronizados
)

from MODULOS_SECUNDARIOS import (
    atualizar_movimentacoes_anuais,
    atualizar_movimentacoes_mensais,
    atualizar_variacoes_patrimoniais_anuais,
    atualizar_variacoes_patrimoniais_mensais,
    gerar_dados_historicos,
    general_functions,
    gerar_relatorios,
    historico_movimentacoes_mensais,
    investimentos_btg,
    investimentos_functions,
    rentabilidade_representatividade,
    somar_movimentacoes_mensais,
    somar_valores_mensais,
    somar_variacoes_patrimoniais_mensais,
    year_month_interest
)

from MODULOS_TERCIARIOS import (
    gui_functions,
    gerar_graficos,
    gerar_tabelas
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++

# Ensure the path to custom modules is included
sys.path.append(r'C:\Users\ridim\OneDrive\PYTHON\PYTHON MODULES')
