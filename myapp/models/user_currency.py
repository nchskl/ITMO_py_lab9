from myapp.models.user import User

#недописанная модель

class UserCurrency(User):
    def __init__(self, uid: str = '504485', username: str = 'nchskl', currency: float = 0.0):
        super().__init__(uid, username)
        self.currency = currency

    @property
    def currency(self) -> float:
        return self.__currency

    @currency.setter
    def currency(self, currency: float):
        if not isinstance(currency, (int, float)):
            raise TypeError("Currency must be a number.")
        if currency < 0:
            raise ValueError("Currency cannot be negative.")
        self.__currency = float(currency)

