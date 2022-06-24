import requests
from sympy import re

def getProxy():
    # 从127.0.0.1:5000获取代理ip
    response = requests.get('http://127.0.0.1:8080/get')
    response = response.json()
    return response
