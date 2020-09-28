from .api import Api

__all__ = ["WayForPay"]


class WayForPay:
    def __init__(self, merchant_account, merchant_key, merchant_domain):
        self.merchant_account = merchant_account
        self.merchant_key = merchant_key
        self.merchant_domain = merchant_domain
        self.api = Api(self.merchant_account, self.merchant_key, self.merchant_domain)
