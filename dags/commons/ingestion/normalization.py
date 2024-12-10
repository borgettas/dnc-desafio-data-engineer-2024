import pandas as pd


def treat_null_values_to_zero(value: any):
    return 0 if value in ['', ' ', None] else value


def treat_cols_with_null_values_to_zero(df, cols):
    for col in cols:
        df[col] = df[col].apply(treat_null_values_to_zero)

    return df