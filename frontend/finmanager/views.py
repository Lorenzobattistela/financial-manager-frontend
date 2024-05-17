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


def dashboard(request):
    btc = BitcoinAddress.objects.all()[0]
    print(btc)
    eth = EthereumAddress.objects.all()[0]
    print(eth)
    stocks = Stock.objects.all()
    total_value_stocks = 0
    for stock in stocks:
        total_value_stocks += stock.updated_value

    fii = Fii.objects.all()
    total_value_fii = 0
    for f in fii:
        total_value_fii += f.updated_value

    print(fii)
    total_value_treasury = 0
    treasury = TreasuryDirect.objects.all()
    print(treasury)
    for title in treasury:
        total_value_treasury += title.updated_value

    print(treasury)

    b3_parsed = {
        "treasury_directs": treasury,
        "total_value_treasury_directs": total_value_treasury,
        "stocks": stocks,
        "total_value_stocks": total_value_stocks,
        "fiis": fii,
        "total_value_fiis": total_value_fii
    }

    balances = [
        {"product": "Tesouro Direto", "balance": b3_parsed["total_value_treasury_directs"]},
        {"product": "Ações", "balance": b3_parsed["total_value_stocks"]},
        {"product": "Fundos Imobiliários", "balance": b3_parsed["total_value_fiis"]},
        {"product": "Bitcoin", "balance": btc.brl_balance},
        {"product": "Ethereum", "balance": eth.brl_balance}
    ]

    balances = [{k: str(v) for k, v in balance.items()} for balance in balances]
    balances = json.dumps(balances)

    ctx = {
        "eth_balance": eth,
        "btc_balance": btc,
        "b3_parsed": b3_parsed,
        "balances": balances
    }

    return render(request, 'dashboard.html', ctx)


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
    print(eth_val_json)
    price = eth_val_json.get("price")

    if response.status_code == 200:
        data = json.loads(response.json())
        print(data)
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

        stocks = data.get("stocks")
        fiis = data.get("fiis")
        treasury_direct = data.get("treasury_directs")

        for stock in stocks:
            negotiation_code = stock.get("negotiation_code")
            db_stock, created = Stock.objects.get_or_create(
                negotiation_code=negotiation_code)

            db_stock.quantity = stock.get("quantity")
            db_stock.price = stock.get("last_price")
            db_stock.updated_value = stock.get("updated_value")
            db_stock.save()

        for fii in fiis:
            negotiation_code = fii.get("negotiation_code")
            db_fii, created = Fii.objects.get_or_create(
                negotiation_code=negotiation_code)

            db_fii.quantity = fii.get("quantity")
            db_fii.price = fii.get("last_price")
            db_fii.updated_value = fii.get("updated_value")
            db_fii.save()

        for title in treasury_direct:
            product = title.get("product")
            db_title, created = TreasuryDirect.objects.get_or_create(
                product=product)

            db_title.indexer = title.get("indexer")
            db_title.quantity = title.get("quantity")
            db_title.deadline = title.get("deadline")
            db_title.applied_value = title.get("applied_value")
            db_title.brute_value = title.get("brute_value")
            db_title.liquid_value = title.get("liquid_value")
            db_title.updated_value = title.get("updated_value")
            db_title.save()

        return data
    return
