# 2022 (c) Petr Kracik
# Apache 2 License

import json
from fio import FioBankAPI
from creditas import BankaCreditasAPI


def main():
    config = json.load(open("config.json"))

    creditas_accounts = []
    fio_accounts = []

    for a in config['creditas']:
        creditas_accounts.append(BankaCreditasAPI(a['account_id'], a['token']))

    for a in creditas_accounts:
        print(a)

    for f in config['fio']:
        fio_accounts.append(FioBankAPI(f['token'], f['name'] if 'name' in f else None))

    for f in fio_accounts:
        print(f)


if __name__ == "__main__":
    main()