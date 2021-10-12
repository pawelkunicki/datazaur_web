from django.conf import settings
import pandas as pd

CURRENCY = settings.DEFAULT_CURRENCY
URL = settings.BASE_CRYPTOCOMPARE_URL

def round_number(x, n):
    x2 = float(x.replace('%', '').replace('+', '')) if type(x) == str else x
    return x2.__round__(n)



def add_hyperlinks(df):
    for col in ['Symbol', 'Name']:
        df[col] = df.apply(lambda x: f"""<a href={URL + x['Url']}>{x[col]}</a>""", axis=1)
    return df

def add_yields_hyperlinks(x):
    return f"""<a href='/yield_curves?country={x}'> {x.title()} </a>"""


def string_to_float(x):
    if type(x) == str:
        return float(x.replace('%', '').replace('+', ''))

def round_strings(cell):
    abs_integer = cell.split()[0].split('.')[0]
    abs_decimal = cell.split()[0].split('.')[1]

    pct_integer = cell.split()[1].split('.')[0]
    pct_decimal = cell.split()[1].split('.')[1]

    return f'{abs_integer}.{abs_decimal[:3]} ({pct_integer}.{pct_decimal[:3]})%'


def color_cell(x):
    if '-' in str(x):
        color = 'red'
    else:
        color = 'green'
    return f"""<p class={color}>{x}</p>"""

def prepare_df_display(df):
    df.iloc[:, 3:] = df.iloc[:, 3:].astype('float64').round(3)

    df.iloc[:, 3:] = df.iloc[:, 3:].applymap(lambda x: format(x, ','))

    delta_cols = [col for col in df.columns if 'Δ' in col]
    if delta_cols:
        df[delta_cols] = df[delta_cols].applymap(color_cell)

    df = add_hyperlinks(df)
    if 'Url' in df.columns:
        df.drop('Url', inplace=True, axis=1)
    if 'Updated' in df.columns:
        df['Updated'] = df['Updated'].apply(lambda x: pd.to_datetime(x * 10 ** 9))
    return df


def set_dtypes(df, **kwargs):
    for k, v in kwargs.items():
        print(df)
        print(k)
        print(v)
        for col_n in v:
            df.iloc[:, col_n] = df.iloc[:, col_n].astype(k)
    return df


def prepare_df_save(df):
    df.columns = ['Symbol', 'Name', 'Url', 'Price', '24h Δ', '1h %Δ', '24h %Δ', '24h vol', f'Market cap ({CURRENCY})',
                  'Supply', 'Updated']
    df.dropna(inplace=True)
    df.iloc[:, 7:9] = df.iloc[:, 7:9].astype('int64')
    return df



