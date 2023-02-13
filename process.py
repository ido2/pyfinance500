

def is_module_loaded(module):
    import sys
    return module in sys.modules

def install(package):
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


class dtr:
    def get_ticker(self, tickers, start, end):
        #process.install("git+https://github.com/raphi6/pandas-datareader@22f1b951fdd49f30a5832cbca0119f5a2e6da15f")
        
        import pandas_datareader as dtr
        data = dtr.get_data_yahoo(tickers, start=start, end=end)['Adj Close']
        return data

class yahoo:
    def get_ticker(self, tickers, start, end):
        if not is_module_loaded("yfinance"):
            install("yfinance")
        
        import yfinance as yf
        data = yf.download(tickers, start=start, end=end, ignore_tz=True, prepost=False, period="1d")['Adj Close']
        if len(tickers) == 1:
            data = data.to_frame(name=tickers[0])

        return data


class maya:
    def get_ticker(self, tickers, start, end):
        from pymaya.maya import Maya

        maya = Maya()
        historical_prices = maya.get_price_history(security_id=tickers, from_data=start, to_date=end)
        import pandas as pd
        someDf = pd.DataFrame(historical_prices)
        return self._fix(someDf)

    def _fix(self, someDf):
        s1 = someDf[["TradeDate", "CloseRate"]]
        s1 = s1.rename(columns={'TradeDate': 'Date', 'CloseRate': '1159250'})
        s1 = s1.iloc[::-1]
        import pandas as pd
        s1["Date"] = pd.to_datetime(s1['Date'].astype(str), format='%d/%m/%Y')
        s1 = s1.set_index("Date")
        return s1
