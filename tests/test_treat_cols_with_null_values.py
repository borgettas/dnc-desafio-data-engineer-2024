import pandas as pd
import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dags.commons.ingestion.normalization import treat_null_values_to_zero, treat_cols_with_null_values_to_zero


def test_treat_cols_with_null_values_to_zero():
    # Criando um DataFrame de exemplo
    data = {
        'coluna1': [1, None, ' ', 4, 'texto', ''],
        'coluna2': [None, 2, 3, '', 5, ' '],
        'coluna3': [10, 20, 30, 40, 50, 60]  # Coluna que não deve ser alterada
    }
    df = pd.DataFrame(data)

    # Colunas a serem tratadas
    cols_to_treat = ['coluna1', 'coluna2']

    # Aplicando a função
    df_result = treat_cols_with_null_values_to_zero(df, cols_to_treat)

    # Verificando os resultados
    expected_data = {
        'coluna1': [1, 0, 0, 4, 'texto', 0],
        'coluna2': [0, 2, 3, 0, 5, 0],
        'coluna3': [10, 20, 30, 40, 50, 60]  # Deve permanecer inalterada
    }
    expected_df = pd.DataFrame(expected_data)

    # Comparando o DataFrame resultante com o esperado
    pd.testing.assert_frame_equal(df_result, expected_df)
