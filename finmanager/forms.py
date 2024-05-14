from django import forms
from django.core.validators import RegexValidator

class CryptoAddressForm(forms.Form):
    btc_address = forms.CharField(
        label='BTC Address',
        validators=[
            # RegexValidator(
            #     regex=r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
            #     message='Invalid BTC address'
            # )
        ]
    )
    eth_address = forms.CharField(
        label='ETH Address',
        validators=[
            # RegexValidator(
            #     regex=r'^0x[a-fA-F0-9]{40}$',
            #     message='Invalid ETH address'
            # )
        ]
    )
    b3_file = forms.FileField(
        label='B3 File',
        allow_empty_file=False,
        required=True
    )