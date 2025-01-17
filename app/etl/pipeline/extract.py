import yfinance as yf
from typing import Set

def extract_stock_data(ticker: Set[str], start_date: str = None, end_date: str = None):
    """
    Extrai dados históricos de ações para um ticker específico.
    """
    df_extract_data = yf.download(ticker, start=start_date, end=end_date, actions=True)

    # Remove ativos sem todos os dados (invalidos)
    df_extract_data.dropna(axis=1, how='all', inplace=True)

    asset_selected = {column[1] for column in df_extract_data.columns}

    difference_ticker = ticker.difference(asset_selected)
    if difference_ticker:
        print(f"Ativos invalidos: {difference_ticker}")

    if len(asset_selected) < 0:
        raise ValueError("Não há ativos para proseguir com a transformação")

    dict_asset_process = process_yfinance_data(asset_selected)

    return df_extract_data, dict_asset_process

def process_yfinance_data(asset_selected: list):
    dict_asset_process = {}
    for asset in asset_selected:
        stock = yf.Ticker(asset)
        name = stock.info.get('shortName', asset)
        category = stock.info.get('quoteType', "Unknown")
        country = stock.info.get('country', "Unknown")

        dict_asset_process[asset] = {
                                "name":name,
                                "category":category,
                                "category":category,
                                "country":country,
                                }
        
    return dict_asset_process



