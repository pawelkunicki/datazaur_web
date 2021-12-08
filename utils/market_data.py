import requests
from utils.compare_timestamps import *
from utils.decorators import load_or_save
import investpy
import datetime
from data.default_countries import DEFAULT_COUNTRIES
from data.default_indices import GENERAL_INDICES
from .formatting import *


CRYPTOCOMPARE_KEY = os.environ.get('CRYPTOCOMPARE_KEY')
REFRESH_RATE = 600
COLUMNS = ['Instrument', 'Price', '24h Δ', '24h %Δ']
RESULT_DF = pd.DataFrame(columns=COLUMNS)
CURRENCY = settings.DEFAULT_CURRENCY
TENOR = '10Y'


def all_markets_data(refresh_rate=REFRESH_RATE):
    data = {}
    coins_data = prep_market_df(coins_by_mcap())
    data['crypto'] = coins_data.to_html(escape=False, justify='center')

    forex = get_fx_rates(CURRENCY)
    data['forex'] = prep_market_df(forex).to_html(escape=False, justify='center')

    indices = get_indices_table()
    data['indices'] = prep_market_df(indices).to_html(escape=False, justify='center')

    yields = get_yields_table(TENOR)
    data['yields'] = prep_market_df(yields).to_html(escape=False, justify='center')

    commodities_file = 'commodities.csv'
    if compare_timestamps(refresh_rate, commodities_file):
        data['commodities'] = pd.read_csv(commodities_file, index_col=0)
    else:
        commodities = get_commodities()
        data['commodities'] = commodities
    return data


def check_indices_files():
    return


@load_or_save('indices.csv', 1800)
def get_indices_table():
    indices = GENERAL_INDICES
    result = pd.DataFrame(columns=['Index', 'Price', '24h Δ', '24h %Δ'])
    for k, v in indices.items():
        for indx in v:
            try:
                data = investpy.get_index_recent_data(indx, k)['Close'].iloc[-2:]
                diff = (data[1] - data[0]).__round__(2)
                diff_pct = (100 * diff / data[0]).__round__(2)
                result.loc[len(result)] = {'Index': f"""{indx} <br> ({k.title()})""",
                                           'Price': data[1],
                                           '24h Δ': diff,
                                           '24h %Δ': diff_pct}
            except Exception as e:
                print(f'error {e}')

    result.iloc[:, 1] = result.iloc[:, 1].astype(float).round(2)
    return result


@load_or_save('yields.csv', 1800)
def get_yields_table(tenor='10Y'):
    result = pd.DataFrame(columns=['Bond', 'Yield', '24h Δ', '24h %Δ'])
    today = datetime.date.today()
    n_days_diff = find_days_diff(today)
    start_date = today - datetime.timedelta(days=n_days_diff)
    end_date = today - datetime.timedelta(days=n_days_diff-1)
    start_date = datetime.datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%d/%m/%Y")
    end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%d/%m/%Y")
    if 'yields.csv' in os.listdir():
        countries = [bond.split(' 10')[0] for bond in pd.read_csv('yields.csv', index_col=0)['Bond']]
    else:
        countries = investpy.get_bond_countries()
    for country in countries:
        bond = country + ' ' + tenor
        try:
            data = investpy.get_bond_historical_data(f'{bond}', from_date=start_date, to_date=end_date).iloc[-2:]
            diff = data['Close'].iloc[1] - data['Close'].iloc[0]
            diff_pct = 100 * diff / data['Close'].iloc[0]
            result.loc[len(result)] = [bond.title(), data['Close'].iloc[-1], diff, diff_pct]
        except Exception as e:
            print(f'error {e}')

    return result


def find_days_diff(today):
    if today.isoweekday() == 6:
        return 2
    elif today.isoweekday() == 7:
        return 3
    elif today.isoweekday() == 1:
        return 4
    else:
        return 1



def get_yield_curves():
    result = {}
    countries = DEFAULT_COUNTRIES
    for country in countries:
        try:
            data = investpy.get_bonds_overview(country)[['name', 'last', 'change']]
            data.columns = ['Bond', 'Yield', '24h Δ']
            result[country] = data.to_html()
            print(result)
        except Exception as e:
            print(f'error {e}')

    print(result)
    #pd.DataFrame(result).to_csv('yield_curves.csv')
    return result



def get_commodities():
    cols = ['name', 'country', 'last', 'change', 'change_percentage', 'currency']
    result_cols = ['Instrument', 'Price', '24h Δ', '24h %Δ']
    result = pd.DataFrame(columns=result_cols)
    groups = investpy.get_commodity_groups()
    tables = {}
    for group in groups:
        table = investpy.get_commodities_overview(group)[cols]
        table['Instrument'] = table['name'] + '<br>' + table['country'].astype(str).apply(lambda x: '' if x == 'None' else x.title())
        table['Price'] = table['last'].astype(str) + '<br> (' + table['currency'].astype(str) + ')'
        table = table[['Instrument', 'Price', 'change', 'change_percentage']]
        table.columns = result_cols
        tables[group] = table.to_html(escape=False, justify='center')
    #result.iloc[:, 2] = result.iloc[:, 2].apply(color_cell)
    return tables


@load_or_save('forex.csv', 1800)
def get_fx_rates(base_currency):
    return investpy.get_currency_crosses_overview(base_currency)[['symbol', 'bid', 'change', 'change_percentage']]


def get_coins_info():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={CRYPTOCOMPARE_KEY}'
    data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
                                                                       'FullName', 'Description', 'Algorithm',
                                                                       'ProofType', 'TotalCoinsMined',
                                                                       'CirculatingSupply', 'MaxSupply',
                                                                       'BlockReward', 'AssetWebsiteUrl',
                                                                       'IsUsedInDefi', 'IsUsedInNft']]
    return data



@load_or_save('crypto_small.csv', 600)
def coins_by_mcap():
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=50&tsym={CURRENCY}&api_key={CRYPTOCOMPARE_KEY}'
    cols = f'CoinInfo.Name RAW.{CURRENCY}.PRICE RAW.{CURRENCY}.CHANGE24HOUR RAW.{CURRENCY}.CHANGEPCT24HOUR'.split()
    df = pd.json_normalize(requests.get(url).json()['Data'])[cols]
    df.columns = ['Symbol', 'Price', '24h Δ', '24h %Δ']
    return df


def prep_market_df(df, n_decimals=3):
    df.columns = ['Symbol', 'Price', '24h Δ'] if len(df.columns) == 3 else ['Symbol', 'Price', '24h Δ', '24h %Δ']
    df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: float(str(x).replace('%', '').replace('+', ''))).round(n_decimals).applymap(lambda x: format(x, ','))
    df['24h %Δ'] = df['24h %Δ'].apply(lambda x: f'{x}%')
    df.iloc[:, 2:] = df.iloc[:, 2:].applymap(color_cell)
    df.iloc[:, 2] = df.iloc[:, 2].astype(str) + '<br>' + df.iloc[:, 3].astype(str)
    return df.iloc[:, :-1]








