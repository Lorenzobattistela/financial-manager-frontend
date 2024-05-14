from django import forms
from django.core.validators import RegexValidator

class DashboardForm(forms.Form):
    btc_address = forms.CharField(
        label='BTC Address',
        # validators=[
        #     RegexValidator(
        #         regex=r"^(bc1|[13])[a-km-zA-HJ-NP-Z1-9]{25,34}$",
        #         message='Invalid BTC address'
        #     )
        # ]
    )
    eth_address = forms.CharField(
        label='ETH Address',
        validators=[
            RegexValidator(
                regex=r'^(0x)?[0-9a-fA-F]{40}$',
                message='Invalid ETH address'
            )
        ]
    )
    b3_file = forms.FileField(
        label='B3 File',
        allow_empty_file=False,
        required=True,
        # validators=[
        #     RegexValidator(
        #         regex=r'^.*\.xlsx$',
        #         message='Invalid B3 excel file'
        #     )
        # ]
    )