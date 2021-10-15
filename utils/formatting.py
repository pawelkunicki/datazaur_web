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



def color_cell(x):
    sign = str(x)[0]
    if sign == '-':
        color = 'red'
        pref = ''
    else:
        color = 'green'
        pref = '+'
    if '%' in str(x):
        return f"""<p class={color}>({pref}{x})</p>"""
    else:
        return f"""<p class={color}>{pref}{x}</p>"""


def prepare_df_display(df, n_decimals=3):
    for col in df.columns:
        if 'Price' in col or 'Δ' in col or 'vol' in col or 'cap' in col or 'Supply' in col:
            df[col] = df[col].apply(lambda x: format(float(x.replace(',', '')).__round__(n_decimals), ',') if type(x) == str else
                                    format(float(x).__round__(n_decimals), ','))
            if 'Δ' in col:
                df[col] = df[col].apply(color_cell)

    if 'Url' in df.columns:
        df = add_hyperlinks(df)
        df.drop('Url', inplace=True, axis=1)

    if 'Updated' in df.columns:
        df['Updated'] = df['Updated'].apply(lambda x: pd.to_datetime(x * 10 ** 9))
    return df




def prepare_df_save(df):
    df.columns = ['Symbol', 'Name', 'Url', 'Price', '24h Δ', '1h %Δ', '24h %Δ', '24h vol', f'Market cap ({CURRENCY})',
                  'Supply', 'Updated']
    df.dropna(inplace=True)
    df.iloc[:, 7:9] = df.iloc[:, 7:9].astype('int64')
    return df



