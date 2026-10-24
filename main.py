import requests, shelve

api_key = ""
allow_debt = True

def write_db(key, value):
    with shelve.open("tradetool-db") as db:
        db[key] = value

def read_db(key):
    with shelve.open("tradetool-db") as db:
        if db[key]:
            return db[key]
        else:
            return None


with open('secrets.txt', 'r') as f:
    api_key = f.read()

class TradeTool():
    def __init__(self, starting_money=100):
        try:
            self.money = read_db("money") if read_db("money") != None else starting_money
            self.assets = read_db("assets") if read_db("assets") != None else {}
        except KeyError:
            self.money = starting_money
            self.assets = {}
            self.save_to_db()

    def load_from_db(self):
        self.money = read_db("money")
        self.assets = read_db("assets")
    
    def save_to_db(self):
        write_db("money", self.money)
        write_db("assets", self.assets)

    # Read API

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

    # Actions

    def trade_stock(self, symbol, amount=0):
        price = requests.get(f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&apikey={api_key}").json()
        price = price[0]['price']
        if price > self.money and not allow_debt:
            return "Too expensive."
        else:
            self.money -= price * amount
            self.assets[symbol] = self.assets.get(symbol, 0) + amount

    def sell_stock(self, symbol, amount=0):
        if amount > self.assets[symbol]:
            return "Not enough owned to sell."
        else:
            price = requests.get(f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&apikey={api_key}").json()
            price = price[0]['price']
            self.money += price * amount
            self.assets[symbol] = self.assets.get(symbol, 0) - amount

# tradetool = TradeTool(starting_money=200)
# print(tradetool.sell_stock("AAPL", 0.08))
# tradetool.save_to_db()