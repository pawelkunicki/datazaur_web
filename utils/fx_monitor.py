import yaml
from forex_python.converter import CurrencyRates
import pandas as pd
import os
from django.conf import settings


class ForexMonitor:
    def __init__(self):
        self.rates = CurrencyRates()
        self.base_currency = None
        self.sorted_currencies = []
        self.matrix = None

        self.load_config()
        self.get_forex_matrix()

    @staticmethod
    def round_data(df, n):
        for col in df.columns:
            df[col] = df[col].round(n)
        return df

    def load_config(self):

        self.base_currency = settings.DEFAULT_CURRENCY
        self.sorted_currencies = settings.SORTED_CURRENCIES





    def get_forex_matrix(self):
        try:
            rates = pd.concat([pd.Series({self.base_currency: 1}), pd.Series(self.rates.get_rates(self.base_currency))])
            if not self.sorted_currencies:
                self.sorted_currencies = list(rates.index)
            self.sorted_currencies.remove(self.base_currency)
            self.sorted_currencies.insert(0, self.base_currency)
            self.matrix = pd.DataFrame(index=self.sorted_currencies, columns=self.sorted_currencies)
            print(1)
            print(self.matrix)
            self.matrix.loc[self.base_currency, :] = rates
            self.matrix.loc[:, self.base_currency] = rates
            print(2)
            print(self.matrix)
            self.matrix = self.round_data(self.calculate_cross_rates(self.matrix, self.base_currency), 3)
            print(3)
            print(self.matrix)
            return self.matrix
        except:
            return None


    @staticmethod
    def calculate_cross_rates(matrix, base_currency):
        return matrix.apply(lambda x: matrix.loc[base_currency] / x.loc[base_currency]).transpose()





    def enable_dateedit(self):

        self.dateedit.setEnabled(True)

    def hist_prices_off(self):

        self.get_currency_matrix(self.rates)

    def convert(self):
        #rate = self.currencies.get_rate(self.comboBox.currentText(), self.comboBox1.currentText())
        if float(self.lineEdit1.text()):
            rate = self.matrix.loc[self.comboBox.currentText(), self.comboBox1.currentText()]
            amount = float(self.lineEdit1.text())
            cash = str(amount * rate)
            self.label3.setText(cash)
        else:
            pass

    def get_rates2(self):
        return pd.Series(self.currencies.get_rates(self.base_currency))

    def get_historical_rates(self):
        date = self.dateedit.dateTime().toPyDateTime()
        return pd.Series(self.currencies.get_rates(self.base_currency, date))


    def search(self):
        text = self.lineEdit.text()
        filtered_df = self.matrix.loc[filter(lambda x: text.upper() in x, self.matrix.index)]
        model = PandasModel(filtered_df)
        self.table.setModel(model)


    def get_currency_matrix(self, series):
        matrix = pd.DataFrame(index=self.sorted_currencies, columns=self.sorted_currencies)
        s1 = series.copy()
        matrix.loc[self.base_currency] = s1
        matrix.loc[:, self.base_currency] = s1
        self.matrix = matrix.apply(lambda x: matrix.loc[self.base_currency] / x.loc[self.base_currency])
        self.matrix = self.matrix.transpose(copy=True)
        self.matrix = self.round_data(self.matrix.copy(), 4)

        model = PandasModel(self.matrix)
        self.table.setModel(model)






