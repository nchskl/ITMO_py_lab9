class Currency:
    def __init__(self, cid: str, num_code: str, char_code: str, name: str, value: float, nominal: str):
        self.cid = cid
        self.num_code = num_code
        self.name = name
        self.value = value
        self.nominal = nominal
        self.char_code = char_code

    @property
    def cid(self) -> str:
        return self.__cid

    @property
    def num_code(self) -> str:
        return self.__num_code

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> float:
        return self.__value

    @property
    def nominal(self) -> int:
        return self.__nominal

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if not isinstance(char_code, str):
            raise TypeError("Char_code must be a string.")
        if char_code == "":
            raise ValueError("Char_code cannot be empty.")
        self.__char_code = char_code.strip()

    @cid.setter
    def cid(self, cid: str):
        if not isinstance(cid, str):
            raise TypeError("ID must be an string.")
        self.__cid = cid

    @num_code.setter
    def num_code(self, num_code: str):
        if not isinstance(num_code, str):
            raise TypeError("Num_code must be a string.")
        if num_code == "":
            raise ValueError("Num_code cannot be empty.")
        self.__num_code = num_code.strip()

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if name == "":
            raise ValueError("Name cannot be empty.")
        self.__name = name.strip()

    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number.")
        if value < 0:
            raise ValueError("Value must be a non-negative number.")
        self.__value = float(value)

    @nominal.setter
    def nominal(self, nominal: int):
        if not isinstance(nominal, int):
            raise TypeError("Nominal must be an integer.")
        if nominal <= 0:
            raise ValueError("Nominal must be a positive integer.")
        self.__nominal = nominal

