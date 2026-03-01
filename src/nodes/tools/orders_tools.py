

from langchain_community.tools import tool
import requests
from dotenv import load_dotenv
import os

STORE_API_KEY = os.environ["STORE_API_KEY"] 

@tool
def get_orders() -> list[any]:

    """"
        This tool is intended to return the user the
        current list of orders.

    """
    try:
        url = f"{STORE_API_KEY}api/get_brands/"
        resp = requests.get(url)
        data = resp.json()
        return data
    except Exception as ex:
            return f"There was an error getting the weather from: {ex}"


tools = [
    get_orders
]