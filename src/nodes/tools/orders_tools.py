

from typing import Union

from langchain_community.tools import tool
import requests
from dotenv import load_dotenv
import os

STORE_API_KEY = os.environ["STORE_API_KEY"] 

@tool
def get_orders() -> Union[list, str]:

    """
    This tool is intended to return the user the
    current list of orders made by the users.
    """
    try:
        url = f"{STORE_API_KEY}api/orders/"
        resp = requests.get(url)
        resp.raise_for_status()

        return resp.json()
    except Exception as ex:
            return f"There was an error getting the weather from: {ex}"


tools = [
    get_orders
]