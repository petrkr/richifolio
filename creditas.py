# Apache 2 License
# Petr Kracik (c) 2022

from genericapi import GenericBankAPI
import json
import requests


class Info():
    def __init__(self, data):
        self._accountId = data["accountId"]
        self._bban = data["bban"]
        self._bankCode = data["bankCode"]
        self._iban = data["iban"]
        self._bic = data["bic"]
        self._currency = data["currency"]
        self._country = data["country"]
        self._status = data["status"]
        self._name = data["name"]
        self._productCode = data["productCode"]
        self._productI18N = data["productI18N"]
        self._currentBalance = float(data["currentBalance"])
        self._availableBalance = float(data["availableBalance"])


    def __str__(self):
        return self._name


    @property
    def account_id(self):
        return self._accountId


    @property
    def bban(self):
        return self._bban


    @property
    def current_balance(self):
        return self._currentBalance


    @property
    def available_balance(self):
        return self._availableBalance


    @property
    def name(self):
        return self._name



class BankaCreditasAPI(GenericBankAPI):
    BASEURL = "https://api.creditas.cz/oam/v1"

    def __init__(self, account_id, token):
        super().__init__()

        self._account_id = account_id
        self._token = token
        self._rawdata = None
        self._info = None
        self._transactions = []

        self._load_account()


    def _load_account(self):
        headers ={
            "Authorization": "Bearer {}".format(self._token),
            "Content-Type" : "application/json"
        }

        data = '{{"accountId":"{}"}}'.format(self._account_id)
        res = requests.post("{}/account/current/get".format(self.BASEURL), data=data, headers=headers)


        if res.status_code != 200:
            raise Exception("Unknown error: {}: {}".format(res.status_code, res.text))

        self._rawdata = res.json()
        self._info = Info(self._rawdata['currentAccount'])


    def __str__(self):
        return "{}: {}".format(self.name, self.balance)


    @property
    def name(self):
        return self._info.name


    @property
    def balance(self):
        if not self._info:
            return None

        return self._info.available_balance


    @property
    def account_info(self):
        return self._info

