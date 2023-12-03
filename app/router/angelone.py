from fastapi import Request, APIRouter, Query
from SmartApi import SmartConnect #, SmartWebSocket

import requests
import json
import pyotp

# Database
# from app.databaseutils import get_db

router = APIRouter(prefix='/angelone', tags=['AngelOne'])

token = "RYJNWG52S5XHH6Q7PUNVIOFQXM"
totp = pyotp.TOTP(token).now()
api_key = "6pLf0hLk"
username = "H178455"
password = "4333"

# Json File 
class TokenDataProcessor:
    def __init__(self):
        self.data = []
        self.filename = "scrip_master.json"

    def download_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()

            with open(self.filename, 'w') as json_file:
                json_file.write(response.text)

            print(f"Data downloaded and saved to {self.filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def load_data(self):
        try:
            with open(self.filename, "r") as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            print("File not found.")

    def get_filtered_data(self, symbol=None, token=None):
        filtered_data = []
        symbol = symbol.lower() if symbol else None
        token = token.lower() if token else None
        # name = name.lower() if name else None

        for item in self.data:
            item_symbol = item["symbol"].lower()
            item_token = item["token"].lower()
            # item_name = item["name"].lower()

            if (not symbol or symbol in item_symbol) and (not token or token == item_token):
                filtered_data.append(item)

        return filtered_data
    
# Assuming you already have the necessary imports and configurations for SmartConnect
class SmartConnection:
    def __init__(self, api_key, username, password, totp):
        self.api_key = api_key
        self.username = username
        self.password = password
        self.totp = totp
        self.session = None
        self.access_token = None

    async def generate_session(self):
        smart_api = SmartConnect(api_key=self.api_key)
        session_data = smart_api.generateSession(self.username, self.password, self.totp)
        self.access_token = session_data['data']['jwtToken']
        self.session = smart_api

    async def get_profile(self):
        if not self.session:
            await self.generate_session()
        profile_data = self.session.getProfile(self.access_token)
        data = profile_data['data']['exchanges']
        return data

    async def get_orderBook(self):
        if not self.session:
            await self.generate_session()
        orderBook_data = self.session.orderBook(self)
        data = orderBook_data
        return data
    
    async def get_candle_data(self, exchange, token, interval, fromdate, todate):
        if not self.session:
            await self.generate_session()

        historicDataParams = {
            "exchange": exchange,
            "symboltoken": token,
            "interval": interval,
            "fromdate": fromdate, # YYYY-MM-DD HH:MM / 2022-10-18 11:40
            "todate": todate # YYYY-MM-DD HH:MM / 2022-10-18 11:40
        }

        result = self.session.getCandleData(historicDataParams)

        return result


smart_connection = SmartConnection(api_key, username, password, totp)

data_processor = TokenDataProcessor()


# @router.on_event("startup")
# async def startup_event():
#     url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#     data_processor.download_data(url) # commant on tesing 

@router.get("/get_token_to_name")
async def get_token_to_name(request: Request, token: str = Query(None)):
    filtered_data = data_processor.get_filtered_data(token=token)
    if not filtered_data:
        return {"message": "No matching data found."}

    return {"data": filtered_data, "message": "success"}

@router.get("/get_data_json")
async def get_data_json(request: Request, token: str = Query(None), symbol: str = Query(None), limit: int = Query(10, gt=0), skip: int = Query(0, ge=0)):
    data_processor.load_data()
    filtered_data = data_processor.get_filtered_data(symbol=symbol, token=token)
    if not filtered_data:
        return {"message": "No matching data found."}

    start_idx = skip
    end_idx = skip + limit
    result = filtered_data[start_idx:end_idx]
    count = len(result)

    data = {
        "result": result, 
        "count": count
    }

    return data

@router.get("/display_table_view_json")
async def display_table_view_json(request: Request, exchange: str = Query(None), token: str = Query(None), interval: str = Query(None), fromdate: str = Query(None), todate: str = Query(None)):
    if not exchange:
        exchange = "NFO"
    else:
        exchange = exchange
    
    if not token:
        token = "41011"
    else:
        token = token

    if not interval:
        interval = "FIVE_MINUTE"
    else:
        interval = interval

    if fromdate and todate:
        fromdate = f"{fromdate}"
        todate = f"{todate}"
    else:
        fromdate = "2023-12-01 09:30" # YYYY-MM-DD HH:MM / 2022-10-18 11:40
        todate = "2023-12-01 12:00"   # YYYY-MM-DD HH:MM / 2022-10-18 11:40

    token_name = await get_token_to_name(request, token)

    result = await smart_connection.get_candle_data(exchange, token, interval, fromdate, todate)
    # [timestamp, open, high, low, close, volume]


    if 'data' in token_name:
        token_symbols = [item['symbol'] for item in token_name['data']]
    else:
        token_symbols = ['']

    token = {
        'token_name': ', '.join(token_symbols),
        "data": result['data']
    }

    return token

