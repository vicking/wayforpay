import requests

from .constants import API_URL
from .utils import generate_signature


class Api:
    def __init__(self, merchant_account, merchant_key, merchant_domain):
        self.merchant_account = merchant_account
        self.merchant_key = merchant_key
        self.merchant_domain = merchant_domain

    def _query(self, params, url=API_URL):
        response = requests.post(url, json=params)
        return response.json()

    def verify(self, data):
        """
        Cart verification and receiving token(Verify)
        Запрос Verify используется для проведения верификации карты клиента.
        :param data:
        :return:
        """
        signature_data = f"{self.merchant_account};{self.merchant_domain};{data['orderReference']};{data['amount']};{data['currency']}"
        params = {
            "transactionType": "VERIFY",
            "merchantAccount": self.merchant_account,
            "merchantAuthType": "SimpleSignature",
            "merchantDomainName": self.merchant_domain,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": 1,
            "orderReference": data["orderReference"],
            "amount": data["amount"],
            "currency": data["currency"],
            "card": data["card"],
            "expMonth": data["expMonth"],
            "expYear": data["expYear"],
            "cardCvv": data["cardCvv"],
            "cardHolder": data["cardHolder"]
        }
        if 'serviceUrl' in data.keys():
            params["serviceUrl"] = data['serviceUrl']
        if 'clientCountry' in data.keys():
            params["clientCountry"] = data["clientCountry"]
        if 'clientEmail' in data.keys():
            params["clientEmail"] = data["clientEmail"]
        if 'clientPhone' in data.keys():
            params["clientPhone"] = data["clientPhone"]
        if 'clientAddress' in data.keys():
            params["clientAddress"] = data["clientAddress"]
        if 'clientCity' in data.keys():
            params["clientCity"] = data["clientCity"]
        if 'clientState' in data.keys():
            params["clientState"] = data["clientState"]
        if 'clientZipCode' in data.keys():
            params["clientZipCode"] = data["clientZipCode"]
        response = self._query(params)
        return response
