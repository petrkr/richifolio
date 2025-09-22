# Apache 2 License
# Petr Kracik (c) 2022

from genericapi import GenericBankAPI, Trasaction
import json
import requests
from datetime import datetime

#https://www.fio.cz/ib_api/rest/periods/{token}/{datum od}/{datum do}/transactions.{format}
# date format rrrr-mm-dd

class Info():
    def __init__(self, data):
        self._accountId = data['accountId']
        self._bankId = data['bankId']
        self._currency = data['currency']
        self._iban = data['iban']
        self._bic = data['bic']
        self._openingBalance = data['openingBalance']
        self._closingBalance = data['closingBalance']
        self._dateStart = datetime.strptime(data['dateStart'], "%Y-%m-%d%z").date()
        self._dateEnd = datetime.strptime(data['dateEnd'], "%Y-%m-%d%z").date()
        self._yearList = data['yearList']
        self._idList = data['idList']
        self._idFrom = data['idFrom']
        self._idTo = data['idTo']
        self._idLastDownload = data['idLastDownload']

    def __str__(self):
        return "{}/{}".format(self.account_id,self.bank_id)

    @property
    def account_id(self):
        return self._accountId


    @property
    def bank_id(self):
        return self._bankId


    @property
    def closing_balance(self):
        return self._closingBalance


    @property
    def date_end(self):
        return self._dateEnd


class FioBankAPI(GenericBankAPI):
    BASEURL = "https://fioapi.fio.cz/v1/rest"

    def __init__(self, fio_token, name=None):
        super().__init__()

        self._name = name
        self._token = fio_token
        self._rawdata = None
        self._info = None
        self._transactions = []

        self._load()


    def _load(self):
        now = datetime.now().date()
        res = requests.get("{}/periods/{}/{}/{}/transactions.json".format(self.BASEURL, self._token, now, now))

        if res.status_code == 409:
            raise Exception("Too much requests")

        if res.status_code != 200:
            raise Exception("Unknown error: {}: {}".format(res.status_code, res.text))

        self._rawdata = res.json()
        self._info = Info(self._rawdata['accountStatement']['info'])
        if self._name is None:
            self._name = "{}/{}".format(self._info.account_id, self._info.bank_id)


    def __str__(self):
        return "{}: {}".format(self.name, self.balance)


    @property
    def name(self):
        return self._name


    @property
    def balance(self):
        if not self._info:
            return None

        return self._info.closing_balance


    @property
    def account_info(self):
        return self._info

