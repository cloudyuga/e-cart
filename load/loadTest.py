import requests
import re
import sys

def register(ip, port):
    url = 'http://{}:{}/register'.format(ip,port)
    payload = {
        'username': 'cloudyuga',
        'password': 'cloudyuga',
        'confirm': 'cloudyuga',
        'email': 'cloudyuga'
    }
    response = requests.post(url, data=payload)
    return response

def login(ip, port):
    url = 'http://{}:{}/login'.format(ip,port)
    payload = {
        'username': 'cloudyuga',
        'password': 'cloudyuga'
    }
    response = requests.post(url, data=payload)
    return response

def addToCart(ip, port, cookie):
    url = 'http://{}:{}/add-to-cart/2'.format(ip,port)
    response = requests.get(url, cookies=cookie)
    return response

def displayCart(ip, port, cookie):
    url = 'http://{}:{}/cart'.format(ip,port)
    response = requests.get(url, cookies=cookie)
    return response

def placeOrder(ip, port, cookie, cartId):
    url = 'http://{}:{}/place-order/{}'.format(ip,port,cartId)
    response = requests.get(url, cookies=cookie)
    return response

def makePayment(ip, port, cookie, orderId):
    url = 'http://{}:{}/payment/{}'.format(ip,port,orderId)
    response = requests.get(url, cookies=cookie)
    return response

def logout(ip, port):
    url = 'http://{}:{}/logout'.format(ip,port)
    response = requests.get(url)
    return response


ip = sys.argv[1]
port = sys.argv[2]
response = register(ip, port)
response = login(ip, port)
cookie = response.cookies
for index in range(1, 100):
    response = addToCart(ip, port,cookie)
response = displayCart(ip, port,cookie)
# Fetch Cart ID
cartIdPattern = re.search( r'place-order/[0-9]{1,3}', response.text)
cartId = int((cartIdPattern.group().split("/")[1]))
response = placeOrder(ip, port,cookie, cartId)
# Fetch Order ID
orderIdPattern = re.search( r'payment/[0-9]{1,3}', response.text)
orderId = int((orderIdPattern.group().split("/")[1]))
response = makePayment(ip, port,cookie, orderId)
response = logout(ip, port)
