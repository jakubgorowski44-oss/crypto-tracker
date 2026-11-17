import requests as rq
from dotenv import load_dotenv
from functools import wraps
import os
import time

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)

            except rq.RequestException:
                print(f"Attempt {attempt + 1} failed")

            if attempt<2:
                time.sleep(2)

        raise Exception("Unable to get data.")

    return wrapper

class ApiClient:

    load_dotenv()
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = os.getenv("API_KEY")

    if api_key is None:
        raise ValueError("API_KEY not found in .env")

    headers ={
    "X-CMC_PRO_API_KEY": api_key
    }

    params ={
    "start" : 1,
    "limit" : 100,
    "convert": "PLN"
    }

    def __init__(self,url=url,headers=headers,params=params):
        self.url = url
        self.headers = headers
        self.params = params
        
    @retry
    def get_data(self):
        response = rq.get(url=self.url,headers=self.headers,params=self.params,timeout=5)
            
        response.raise_for_status()
        return(response.json())

    