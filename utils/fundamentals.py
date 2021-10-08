import yfinance
import pandas as pd


class FundamentalData:
    def __init__(self, ticker):
        self.data = yfinance.Ticker(ticker)


    def get_fundamentals(self):
        context = {'ticker': self.data.ticker, 'isin': self.data.isin, 'info': self.data.info,
                   'balance_sheet': self.data.balance_sheet, 'financials': self.data.financials,
                   'cashflow': self.data.cashflow, 'earnings': self.data.earnings,
                   'calendar': self.data.calendar,
                   'major_holders': self.data.major_holders,
                   'mutualfund_holders': self.data.mutualfund_holders,
                   'institutional_holders': self.data.institutional_holders,
                   'actions': self.data.actions,
                   'options': self.data.options,
                   'recommendations': self.data.recommendations,
                   'esg': self.data.sustainability}
        return context


    def get_price_history(self):
        context = {'price_history': self.data.history()}
        return context


