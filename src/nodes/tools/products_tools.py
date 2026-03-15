from typing import Union

from langchain_community.tools import tool
import requests
import os

STORE_API_KEY = os.environ["STORE_API_KEY"]


@tool
def get_products() -> Union[list, str]:
    """
    Returns the full list of products available in the store.
    """
    try:
        url = f"{STORE_API_KEY}api/products/"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as ex:
        return f"There was an error getting the products: {ex}"


@tool
def get_product(product_id: int) -> Union[dict, str]:
    """
    Retrieves a single product by its ID.
    Use this when the user asks about a specific product.
    """
    try:
        url = f"{STORE_API_KEY}api/products/{product_id}/"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as ex:
        return f"There was an error getting the product: {ex}"


tools = [
    get_products,
    get_product
]
