from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .forms import DashboardForm
from .models import Stock, Fii, TreasuryDirect, BitcoinAddress, EthereumAddress
from dotenv import load_dotenv
from typing import List
import requests
import json
import os

load_dotenv()


def index(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST, request.FILES)
        if form.is_valid():
            btc_address = form.cleaned_data['btc_address']
            eth_address = form.cleaned_data['eth_address']
            b3_file = form.cleaned_data['b3_file']

            btc_balance = btc(btc_address)
            eth_balance = eth(eth_address)
            b3_parsed = b3(b3_file)

            ctx = {
                'btc_balance': btc_balance,
                'eth_balance': eth_balance,
                'b3_parsed': b3_parsed
            }
            return render(request, 'dashboard.html', ctx)
        else:
            return render(request, 'form.html', {'form': form, 'errors': form.errors})

    form = DashboardForm()
    return render(request, 'form.html', {'form': form})


HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'x_api_key': os.getenv("API_KEY")
}

BASE_URL = "http://localhost:8000"


def btc(address: str) -> BitcoinAddress:
    response = requests.get(
        f"{BASE_URL}/bitcoin/balance/{address}", headers=HEADERS)

    price = 0
    btc_val = requests.get(f"{BASE_URL}/bitcoin/brl-price", headers=HEADERS)
    btc_val_json = json.loads(btc_val.json())
    price = btc_val_json.get("price")

    if response.status_code == 200:
        data = json.loads(response.json())
        balance = data.get("balance")
        btc_price = price * balance

        btc_address, created = BitcoinAddress.objects.get_or_create(
            address=address)
        btc_address.balance = balance
        btc_address.brl_balance = btc_price
        btc_address.save()

        return btc_address
    return


def eth(address: str) -> EthereumAddress:
    response = requests.get(
        f"{BASE_URL}/ethereum/balance/{address}", headers=HEADERS)

    eth_val = requests.get(f"{BASE_URL}/ethereum/brl-price", headers=HEADERS)
    eth_val_json = json.loads(eth_val.json())
    price = eth_val_json.get("price")

    if response.status_code == 200:
        data = json.loads(response.json())
        balance = data.get("balance")
        eth_price = price * balance

        eth_address, created = EthereumAddress.objects.get_or_create(
            address=address
        )
        eth_address.balance = balance
        eth_address.brl_balance = eth_price
        eth_address.save()
        return eth_address
    return


def b3(b3_file):
    files = {'file': b3_file}
    response = requests.post(f"{BASE_URL}/b3/parse",
                             headers=HEADERS, files=files)
    if response.status_code == 200:
        data = json.loads(response.json())
        return data
    return
