import requests

from .constants import API_URL, API_VERSION, PURCHASE_URL
from .utils import generate_signature


class Api:
    def __init__(self, merchant_account, merchant_key, merchant_domain):
        self.merchant_account = merchant_account
        self.merchant_key = merchant_key
        self.merchant_domain = merchant_domain

    def _query(self, params, url=API_URL):
        response = requests.post(url, json=params)
        return response.json()

    def check_status(self, data):
        """
        Запрос Check Status используется для проверки статуса платежа по orderReference
        :param orderReference:
        :return:
        """
        signature_data = f"{self.merchant_account};{data['orderReference']}"
        params = {
            "transactionType": "CHECK_STATUS",
            "merchantAccount": self.merchant_account,
            "orderReference": data['orderReference'],
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION
        }
        response = self._query(params)
        return response

    def refund(self, data):
        """
        Запрос Refund используется для проведения возврата средств или отмены платежа.
        :param data:
        :return:
        """
        signature_data = f"{self.merchant_account};{data['orderReference']};{data['amount']};{data['currency']}"
        params = {
            "transactionType": "REFUND",
            "merchantAccount": self.merchant_account,
            "orderReference": data['orderReference'],
            "amount": data['amount'],
            "currency": data['currency'],
            "comment": data['comment'],
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION
        }
        response = self._query(params)
        return response

    def settle(self, data):
        """
        Запрос Settle используется для подтверждение списания платежа Auth. Результатом обработки запроса является
        списание заблокированных ранее денежных средств с карты клиента. Операция доступна для транзакций Purchase и
        Charge(host-2-host) с типом merchantTr2483ansactionType = AUTH
        :param data:
        :return:
        """
        signature_data = f"{self.merchant_account};{data['orderReference']};{data['amount']};{data['currency']}"
        params = {
            "transactionType": "SETTLE",
            "merchantAccount": self.merchant_account,
            "orderReference": data['orderReference'],
            "amount": data['amount'],
            "currency": data['currency'],
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION
        }
        response = self._query(params)
        return response

    def purchase(self, data):
        """
        Запрос Purchase используется для проведения платежа клиентом на защищенной странице WayForPay.
        :param data:
        :return:
        """
        all_keys = ['merchantAccount', 'merchantAuthType', 'merchantDomainName', 'merchantTransactionType',
                    'merchantTransactionSecureType', 'merchantSignature', 'apiVersion', 'language', 'returnUrl',
                    'serviceUrl', 'orderReference', 'orderDate', 'orderNo', 'amount', 'currency', 'alternativeAmount',
                    'alternativeCurrency', 'holdTimeout', 'orderTimeout', 'orderLifetime', 'recToken', 'productName',
                    'productPrice', 'productCount', 'clientAccountId', 'socialUri', 'deliveryList', 'clientFirstName',
                    'clientLastName', 'clientAddress', 'clientCity', 'clientState', 'clientZipCode', 'clientCountry',
                    'clientEmail', 'clientPhone', 'deliveryFirstName', 'deliveryLastName', 'deliveryAddress',
                    'deliveryCity', 'deliveryState', 'deliveryZipCode', 'deliveryCountry', 'deliveryEmail',
                    'deliveryPhone', 'aviaDepartureDate', 'aviaLocationNumber', 'aviaLocationCodes', 'aviaFirstName',
                    'aviaLastName', 'aviaReservationCode', 'regularMode', 'regularAmount', 'dateNext', 'dateEnd',
                    'regularCount', 'regularOn', 'paymentSystems', 'defaultPaymentSystem']
        signature_data = f"{self.merchant_account};{self.merchant_domain};{data['orderReference']};{data['orderDate']};{data['amount']};{data['currency']};{';'.join(data['productName'])};{';'.join([str(i) for i in data['productCount']])};{';'.join([str(i) for i in data['productPrice']])}"
        params = {
            "merchantAccount": self.merchant_account,
            "merchantDomainName": self.merchant_domain,
            "merchantTransactionSecureType": "AUTO",
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION,
            "orderReference": data['orderReference'],
            "orderDate": data['orderDate'],
            "amount": data['amount'],
            "currency": data['currency'],
            "productName": data['productName'],
            "productPrice": data['productPrice'],
            "productCount": data['productCount']
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params, url=PURCHASE_URL)
        return response

    def charge(self, data):
        """
        Принять платеж с вводом реквизитов на странице магазина
        Примечание: поля (card+expMonth+expYear+cardCvv+cardHolder) или recToken должно быть обязательным.
        :param data:
        :return:
        """
        if not (('recToken' in data.keys) or (
                'card' in data.keys and 'expMonth' in data.keys and 'expYear' in data.keys and 'cardCvv' in data.keys and 'cardHolder' in data.keys)):
            return None
        all_keys = ['transactionType', 'merchantAccount', 'merchantTransactionType', 'merchantDomainName',
                    'merchantSignature', 'apiVersion', 'language', 'notifyMethod', 'serviceUrl', 'orderReference',
                    'orderDate', 'amount', 'currency', 'alternativeAmount', 'alternativeCurrency', 'orderTimeout',
                    'holdTimeout', 'productName', 'productPrice', 'productCount', 'paymentSystems', 'clientFirstName',
                    'clientLastName', 'clientEmail', 'clientPhone']
        signature_data = f"{self.merchant_account};{self.merchant_domain};{data['orderReference']};{data['orderDate']};{data['amount']};{data['currency']};{';'.join(data['productName'])};{';'.join([str(i) for i in data['productCount']])};{';'.join([str(i) for i in data['productPrice']])}"
        params = {
            "transactionType": "CHARGE",
            "merchantAccount": self.merchant_account,
            "apiVersion": API_VERSION,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "merchantDomainName": self.merchant_domain,
            "productName": data['productName'],
            "productPrice": data['productPrice'],
            "productCount": data['productCount'],
            "orderReference": data['orderReference'],
            "orderDate": data['orderDate'],
            "amount": data['amount'],
            "currency": data['currency']
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response

    def create_invoice(self, data):
        """
        Создание счетов
        :param data:
        :return:
        """
        all_keys = ['transactionType', 'merchantAccount', 'merchantTransactionType', 'merchantDomainName',
                    'merchantSignature', 'apiVersion', 'language', 'notifyMethod', 'serviceUrl', 'orderReference',
                    'orderDate', 'amount', 'currency', 'alternativeAmount', 'alternativeCurrency', 'orderTimeout',
                    'holdTimeout', 'productName', 'productPrice', 'productCount', 'paymentSystems', 'clientFirstName',
                    'clientLastName', 'clientEmail', 'clientPhone']
        signature_data = f"{self.merchant_account};{self.merchant_domain};{data['orderReference']};{data['orderDate']};{data['amount']};{data['currency']};{';'.join(data['productName'])};{';'.join([str(i) for i in data['productCount']])};{';'.join([str(i) for i in data['productPrice']])}"
        params = {
            "transactionType": "CREATE_INVOICE",
            "merchantAccount": self.merchant_account,
            "apiVersion": API_VERSION,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "merchantDomainName": self.merchant_domain,
            "productName": data['productName'],
            "productPrice": data['productPrice'],
            "productCount": data['productCount'],
            "orderReference": data['orderReference'],
            "orderDate": data['orderDate'],
            "amount": data['amount'],
            "currency": data['currency']
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response

    def remove_invoice(self, data):
        """
        Данный метод API позволяет удалять выставленные неоплаченные счета.
        :param data:
        :return:
        """
        signature_data = f"{self.merchant_account};{data['orderReference']}"
        params = {
            "transactionType": "REMOVE_INVOICE",
            "merchantAccount": self.merchant_account,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION,
            "orderReference": data["orderReference"]
        }
        response = self._query(params)
        return response

    def verify(self, data, page=False):
        """
        Запрос Verify используется для вызова страницы wayforpay и проведения  верификации карты клиента.
        Запрос Verify используется для проведения верификации карты клиента.
        :param data:
        :param page: True - Верификация на платежной странице
                    False - Верификация карты/получение токена
        :return:
        """
        signature_data = f"{self.merchant_account};{self.merchant_domain};{data['orderReference']};{data['amount']};{data['currency']}"
        if page:
            all_keys = ['merchantAccount', 'merchantAuthType', 'merchantDomainName', 'merchantSignature', 'apiVersion',
                        'returnUrl', 'serviceUrl', 'orderReference', 'amount', 'currency', 'clientEmail', 'clientPhone',
                        'clientCountry', 'clientAddress', 'clientCity', 'clientState', 'clientZipCode']
            params = {
                "merchantAccount": self.merchant_account,
                "merchantAuthType": "SimpleSignature",
                "merchantDomainName": self.merchant_domain,
                "merchantSignature": generate_signature(self.merchant_key, signature_data),
                "apiVersion": API_VERSION,
                "orderReference": data["orderReference"],
                "amount": data["amount"],
                "currency": data["currency"]
            }
        else:
            all_keys = ['transactionType', 'merchantAccount', 'merchantAuthType', 'merchantDomainName',
                        'merchantSignature', 'apiVersion', 'serviceUrl', 'orderReference', 'amount', 'currency', 'card',
                        'expMonth', 'expYear', 'cardCvv', 'cardHolder', 'clientEmail', 'clientPhone', 'clientCountry',
                        'clientAddress', 'clientCity', 'clientState', 'clientZipCode']
            params = {
                "transactionType": "VERIFY",
                "merchantAccount": self.merchant_account,
                "merchantAuthType": "SimpleSignature",
                "merchantDomainName": self.merchant_domain,
                "merchantSignature": generate_signature(self.merchant_key, signature_data),
                "apiVersion": API_VERSION,
                "orderReference": data["orderReference"],
                "amount": data["amount"],
                "currency": data["currency"],
                "card": data["card"],
                "expMonth": data["expMonth"],
                "expYear": data["expYear"],
                "cardCvv": data["cardCvv"],
                "cardHolder": data["cardHolder"]
            }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response

    def get_client(self, data):
        """
        Получение данных по клиенту
        :param data:  Внимание! Должен быть обязательно передан один из параметров card или recToken.
        :return:
        """
        if 'card' in data.keys():
            signature_data = f"{self.merchant_account};{data['card']}"
            params = {
                "apiVersion": API_VERSION,
                "transactionType": "GET_CLIENT",
                "merchantAccount": self.merchant_account,
                "merchantSignature": generate_signature(self.merchant_key, signature_data),
                "card": data['card']
            }
        else:
            signature_data = f"{self.merchant_account};{data['recToken']}"
            params = {
                "apiVersion": API_VERSION,
                "transactionType": "GET_CLIENT",
                "merchantAccount": self.merchant_account,
                "merchantSignature": generate_signature(self.merchant_key, signature_data),
                "recToken": data['recToken']
            }
        response = self._query(params)
        return response

    def transaction_list(self, data):
        """
        Запрос используется для получения списка транзакций по магазину за определенный период времени.
        :param data:
        :return:
        """
        signature_data = f"{self.merchant_account};{data['dateBegin']};{data['dateEnd']}"
        params = {
            "transactionType": "TRANSACTION_LIST",
            "merchantAccount": self.merchant_account,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION,
            "dateBegin": data['dateBegin'],
            "dateEnd": data['dateEnd']
        }
        response = self._query(params)
        return response

    def currency_rates(self, data):
        """
        Запрос CURRENCY_RATES используется для получения курсов валют в системе wayforpay.
        :param data:
        :return:
        """
        signature_data = f"{self.merchant_account};{data['orderDate']}"
        params = {
            "transactionType": "CURRENCY_RATES",
            "merchantAccount": self.merchant_account,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "apiVersion": API_VERSION,
            "orderDate": data['orderDate']
        }
        if 'currency' in data.keys():
            params['currency'] = data['currency']
        response = self._query(params)
        return response

    def create_qr(self, data):
        """
        Данный метод дает возможность генерации QR кодов для оплаты с помощью мобильного приложения wayforpay.qr
        Результатом запроса будет получение ссылки на изображение QR кода.
        :param data:
        :return:
        """
        all_keys = ['transactionType', 'merchantAccount', 'merchantAuthType', 'merchantDomainName', 'merchantSignature',
                    'apiVersion', 'serviceUrl', 'orderReference', 'orderDate', 'amount', 'currency',
                    'alternativeAmount', 'alternativeCurrency', 'orderTimeout', 'productName', 'productPrice',
                    'productCount', 'clientFirstName', 'clientLastName', 'clientEmail', 'clientPhone',
                    'clientFirstName', 'clientLastName', 'clientEmail', 'clientPhone']
        signature_data = f"{self.merchant_account};{self.merchant_domain};{data['orderReference']};{data['orderDate']};{data['amount']};{data['currency']};{';'.join(data['productName'])};{';'.join([str(i) for i in data['productCount']])};{';'.join([str(i) for i in data['productPrice']])}"
        params = {
            "transactionType": "CREATE_QR",
            "merchantAccount": self.merchant_account,
            "apiVersion": API_VERSION,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "merchantDomainName": self.merchant_domain
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response

    def p2p_transfer(self, data):
        """
        Данное API позволяет производить переводы между картами физических лиц, выпущенных украинскими банками.
        Примечание: поля (card+expMonth+expYear+cardCvv+cardHolder) или recToken должно быть обязательным.
        :param data:
        :return:
        """
        if not (('recToken' in data.keys) or (
                'card' in data.keys and 'expMonth' in data.keys and 'expYear' in data.keys and 'cardCvv' in data.keys and 'cardHolder' in data.keys)):
            return None
        all_keys = ['transactionType', 'merchantAccount', 'merchantDomainName', 'orderReference', 'orderDate', 'amount',
                    'fee', 'currency', 'card', 'expMonth', 'expYear', 'cardCvv', 'cardHolder', 'recToken',
                    'clientFirstName', 'clientLastName', 'clientAddress', 'clientCity', 'clientState', 'clientZipCode',
                    'clientCountry', 'clientEmail', 'clientPhone', 'clientIpAddress', 'cardBeneficiary', 'apiVersion',
                    'deliveryFirstName', 'deliveryLastName', 'deliveryEmail', 'deliveryPhone', 'merchantSignature']
        signature_data = f"{self.merchant_account};{data['orderReference']};{data['amount']};{data['currency']};{data['cardBeneficiary']}"
        params = {
            "transactionType": "P2P_TRANSFER",
            "merchantAccount": self.merchant_account,
            "merchantAuthType": "SimpleSignature",
            "apiVersion": API_VERSION,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "merchantDomainName": self.merchant_domain,
            "orderReference": data['orderReference'],
            "orderDate": data['orderDate'],
            "amount": data['amount'],
            "currency": data['currency']
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response

    def p2p_credit(self, data):
        """
        Данное API позволяет производить пополнения карт физических лиц с банковского счета ТСП.
        Пополнение возможно любых карт, выпущенных Украинскими Банками.
        :param data:
        :return:
        """
        all_keys = ['transactionType', 'merchantAccount', 'orderReference', 'amount', 'currency', 'cardBeneficiary',
                    'rec2Token', 'merchantSignature', 'apiVersion', 'serviceUrl', 'recipientFirstName',
                    'recipientLastName', 'recipientPhone', 'recipientEmail']
        signature_data = f"{self.merchant_account};{data['orderReference']};{data['amount']};{data['currency']};{data['cardBeneficiary']};{data['rec2Token']}"
        params = {
            "transactionType": "P2P_CREDIT",
            "merchantAccount": self.merchant_account,
            "merchantAuthType": "SimpleSignature",
            "apiVersion": API_VERSION,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "orderReference": data['orderReference'],
            "amount": data['amount'],
            "currency": data['currency']
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response

    def p2p_account(self, data):
        """
        Данное API позволяет производить пополнения расчетных счетов Юр. лиц и ФОП с банковского счета ТСП.
        Пополнение возможно расчетных счетов, открытых в любом Украинском Банке.
        :param data:
        :return:
        """
        all_keys = ['transactionType', 'merchantAccount', 'orderReference', 'amount', 'currency', 'iban', 'okpo',
                    'accountName', 'merchantSignature', 'apiVersion', 'description', 'serviceUrl', 'recipientLastName',
                    'recipientPhone', 'recipientEmail']
        signature_data = f"{self.merchant_account};{data['orderReference']};{data['amount']};{data['currency']};{data['iban']};{data['okpo']};{data['accountName']}"
        params = {
            "transactionType": "P2P_ACCOUNT",
            "merchantAccount": self.merchant_account,
            "merchantAuthType": "SimpleSignature",
            "apiVersion": API_VERSION,
            "merchantSignature": generate_signature(self.merchant_key, signature_data),
            "orderReference": data['orderReference'],
            "amount": data['amount'],
            "currency": data['currency']
        }
        for key in all_keys:
            if key in data.keys() and key not in params.keys():
                params[key] = data[key]
        response = self._query(params)
        return response
