from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    headers = {
        'User-Agent': 'Your User Agent',
        'Custom-Header': 'Custom Value',
        'x_api_key': 'valid_api_key'
    }

    ctx = {
        'title': 'Bitcoin Balance',
        'balance': '0.00000000'
    }

    try:
        response = requests.get("http://localhost:8000/bitcoin/balance/bc1qup32v2aazd6k7xx5d5dwxtuu8axeam68rwnazj", headers=headers)
        if response.status_code == 200:
            return render(request, 'index.html', ctx)
        else:
            return HttpResponse(f"Request to localhost:8000 failed with status code {response.status_code}")
    except requests.RequestException as e:
        return HttpResponse(f"Error making request to localhost:8000: {e}")

def btc(request):
    # get is a form, post calls the api and renders the result.
    return

def eth(request):
    return

# deal with file input
def b3(request):
    return

# entire dashboard based on user's holdings
def dashboard(request):
    return

def create_account(request):
    return

