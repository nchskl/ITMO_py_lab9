class UserCurrency:
    def __init__(self, ucid: int, user_id: int, currency_id: int):
        self.ucid = ucid
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def ucid(self) -> str:
        return self.__ucid

    @ucid.setter
    def ucid(self, value: int):
        if not isinstance(value, (str,int)):
            raise TypeError("id must be an integer")
        self.__ucid = str(value)

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("user_id must be an integer")
        self.__user_id = value

    @property
    def currency_id(self) -> str:
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("currency_id must be an string")
        self.__currency_id = value
