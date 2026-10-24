import requests, shelve

api_key = ""

def write_db(key, value):
    with shelve.open("tradetool") as db:
        db[key] = value

def read_db(key):
    with shelve.open("tradetool") as db:
        if db[key]:
            return db[key]
        else:
            return None


with open('secrets.txt', 'r') as f:
    api_key = f.read()

class TradeTool():
    def __init__(self, starting_money=100):
        self.money = starting_money
        self.holdings = {"BTC": 0.0, ".INX": 0.0}
    
    def save_to_db(self):
        write_db("money", self.money)
        write_db("holdings", self.holdings)


    def stock_symbol_search(self, symbol):
        r = requests.get(f"https://financialmodelingprep.com/stable/search-symbol?query={symbol}&apikey={api_key}")
        return r.text
    
    def company_name_search(self, company_name):
        r = requests.get(f"https://financialmodelingprep.com/stable/search-name?query={company_name}&apikey={api_key}")
        return r.text

    def stock_quote(self, symbol):
        r = requests.get(f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&apikey={api_key}")
        return r.text

    def crypto_quote(self, symbol):
        r = requests.get(f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&apikey={api_key}")
        return r.text

    
    def trade_stock(self, symbol, sell=False, amount=0):
        price = requests.get(f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&apikey={api_key}").json()
        price = price[0]['price']




tradetool = TradeTool(starting_money=200)
print(tradetool.trade_stock("AAPL"))