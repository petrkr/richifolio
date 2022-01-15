

class Trasaction():
    def __init__(self):
        pass


class GenericBankAPI():
    def balance(self):
        raise NotImplementedError
    
    def transactions(self):
        raise NotImplementedError
